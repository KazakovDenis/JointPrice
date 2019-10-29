# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import xml.etree.ElementTree as ET
import requests
import os.path
import xlrd
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
    purchase_price = db.Column(db.Float)         # цена закупки
    retail_price = db.Column(db.Integer)         # рекомендуема розничная цена
    markup = db.Column(db.Float)                 # наценка
    selling_price = db.Column(db.Integer)        # моя цена продажи
    low_price = db.Column(db.Integer)            # цена "для своих"
    weight = db.Column(db.Float)
    volume = db.Column(db.Float)
    origin = db.Column(db.String(40))
    manufacturer = db.Column(db.String(40))
    description = db.Column(db.Text)
    updated = db.Column(db.DateTime, default=datetime.now())

    # def __init__(self, *args, **kwargs):
    #     self.markup = 1.2 if not kwargs.get('markup') else kwargs.get('markup')
    #     if not kwargs.get('selling_price'):
    #         self.selling_price = int((kwargs.get('purchase_price') or 0) * self.markup)

    def __repr__(self):
        return f'{self.id}.[{self.article}] {self.title}'


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
        super().__init__(*args, **kwargs)
        self.category = 'Шины легковые'
        self.runflat = True if kwargs.get('runflat') else False
        self.powerload = True if kwargs.get('powerload') else False
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


class Fasteners(Product, db.Model):
    fast_type = db.Column(db.String(20))
    outer_diam = db.Column(db.Float)
    inner_diam = db.Column(db.Float)
    nut_height = db.Column(db.Float)
    thread_diam = db.Column(db.String(5))    # e.g. M14
    thread_length = db.Column(db.Float)
    key_size = db.Column(db.Integer)
    fast_shape = db.Column(db.String(20))
    fast_pitch = db.Column(db.Float)
    color = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.markup = 1.30
        super(Fasteners, self).__init__(*args, **kwargs)
        self.category = 'Колёсный крепёж'


class Secrets(Product, db.Model):
    lock_type = db.Column(db.String(20))
    diameter = db.Column(db.String(5))    # e.g. M14
    length = db.Column(db.Float)
    thread_step = db.Column(db.Float)
    head_size = db.Column(db.String(20))
    head_form = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.markup = 1.30
        super(Secrets, self).__init__(*args, **kwargs)
        self.category = 'Секретки'


class Battery(Product, db.Model):
    capacity = db.Column(db.Integer)
    polarity = db.Column(db.String(20))
    cleats = db.Column(db.String(20))
    current = db.Column(db.Integer)
    voltage = db.Column(db.Integer)
    dimensions = db.Column(db.String(20))

    def __init__(self, *args, **kwargs):
        self.markup = 1.30
        super(Battery, self).__init__(*args, **kwargs)
        self.category = 'Аккумуляторы'

        if not kwargs.get('article'):
            self.article = 'SAK' + datetime.now().strftime('%d%m%Y') + str(kwargs.get('voltage')) + \
                            str(int(kwargs.get('capacity'))) + str(kwargs.get('current'))


product_model = {
    'car_tires': CarTire,
    'car_rims': CarRim,
    'truck_tires': TruckTire,
    'truck_rims': TruckRim,
    'fasteners': Fasteners,
    'secrets': Secrets,
    'batteries': Battery
}


class PriceList:
    count = 0
    extensions = ('xml', 'xlsx', 'xls')

    def __init__(self, price_dict, products):
        PriceList.count += 1
        self.url = price_dict[products]
        self.supplier = price_dict['title']
        self.model = product_model.get(products)
        self._extension = '.' + str([extension for extension in self.extensions if extension in self.url][0])
        self.file_name = price_dict['title'] + '_' + products + self._extension

    def download(self):
        """ Creates a cached price list on the local machine """
        response = get_response(self.url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            file_object = response.text

            with open(f'{os.path.join("prices", self.file_name)}', 'w', encoding='utf-8') as cached:
                cached.write(file_object)


class XMLPriceList(PriceList):
    product_tags_stop_list = ('DESCRIPTION', 'company', 'name', 'version', 'info')

    def __init__(self, price_dict, products):
        super().__init__(price_dict, products)
        self.tree = self._get_tree()
        self.product_elements = self._get_products_parent_tag()
        self.product_generator = self._generate_product()

    def _get_tree(self):
        """ Gets an XML tree of cached price """
        if os.path.exists(f'prices/{self.file_name}'):
            with open(f'prices/{self.file_name}', 'r', encoding='utf-8', errors='ignore') as cached:
                xml_object = cached.read()
            tree = ET.fromstring(xml_object)[0] if self.supplier == 'svrauto' else ET.fromstring(xml_object)
            return tree
        print('No cached file. Download the price list at first: .download()')

    def _get_nesting_level(self):
        """ Looks for nesting level of product info in XML tree. Returns a level and a root """
        if os.path.exists(f'{os.path.join("prices", self.file_name)}'):

            def _iter_nesting_level(items, level=0):
                for item in items:
                    if len(item) > 0:
                        level += 1
                        level = _iter_nesting_level(item, level=level)
                        break
                return level

            tree = ET.parse(f'{os.path.join("prices", self.file_name)}')
            root = tree.getroot()
            nesting_level = _iter_nesting_level(root)
            return nesting_level, root
        return 'Nesting level is impossible to measure'

    def _get_products_parent_tag(self):
        """ Returns a list of XML-elements contains products """
        def recursive_search(level_: int, element: list):
            for items in root:
                level_ -= 1
                if level_ > 0:
                    recursive_search(level_, items)
                return items

        level, root = self._get_nesting_level()
        if level <= 1:
            return root
        else:
            elements = recursive_search(level, root)
            return elements

    def _generate_product(self):
        for product_element in self.product_elements:
            if product_element.tag in self.product_tags_stop_list:
                continue
            if self.supplier == 'pwrs':
                if 'car_tires' in self.file_name and product_element.tag != 'tires' or\
                        'car_rims' in self.file_name and product_element.tag != 'rims':
                    continue
            yield product_element

    def extract_next_product_parameters(self):
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


class XLSPriceList(PriceList):

    def __init__(self, price_dict, products):
        super().__init__(price_dict, products)

    def extract_next_product_parameters(self):
        pass
