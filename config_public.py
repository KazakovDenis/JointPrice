# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
import os


class Configuration:
    DEBUG = True
    basedir = os.path.abspath(os.path.dirname(__file__)) + os.path.sep + 'data'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_migrations')
    SECRET_KEY = 'abc123'
    SECURITY_PASSWORD_SALT = '321cba'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'


svrauto_url = 'https://svrauto.ru/'

svrauto = {
    'title': 'svrauto',
    'car_tires': svrauto_url + '&types=1',
    'car_rims': svrauto_url + '&types=2',
    'truck_tires': svrauto_url + '&types=3',
    'truck_rims': svrauto_url + '&types=4',
    'secrets': svrauto_url + '&types=5',
    'fasteners': svrauto_url + '&types=6'
}

pwrs = {
    'title': 'pwrs',
    'car_tires': 'https://pwrs.ru/1.xml',
    'car_rims': 'https://pwrs.ru/2.xml',
    'car_tires_for_order': 'https://pwrs.ru/3.xml',
    'car_rims_for_order': 'https://pwrs.ru/4.xml'
}

trektyre = {
    'title': 'trektyre',
    'car_tires_for_order': 'https://trektyre.ru/load-price-xml?url=1',
    'truck_tires_for_order': 'https://trektyre.ru/load-price-xml?url=2'
}

# all_product_parameters[parameter][supplier] = supplier's tag title in XML
all_product_parameters = {
    'article': {'svrauto': 'SMNFCODE', 'pwrs': 'cae', 'trektyre': 'tag'},
    'title': {'svrauto': 'SMODIFNAME', 'pwrs': 'name', 'trektyre': 'tag'},
    'brand': {'svrauto': 'SMARKA', 'pwrs': 'brand', 'trektyre': 'tag'},
    'model': {'svrauto': 'SMODEL', 'pwrs': 'model', 'trektyre': 'tag'},
    'img': {'svrauto': 'SPICTURE', 'pwrs': 'img_big_my', 'trektyre': 'tag'},
    'supplier': {'svrauto': 'svrauto', 'pwrs': 'pwrs', 'trektyre': 'trektyre'},
    'address': {'svrauto': 'TERRITORY_NAME', 'pwrs': 'tag', 'trektyre': 'Екатеринбург'},
    'count': {'svrauto': 'NREST', 'pwrs': 'rest_novosib', 'trektyre': 'tag', 'pwrs_for_order': 'rest'},
    'purchase_price': {'svrauto': 'NPRICE_PREPAYMENT', 'pwrs': 'price_novosib', 'trektyre': 'tag'},
    'retail_price': {'svrauto': 'NPRICE_RRP', 'pwrs': 'price_novosib_rozn', 'trektyre': 'tag'},
    'selling_price': {'svrauto': 0, 'pwrs': 0, 'trektyre': 0},
    'low_price': {'svrauto': 0, 'pwrs': 0, 'trektyre': 0},
    'description': {'svrauto': 'tag', 'pwrs': 'tag', 'trektyre': 'tag'},
    'width': {'svrauto': 'SWIDTH', 'pwrs': 'width', 'trektyre': 'tag'},
    'height': {'svrauto': 'SHEIGHT', 'pwrs': 'height', 'trektyre': 'tag'},
    'diameter': {'svrauto': 'SDIAMETR', 'pwrs': 'diameter', 'trektyre': 'tag'},
    'season': {'svrauto': 'SSEASON', 'pwrs': 'season', 'trektyre': 'tag'},
    'stud': {'svrauto': 'STHORNING', 'pwrs': 'thorn', 'trektyre': 'tag'},
    'speed_index': {'svrauto': 'SSPEED', 'pwrs': 'speed_index', 'trektyre': 'tag'},
    'load_index': {'svrauto': 'SLOAD', 'pwrs': 'load_index', 'trektyre': 'tag'},
    'runflat': {'svrauto': 'RUNFLAT', 'pwrs': 'runflat', 'trektyre': 'tag'},
    'powerload': {'svrauto': 'POWERLOAD', 'pwrs': 'tonnage', 'trektyre': 'tag'},
    'purpose': {'svrauto': 'PURPOSE', 'pwrs': 'tag', 'trektyre': 'tag'},
    'omologation': {'svrauto': 'HOMOLOGATION', 'pwrs': 'omolog', 'trektyre': 'tag'},
    'cartype': {'svrauto': 'CARTYPE', 'pwrs': 'tiretype', 'trektyre': 'tag'},
}

suppliers = [svrauto, pwrs, trektyre]