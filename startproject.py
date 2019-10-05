# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from models import *
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
        os.system('python manage.py db init')
        os.system('python manage.py db migrate')
        os.system('python manage.py db upgrade')
    print('Project is ready!')


if __name__ == '__main__':
    start()
