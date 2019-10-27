# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import xml.etree.ElementTree as ET
import requests
import os.path
from datetime import datetime
from random import uniform
from time import sleep
from jointprices import db
from config import *


def get_response(url):
    """ Returns response. Looking for <Response [200]> """
    print(f'\nConnecting to {url}')
    try:
        user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = requests.get(url, headers=user_agent, timeout=90)
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
    product_tags_stop_list = ('DESCRIPTION', 'company', 'name', 'version', 'info')

    def __init__(self, price_dict, products):
        self.url = price_dict[products]
        self.supplier = price_dict['title']
        self.file_name = price_dict['title'] + '_' + products + '.xml'
        self.tree = self.get_tree()
        self.product_elements = self.get_products_parent_tag()
        self.product_generator = self.generate_product()
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
            tree = ET.fromstring(xml_object)[0] if self.supplier == 'svrauto' else ET.fromstring(xml_object)
            return tree
        print('No cached file. Download the price list at first: .download()')

    def get_nesting_level(self):
        """ Looks for nesting level of product info in XML tree. Returns a level and a root """
        if os.path.exists(f'prices/{self.file_name}'):

            def _iter_nesting_level(items, level=0):
                for item in items:
                    if len(item) > 0:
                        level += 1
                        level = _iter_nesting_level(item, level=level)
                        break
                return level

            tree = ET.parse(f'prices/{self.file_name}')
            root = tree.getroot()
            nesting_level = _iter_nesting_level(root)
            return nesting_level, root
        return 'Nesting level is impossible to measure'

    def get_products_parent_tag(self):
        """ Returns a list of XML-elements contains products """
        def recursive_search(level: int, element: list):
            for items in root:
                level -= 1
                if level > 0:
                    recursive_search(level, items)
                return items

        level, root = self.get_nesting_level()
        if 0 <= level <= 1:
            return root
        else:
            elements = recursive_search(level, root)
            return elements

    def generate_product(self):
        for product_element in self.product_elements:
            if product_element.tag in PriceList.product_tags_stop_list:
                continue
            if self.supplier == 'pwrs' and 'car_tires' in self.file_name and product_element.tag != 'tires':
                return None
            yield product_element

    def extract_product_parameters(self):
        """ Returns a dictionary of product parameters """
        try:
            product_element = next(self.product_generator)
        except StopIteration:
            return None
        product_parameters = dict(supplier=self.supplier)
        for parameter in all_product_parameters:
            for element in product_element:
                if element.tag == all_product_parameters[parameter].get(self.supplier) and element.text:
                    product_parameters[parameter] = int(element.text) if element.text.isdigit() else element.text
        product_parameters['low_price'] = int((product_parameters.get('purchase_price') or 0) * 1.05)
        return product_parameters


class Product:
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40))
    article = db.Column(db.String(40))
    title = db.Column(db.String(250))
    brand = db.Column(db.String(40))
    brand_latin = db.Column(db.String(40))
    model = db.Column(db.String(40))
    img = db.Column(db.String(200))
    supplier = db.Column(db.String(40))
    address = db.Column(db.String(40))
    count = db.Column(db.Integer)
    purchase_price = db.Column(db.Float)     # цена закупки
    retail_price = db.Column(db.Integer)     # рекомендуема розничная цена
    selling_price = db.Column(db.Integer)    # моя цена продажи
    low_price = db.Column(db.Integer)        # цена "для своих"
    weight = db.Column(db.Float)
    origin = db.Column(db.String(40))
    manufacturer = db.Column(db.String(40))
    description = db.Column(db.Text)
    updated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f'{self.id}. Art № {self.article} - {self.title}'


class CarTire(Product, db.Model):
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    diameter = db.Column(db.String(5))
    season = db.Column(db.String(10))
    stud = db.Column(db.String(10))
    speed_index = db.Column(db.String(3))
    load_index = db.Column(db.String(10))
    runflat = db.Column(db.Boolean, default=False)
    powerload = db.Column(db.Boolean, default=False)
    purpose = db.Column(db.String(20))
    omologation = db.Column(db.String(20))
    cartype = db.Column(db.String(30))

    def __init__(self, *args, **kwargs):
        super(CarTire, self).__init__(*args, **kwargs)
        self.category = 'Шины легковые'
        self.runflat = True if kwargs.get('runflat') else False
        self.powerload = True if kwargs.get('powerload') else False
        self.selling_price = int((kwargs.get('purchase_price') or 0) * 1.2)
        self.stud = self.get_stud(kwargs.get('stud')) if not kwargs.get('stud') else None
        self.season = self.get_season(kwargs.get('season')) if kwargs.get('season') else None

        if kwargs.get('supplier') == 'pwrs':
            self.title = kwargs.get('brand') + kwargs.get('title')

    @staticmethod
    def get_stud(arg):
        arg = str(arg).lower()
        if arg == 'ш.' or arg == 'да' or arg == 'y':
            return 'шипованная'
        elif arg == 'н/ш.' or arg == 'n':
            return 'нешипованная'

    @staticmethod
    def get_season(arg):
        arg = str(arg).lower()
        if arg == 'летняя' or arg == 'лето':
            return 'летняя'
        elif arg == 'зимняя' or arg == 'зима':
            return 'зимняя'
        elif arg == 'всесезонная' or arg == 'всесезон':
            return 'всесезонная'


class CarRim(Product, db.Model):
    width = db.Column(db.String(20))
    height = db.Column(db.String(20))
    diameter = db.Column(db.String(20))
    holes = db.Column(db.String(20))
    PCD = db.Column(db.String(20))
    offset = db.Column(db.String(20))
    dia = db.Column(db.String(20))
    rim_type = db.Column(db.String(20))
    color = db.Column(db.String(20))
    treatment = db.Column(db.String(20))
    for_car = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        super(CarRim, self).__init__(*args, **kwargs)
        self.category = 'Диски легковые'


class TruckTire(Product, db.Model):
    truck_width = db.Column(db.Integer)
    truck_height = db.Column(db.Integer)
    truck_diameter = db.Column(db.String(5))
    speed_index = db.Column(db.String(3))
    load_index = db.Column(db.String(10))
    axis = db.Column(db.String(40))
    tube = db.Column(db.String(20))
    layer = db.Column(db.String(20))
    type = db.Column(db.String(40))
    restored = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        super(TruckTire, self).__init__(*args, **kwargs)
        self.category = 'Шины грузовые'


class TruckRim(Product, db.Model):
    width = db.Column(db.Float)
    diameter = db.Column(db.Integer)
    holes = db.Column(db.Integer)
    PCD = db.Column(db.Float)
    offset = db.Column(db.String(20))
    dia = db.Column(db.Float)
    rim_type = db.Column(db.String(20))
    color = db.Column(db.String(20))
    treatment = db.Column(db.String(40))
    for_car = db.Column(db.String(40))

    def __init__(self, *args, **kwargs):
        super(TruckRim, self).__init__(*args, **kwargs)
        self.category = 'Диски грузовые'


class Battery(Product, db.Model):
    capacity = db.Column(db.Integer)
    polarity = db.Column(db.String(20))
    cleats = db.Column(db.String(20))
    current = db.Column(db.Integer)
    voltage = db.Column(db.Integer)
    dimensions = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        super(Battery, self).__init__(*args, **kwargs)
        self.category = 'Аккумуляторы'
