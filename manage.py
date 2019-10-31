# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os
from threading import Thread
from jointprices import app, manager, db
from config import suppliers
from models import *
""" Module contains functions to manage the project """


def download_prices_of(supplier):
    print('Starting to download price lists of ', supplier)
    # starting svrauto in a parallel thread
    if supplier['title'] == 'svrauto':
        def _download_svr():
            for price_ in supplier:
                if price_ != 'title':
                    PriceList(supplier, price_).download()
                    print('Now sleeping for 11 minutes because of svrauto lock')
                    sleep(60 * 11)
        Thread(target=_download_svr).start()
    else:
        # loading another supplier's prices
        [PriceList(supplier, price).download() for price in supplier if price != 'title']


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
    """ Fills up and updates the db from chosen supplier and price list """
    price_obj = XMLPriceList(supplier, price) if 'xml' in price else XLSPriceList(supplier, price)
    while True:
        product_params = price_obj.extract_next_product_parameters()
        if product_params:
            product = price_obj.model(**product_params)
            add_to_db(product)
        else:
            break


def update_db_by(supplier):
    """ Fills up and updates the db from chosen supplier """
    [update_db_category(supplier, price) for price in supplier if price != 'title']


def update_db_entirely():
    """ Fills up and updates the db entirely """
    [update_db_by(supplier) for supplier in suppliers]


def get_markups() -> dict:
    with open(os.path.join('data', 'markups.txt'), 'r', encoding='utf-8') as file:
        rows = file.readlines()
        markups = {row.split('=')[0].strip(): float(row.split('=')[-1].strip()) for row in rows if '#' not in row}
    return markups


# delete after usage
def sak_fill_db():
    """ Uploads SAK goods to db from the prepared file """
    book = xlrd.open_workbook(os.path.join('prices', 'sakbase.xlsx'), encoding_override='cp1252')
    sheet = book.sheet_by_index(0)
    markups = get_markups()
    for i in range(1, sheet.nrows):
        params = dict(supplier='sak')
        params['title'] = sheet.cell(i, 0).value
        params['brand'] = sheet.cell(i, 9).value
        params['img'] = sheet.cell(i, 4).value
        params['address'] = 'Есенина'
        params['count'] = int(sheet.cell(i, 6).value or 0)
        params['markup'] = [markups[brand] for brand in markups if brand in params['title']][0]
        params['selling_price'] = int(sheet.cell(i, 5).value or 0)
        params['weight'] = float(sheet.cell(i, 7).value or 0)
        params['origin'] = sheet.cell(i, 8).value
        params['manufacturer'] = sheet.cell(i, 14).value
        params['description'] = sheet.cell(i, 1).value
        params['capacity'] = int(sheet.cell(i, 10).value or 0)
        params['polarity'] = sheet.cell(i, 13).value
        params['cleats'] = sheet.cell(i, 12).value
        params['current'] = int(sheet.cell(i, 15).value or 0)
        params['voltage'] = int(sheet.cell(i, 11).value or 0)
        try:
            akb = Battery(**params)
            add_to_db(akb)
        except Exception as e:
            print(e)
            continue


if __name__ == '__main__':
    manager.run()
