# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from threading import Thread
from jointprices import manager, db
from config import suppliers
from models import *
from run import *
""" Module contains functions to manage the project """


def download_prices_of(supplier):
    print('Starting to download prices of', supplier['title'])
    def _download(price_list):
        print(f"Starting to download '{price_list}' of {supplier['title']}")
        price_obj = PriceList(supplier, price_list)
        price_obj.download()
        print(f"'{price_list}' of {supplier['title']} is downloaded")
    # starting svrauto in a parallel thread
    if supplier['title'] == 'svrauto':
        def _download_svr():
            for price_ in supplier:
                if price_ != 'title':
                    _download(price_)
                    print('Now sleeping for 11 minutes because of svrauto lock')
                    sleep(60 * 11)
        Thread(target=_download_svr).start()
    else:
        # loading another supplier's prices
        [_download(price) for price in supplier if price != 'title']


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
    if obj.category == 'Шины легковые':
        """ Adds an object to database. ex: >>> p = Post(title='Some title', body='Some body'); add_to_db(p) """
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
    else:
        print('Application is not ready to update this category:', obj.category)


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
    if 'car_tires' in price:
        price_obj = PriceList(supplier, price)
        handler = PriceHandler(price_obj)
        while True:
            product_params = handler.extract_product_parameters()
            if product_params:
                obj = CarTire(**product_params)
                add_to_db(obj)
            else:
                break
    else:
        print('Application is not ready to update this category:', price)


def update_db_by(supplier):
    """ Fills up and updates the db from chosen supplier """
    [update_db_category(supplier, price) for price in supplier if price != 'title']


def update_db_entirely():
    """ Fills up and updates the db entirely """
    [update_db_by(supplier) for supplier in suppliers]


if __name__ == '__main__':
    manager.run()
