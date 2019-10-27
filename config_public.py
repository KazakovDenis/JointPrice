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

sak = {
    'title': 'sak',
    'batteries': ''
}

# all_product_parameters[parameter][supplier] = supplier's tag title in XML
all_product_parameters = {
    'article': {'rus': 'Артикул', 'svrauto': 'SMNFCODE', 'pwrs': 'cae', 'trektyre': 'atricle'},
    'title': {'rus': 'Название', 'svrauto': 'SMODIFNAME', 'pwrs': 'name', 'trektyre': 'name'},
    'brand': {'rus': 'Марка', 'svrauto': 'SMARKA', 'pwrs': 'brand', 'trektyre': 'producer'},
    'brand_latin': {'rus': 'Марка', 'svrauto': 'SMARKORIG'},
    'model': {'rus': 'Модель', 'svrauto': 'SMODEL', 'pwrs': 'model', 'trektyre': 'model'},
    'img': {'rus': 'Изображение', 'svrauto': 'SPICTURE', 'pwrs': 'img_big_my', 'trektyre': 'img'},
    'address': {'rus': 'Склад', 'svrauto': 'TERRITORY_NAME'},
    'count': {'rus': 'Количество', 'svrauto': 'NREST', 'pwrs': 'rest_novosib', 'trektyre': 'StockEkb', 'pwrs_for_order': 'rest'},
    'purchase_price': {'rus': 'Цена закупки', 'svrauto': 'NPRICE_PREPAYMENT', 'pwrs': 'price_novosib', 'trektyre': 'price'},
    'retail_price': {'rus': 'Рекомендуемая цена', 'svrauto': 'NPRICE_RRP', 'pwrs': 'price_novosib_rozn', 'trektyre': 'rs'},
    'selling_price': {'rus': 'Цена продажи'},
    'low_price': {'rus': 'Цена для своих'},
    'description': {'rus': 'Описание', 'sak': None},
    'origin': {'rus': 'Описание', 'svrauto': 'SGOODLAND', 'sak': None},
    'manufacturer': {'rus': 'Описание', 'sak': None},
    'weight': {'rus': 'Масса', 'sak': None},
    # car tires
    'width': {'rus': 'Ширина', 'svrauto': 'SWIDTH', 'pwrs': 'width', 'trektyre': 'width'},
    'height': {'rus': 'Высота профиля', 'svrauto': 'SHEIGHT', 'pwrs': 'height', 'trektyre': 'h'},
    'diameter': {'rus': 'Диаметр', 'svrauto': 'SDIAMETR', 'pwrs': 'diameter', 'trektyre': 'radius'},
    'season': {'rus': 'Сезон', 'svrauto': 'SSEASON', 'pwrs': 'season', 'trektyre': 'season'},
    'stud': {'rus': 'Шипы', 'svrauto': 'STHORNING', 'pwrs': 'thorn', 'trektyre': 'stud'},
    'speed_index': {'rus': 'Индекс скорости', 'svrauto': 'SSPEED', 'pwrs': 'speed_index', 'trektyre': 'ss'},
    'load_index': {'rus': 'Индекс нагрузки', 'svrauto': 'SLOAD', 'pwrs': 'load_index', 'trektyre': 'li'},
    'runflat': {'rus': 'Технология Run Flat', 'svrauto': 'RUNFLAT', 'pwrs': 'runflat', 'trektyre': None},
    'powerload': {'rus': 'Усиление', 'svrauto': 'POWERLOAD', 'pwrs': 'reinforced', 'trektyre': None},
    'purpose': {'rus': 'Назначение', 'svrauto': 'PURPOSE', 'pwrs': None, 'trektyre': None},
    'omologation': {'rus': 'Омологация', 'svrauto': 'HOMOLOGATION', 'pwrs': 'omolog', 'trektyre': None},
    'cartype': {'rus': 'Тип автомобиля', 'svrauto': 'CARTYPE', 'pwrs': 'tiretype', 'trektyre': 'type'},
    # truck tires
    'truck_width': {'rus': 'Ширина', 'svrauto': 'STIREWIDTH', 'pwrs': 'tag', 'trektyre': 'tag'},
    'truck_height': {'rus': 'Высота профиля', 'svrauto': 'STIRERATIO', 'pwrs': 'tag', 'trektyre': 'tag'},
    'truck_diameter': {'rus': 'Диаметр', 'svrauto': 'STIREDIAM', 'pwrs': 'tag', 'trektyre': 'tag'},
    'axis': {'rus': 'Ось', 'svrauto': 'STIREAXLE', 'pwrs': 'tag', 'trektyre': 'tag'},
    'tube': {'rus': 'Камерность', 'svrauto': 'STIRETUBE', 'pwrs': 'tag', 'trektyre': 'tag'},
    'layer': {'rus': 'Слойность', 'svrauto': 'SLAYER', 'pwrs': 'tag', 'trektyre': 'tag'},
    'type': {'rus': 'Тип', 'svrauto': 'SUSETYPE', 'pwrs': 'tag', 'trektyre': 'tag'},
    'restored': {'rus': 'Восстановленность', 'svrauto': 'SRETREAD', 'pwrs': 'tag', 'trektyre': 'tag'},
    # car & truck rims
    'holes': {'rus': 'Количество отверстий', 'svrauto': 'SHOLESQUANT', 'pwrs': 'bolts_count', 'trektyre': 'tag'},
    'PCD': {'rus': 'PCD', 'svrauto': 'SPCD', 'pwrs': 'bolts_spacing', 'trektyre': 'tag'},
    'offset': {'rus': 'Вылет', 'svrauto': 'SWHEELOFFSET', 'pwrs': 'et', 'trektyre': 'tag'},
    'dia': {'rus': 'Вылет', 'svrauto': 'SDIA', 'pwrs': 'tag', 'trektyre': 'tag'},
    'color': {'rus': 'Цвет', 'svrauto': 'SCOLOR', 'pwrs': 'color', 'trektyre': 'tag'},
    'rim_type': {'rus': 'Цвет', 'svrauto': 'STYPE', 'pwrs': 'rim_type', 'trektyre': 'tag'},
    'treatment': {'rus': 'Цвет', 'svrauto': 'SPROCESSWAY', 'pwrs': 'rim_type', 'trektyre': 'tag'},
    'for_car': {'rus': 'Цвет', 'svrauto': 'SAUTOLIST', 'pwrs': 'rim_type', 'trektyre': 'tag'},
    # batteries
    'capacity': {'rus': 'Ёмкость', 'sak': 'None'},
    'polarity': {'rus': 'Полярность', 'sak': 'None'},
    'current': {'rus': 'Пусковой ток', 'sak': 'None'},
    'voltage': {'rus': 'Номинальное напряжение', 'sak': 'None'},
    'dimensions': {'rus': 'Габариты', 'sak': 'None'},
    'cleats': {'rus': 'Тип клемм', 'sak': 'None'},
}

suppliers = [svrauto, pwrs, trektyre, sak]
applied_sa_addresses = ('Твардовского/3', 'Шамшиных', 'Фабричная93', 'Кирова232', 'Ипподромск')
