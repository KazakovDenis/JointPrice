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
    'article': {'rus': 'Артикул', 'svrauto': 'SMNFCODE', 'pwrs': 'cae', 'trektyre': 'tag'},
    'title': {'rus': 'Название', 'svrauto': 'SMODIFNAME', 'pwrs': 'name', 'trektyre': 'tag'},
    'brand': {'rus': 'Марка', 'svrauto': 'SMARKA', 'pwrs': 'brand', 'trektyre': 'tag'},
    'model': {'rus': 'Модель', 'svrauto': 'SMODEL', 'pwrs': 'model', 'trektyre': 'tag'},
    'img': {'rus': 'Изображение', 'svrauto': 'SPICTURE', 'pwrs': 'img_big_my', 'trektyre': 'tag'},
    'supplier': {'rus': 'Поставщик', 'svrauto': 'svrauto', 'pwrs': 'pwrs', 'trektyre': 'trektyre'},
    'address': {'rus': 'Склад', 'svrauto': 'TERRITORY_NAME', 'pwrs': 'tag', 'trektyre': 'Екатеринбург'},
    'count': {'rus': 'Количество', 'svrauto': 'NREST', 'pwrs': 'rest_novosib', 'trektyre': 'tag', 'pwrs_for_order': 'rest'},
    'purchase_price': {'rus': 'Цена закупки', 'svrauto': 'NPRICE_PREPAYMENT', 'pwrs': 'price_novosib', 'trektyre': 'tag'},
    'retail_price': {'rus': 'Рекомендуемая цена', 'svrauto': 'NPRICE_RRP', 'pwrs': 'price_novosib_rozn', 'trektyre': 'tag'},
    'selling_price': {'rus': 'Цена продажи', 'svrauto': 0, 'pwrs': 0, 'trektyre': 0},
    'low_price': {'rus': 'Цена для своих', 'svrauto': 0, 'pwrs': 0, 'trektyre': 0},
    'description': {'rus': 'Описание', 'svrauto': 'tag', 'pwrs': 'tag', 'trektyre': 'tag'},
    'width': {'rus': 'Ширина', 'svrauto': 'SWIDTH', 'pwrs': 'width', 'trektyre': 'tag'},
    'height': {'rus': 'Высота профиля', 'svrauto': 'SHEIGHT', 'pwrs': 'height', 'trektyre': 'tag'},
    'diameter': {'rus': 'Диаметр', 'svrauto': 'SDIAMETR', 'pwrs': 'diameter', 'trektyre': 'tag'},
    'season': {'rus': 'Сезон', 'svrauto': 'SSEASON', 'pwrs': 'season', 'trektyre': 'tag'},
    'stud': {'rus': 'Шипы', 'svrauto': 'STHORNING', 'pwrs': 'thorn', 'trektyre': 'tag'},
    'speed_index': {'rus': 'Индекс скорости', 'svrauto': 'SSPEED', 'pwrs': 'speed_index', 'trektyre': 'tag'},
    'load_index': {'rus': 'Индекс нагрузки', 'svrauto': 'SLOAD', 'pwrs': 'load_index', 'trektyre': 'tag'},
    'runflat': {'rus': 'Технология Run Flat', 'svrauto': 'RUNFLAT', 'pwrs': 'runflat', 'trektyre': 'tag'},
    'powerload': {'rus': 'Усиление', 'svrauto': 'POWERLOAD', 'pwrs': 'tonnage', 'trektyre': 'tag'},
    'purpose': {'rus': 'Назначение', 'svrauto': 'PURPOSE', 'pwrs': 'tag', 'trektyre': 'tag'},
    'omologation': {'rus': 'Омологация', 'svrauto': 'HOMOLOGATION', 'pwrs': 'omolog', 'trektyre': 'tag'},
    'cartype': {'rus': 'Тип автомобиля', 'svrauto': 'CARTYPE', 'pwrs': 'tiretype', 'trektyre': 'tag'},
}

suppliers = [svrauto, pwrs, trektyre]