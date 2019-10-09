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
        response = input('The project is ready! Should I download prices or will you do it later? [y/n] --> ').lower()
        if response == 'y':
            print('Ok! It will take some time.')
            download_all_prices()
            print('Download is complete! Now you can fill up the database with update_db_entirely() from manage.py')
        else:
            print('For this purpose use download_all_prices() from manage.py')


if __name__ == '__main__':
    start()
