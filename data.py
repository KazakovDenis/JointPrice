# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from config import all_product_parameters
from models import *
from manage import add_to_db


def get_products(price_obj):
    def recursive_search(level):
        for items in root:
            level -= 1
            if level > 0:
                recursive_search(level)
            return items
    level, root = price_obj.get_nesting_level()
    return recursive_search(level)


def extract_product_parameters(product_element, supplier):
    """ Returns a dictionary of product parameters """
    product_parameters = dict()
    if not product_element.tag == 'DESCRIPTION':
        for parameter in all_product_parameters:
            for element in product_element:
                if element.tag == all_product_parameters[parameter][supplier]:
                    product_parameters[parameter] = element.text
    return product_parameters


def update_db(product_parameters):
    obj = CarTire(**product_parameters)
    add_to_db(obj)
