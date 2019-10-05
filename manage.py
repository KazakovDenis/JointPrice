# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from jointprices import manager, db
from models import *
from run import *
""" Module contains functions to manage the project """


def check_relevance(obj):
    """ Returns True if the record contains current price and quantity data """
    obj_check_sum = obj.article + obj.title + str(obj.count) + str(obj.purchase_price)
    select = eval(obj.__class__.__name__).query.filter_by
    record_in_db = select(supplier=obj.supplier, title=obj.title, article=obj.article).first()
    record_check_sum = record_in_db.article + record_in_db.title + \
                       str(record_in_db.count) + str(record_in_db.purchase_price)
    if record_check_sum == obj_check_sum:
        return True


def add_to_db(obj):
    """ Adds a list of objects to database. ex: >>> p = Post(title='Some title', body='Some body'); add_to_db(p) """
    if not check_relevance(obj):
        db.session.add(obj)
        db.session.commit()
        print(f'Object "{obj}" have been created (updated)!')


def delete_from_db(obj, confirm='n'):
    if confirm != 'y':
        confirm = input('Are you sure? [y/n] --> ').lower()
    if confirm != 'y':
        return
    else:
        db.session.delete(obj)
        db.session.commit()
        print(f'Object "{obj}" has been deleted!')


if __name__ == '__main__':
    manager.run()
