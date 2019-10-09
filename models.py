# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import xml.etree.ElementTree as ET
import requests
import os.path
from datetime import datetime
from itertools import repeat
from random import uniform
from time import sleep
from jointprices import db
from config import svrauto, pwrs, trektyre, all_product_parameters


def get_response(url):
    """ Returns response. Looking for <Response [200]> """
    print(f'\nConnecting to {url}')
    try:
        useragent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = requests.get(url, headers=useragent, timeout=90)
        pause = uniform(2, 9)
        sleep(pause)
        return response
    # в случае бана пробуем снова с бОльшей паузой
    except requests.exceptions.RequestException as e:
        print(f'get_response error: {e}.')
        pause = uniform(10, 15)
        sleep(pause)
        get_response(url)
    except Exception as e:
        print(f'get_response another error: {e}.')


class PriceList:
    count = 0

    def __init__(self, price_dict, products):
        self.url = price_dict[products]
        self.supplier = price_dict['title']
        self.file_name = price_dict['title'] + '_' + products + '.xml'
        self.tree = self.get_tree()
        PriceList.count += 1

    def download(self):
        """ Creates a cached price list on the local machine """
        response = get_response(self.url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            xml_object = response.text

            with open(f'prices/{self.file_name}', 'w', encoding='utf-8') as cached:
                cached.write(xml_object)

    def get_tree(self):
        """ Gets an XML tree of cached price """
        if os.path.exists(f'prices/{self.file_name}'):
            with open(f'prices/{self.file_name}', 'r', encoding='utf-8', errors='ignore') as cached:
                xml_object = cached.read()
            tree = ET.fromstring(xml_object)[0]
            return tree
        print('No cached file. Download the price list at first: .download()')

    def get_nesting_level(self):
        """ Looks for nesting level of product info in XML tree. Returns a level and a root """
        if os.path.exists(f'prices/{self.file_name}'):
            def _iter_nesting_level(items, level=0):
                if items[0]:
                    level += 1
                    level = _iter_nesting_level(items[0], level=level)
                return level
            tree = ET.parse(f'prices/{self.file_name}')
            root = tree.getroot()
            nesting_level = _iter_nesting_level(root)
            return nesting_level, root
        return 'Nesting level is impossible to measure'

    def get_product_elements(self):
        """ Returns a list of XML-elements contains products """
        def recursive_search(level: int, element: list):
            for items in root:
                level -= 1
                if level > 0:
                    recursive_search(level, items)
                return items

        level, root = self.get_nesting_level()
        return recursive_search(level, root)

    # methods to consider the need
    @staticmethod
    def _get_product_by(params):
        """ Secondary function for get_product_objs filter() """
        items, tag, value = params
        if type(value) == int and 'PRICE' in tag:
            for item in items:
                if item.tag == tag and int(item.text or 0) <= value:
                    return True
        elif type(value) == int and 'REST' in tag:
            for item in items:
                if item.tag == tag and int(item.text or 0) >= value:
                    return True
        elif type(value) == int and 'PRICE' not in tag and 'REST' not in tag:
            for item in items:
                if item.tag == tag and int(item.text or 0) == value:
                    return True
        else:
            for item in items:
                if item.tag == tag and item.text == value:
                    return True

    def get_product_objs(self, products=None, **filters):
        """ Returns list of products filtered by parameters in kwargs """
        if not products:
            products = self.tree[1:]

        key = list(filters.keys())[0]
        filtered = list(filter(self._get_product_by, zip(products, repeat(key), repeat(filters[key]))))
        result = [i[0] for i in filtered]

        del filters[key]
        if len(filters) > 0:
            result = self.get_product_objs(products=result, **filters)

        return result

    def show_products_as_dicts(self, **filters):
        """
        Returns found products from the XML tree in a format ready to display.
        Example filter: filters_ = {'NPRICE_RRP': 10600, 'SMARKA': 'SATOYA', 'NREST': 20}
         """
        filtered_products = self.get_product_objs(**filters)
        found = {}
        for product in filtered_products:
            found[product] = {}
            for attribute in product:
                found[product][attribute.tag] = attribute.text
        return found

    def print_products(self, **filters):
        found = self.show_products_as_dicts(**filters)
        for key, value in found.items():
            print(key, ':')
            for key1, value1 in value.items():
                print('\t', key1, ' - ', value1)


class PriceHandler:
    """ It extracts products from Price """
    def __init__(self, price_obj):
        self.supplier = price_obj.supplier
        self.product_elements = price_obj.get_product_elements()
        self.product_generator = self.generate_product()

    def generate_product(self):
        for product_element in self.product_elements:
            if product_element.tag == 'DESCRIPTION':
                continue
            yield product_element

    def extract_product_parameters(self):
        """ Returns a dictionary of product parameters """
        try:
            product_element = next(self.product_generator)
        except StopIteration:
            return None
        product_parameters = dict()
        for parameter in all_product_parameters:
            for element in product_element:
                if element.tag == all_product_parameters[parameter][self.supplier] and element.text:
                    if element.text.isdigit():
                        product_parameters[parameter] = int(element.text)
                    else:
                        product_parameters[parameter] = element.text
        product_parameters['supplier'] = self.supplier
        try:
            product_parameters['low_price'] = int(product_parameters['purchase_price'] * 1.05)
        except KeyError:
            pass
        return product_parameters


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40))
    article = db.Column(db.String(40))
    title = db.Column(db.String(250))
    brand = db.Column(db.String(40))
    model = db.Column(db.String(40))
    img = db.Column(db.String(200))
    supplier = db.Column(db.String(40))
    address = db.Column(db.String(40))
    count = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)   # цена закупки
    retail_price = db.Column(db.Integer)     # рекомендуема розничная цена
    selling_price = db.Column(db.Integer)    # моя цена продажи
    low_price = db.Column(db.Integer)        # цена "для своих"
    description = db.Column(db.Text)
    updated = db.Column(db.DateTime, default=datetime.now())
    # category = db.Column(db.ForeignKey('category.title'))

    def __repr__(self):
        return f'{self.id}. Art № {self.article} - {self.title}'


class CarTire(Product):
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    diameter = db.Column(db.String(5))
    season = db.Column(db.String(10))
    stud = db.Column(db.String(10))
    speed_index = db.Column(db.String(3))
    load_index = db.Column(db.Integer)
    runflat = db.Column(db.Boolean, default=False)
    powerload = db.Column(db.Boolean, default=False)
    purpose = db.Column(db.String(20))
    omologation = db.Column(db.String(20))
    cartype = db.Column(db.String(30))

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.category = 'Шины легковые'
        self.runflat = True if kwargs.get('runflat') else False
        self.powerload = True if kwargs.get('powerload') else False
        self.selling_price = int((kwargs.get('purchase_price') or 0) * 1.2)

# class CarRim(Product):
#     pass
#
#
# class TruckTire(Product):
#     pass
#
#
# class TruckRim(Product):
#     pass
#
#
# class Battery(Product):
#     pass


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50))
#
#     def __repr__(self):
#         return f'{self.id}. {self.title}'
