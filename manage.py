# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from jointprices import manager, db
from config import suppliers
from models import *
from run import *
""" Module contains functions to manage the project """


def download_prices_of(supplier):
    if supplier['title'] == 'svrauto':
        os.system('python svrauto.py')
        return
    for price in supplier:
        if price != 'title':
            price_obj = PriceList(supplier, price)
            price_obj.download()


def download_all_prices():
    for supplier in suppliers:
        download_prices_of(supplier)


def check_relevance(obj):
    """ Returns True if the record contains current price and quantity data """
    # checking the object itself
    try:
        obj_check_sum = str(obj.article) + obj.title + str(obj.count) + str(obj.purchase_price)
    except AttributeError:
        return None
    # doing a query
    select = eval(obj.__class__.__name__).query.filter_by
    record_in_db = select(supplier=obj.supplier, title=obj.title, article=obj.article).first()
    if not record_in_db:
        return 'Not in db', None
    # comparing the object and the record in db
    record_check_sum = str(record_in_db.article) + record_in_db.title + \
                       str(record_in_db.count) + str(record_in_db.purchase_price)
    if record_check_sum == obj_check_sum:
        return 'Relevant', None
    else:
        return 'Needs update', record_in_db


def add_to_db(obj):
    """ Adds a list of objects to database. ex: >>> p = Post(title='Some title', body='Some body'); add_to_db(p) """
    relevant = check_relevance(obj)
    if relevant[0] == 'Not in db':
        db.session.add(obj)
        db.session.commit()
        print(f'Record "{obj}" has been added to DB!')
    elif relevant[0] == 'Relevant':
        print(f'Record "{obj}" is already relevant')
    elif relevant[0] == 'Needs update':
        record = relevant[1]
        record.count = obj.count
        record.purchase_price = obj.purchase_price
        db.session.commit()
        print(f'Record "{obj}" has been updated in DB!')
    else:
        print(f'WARNING! {obj} has no required parameters')


def delete_from_db(obj, confirm='n'):
    if confirm != 'y':
        confirm = input('Are you sure? [y/n] --> ').lower()
    if confirm != 'y':
        return
    else:
        db.session.delete(obj)
        db.session.commit()
        print(f'Record "{obj}" has been deleted from DB!')


def update_db_category(supplier, price):
    price_obj = PriceList(supplier, price)
    handler = PriceHandler(price_obj)
    while True:
        product_params = handler.extract_product_parameters()
        if product_params:
            obj = CarTire(**product_params)
            add_to_db(obj)
        else:
            break


def update_db_by(supplier):
    """ Fills up and updates the db from chosen supplier """
    if supplier == 'svrauto':
        print(', '.join([i for i in supplier]))
        price = input('SVRAUTO requires 15 minute pause between downloads. Choose a price to update -->')
        update_db_category(supplier, price)
    else:
        for price in supplier:
            if price != 'title':
                update_db_category(supplier, price)


def update_db_entirely():
    """ Fills up the db entirely """
    for supplier in suppliers:
        update_db_by(supplier)


if __name__ == '__main__':
    manager.run()
