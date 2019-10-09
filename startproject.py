# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from jointprices import db
from manage import download_all_prices
from models import *
from config import *
import os
""" Module executes functions to start the project """


def init_tables_from_models():
    db.create_all()
    db.session.commit()
    print(f'Tables have been created!')


def start():
    check = input('Are you sure database has been created and config.py has been edited? [y/n] --> ').lower()
    if check == 'y':
        init_tables_from_models()
        os.system('mkdir data && mkdir prices')
        os.system('python manage.py db init')
        os.system('python manage.py db migrate')
        os.system('python manage.py db upgrade')
        print('Project is ready! You may now download prices.')


if __name__ == '__main__':
    start()
