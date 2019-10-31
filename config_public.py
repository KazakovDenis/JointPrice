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
    'batteries': 'xls'
}

# all_product_parameters[parameter][supplier] = supplier's tag title in XML
all_product_parameters = {
    # common parameters
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
    'selling_price': {'rus': 'Цена продажи', 'sak': None},
    'low_price': {'rus': 'Цена для своих', 'sak': None},
    'description': {'rus': 'Описание', 'sak': None},
    'origin': {'rus': 'Происхождение', 'svrauto': 'SGOODLAND', 'sak': None},
    'manufacturer': {'rus': 'Производитель', 'sak': None},
    'weight': {'rus': 'Масса', 'sak': None},
    'length': {'rus': 'Длина', 'svrauto': 'SLENGTH'},
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
    'truck_width': {'rus': 'Ширина', 'svrauto': 'STIREWIDTH'},
    'truck_height': {'rus': 'Высота профиля', 'svrauto': 'STIRERATIO'},
    'truck_diameter': {'rus': 'Диаметр', 'svrauto': 'STIREDIAM'},
    'axis': {'rus': 'Ось', 'svrauto': 'STIREAXLE'},
    'tube': {'rus': 'Камерность', 'svrauto': 'STIRETUBE'},
    'layer': {'rus': 'Слойность', 'svrauto': 'SLAYER'},
    'type': {'rus': 'Тип', 'svrauto': 'SUSETYPE'},
    'restored': {'rus': 'Восстановленность', 'svrauto': 'SRETREAD'},
    # car & truck rims
    'holes': {'rus': 'Количество отверстий', 'svrauto': 'SHOLESQUANT', 'pwrs': 'bolts_count'},
    'PCD': {'rus': 'PCD', 'svrauto': 'SPCD', 'pwrs': 'bolts_spacing'},
    'offset': {'rus': 'Вылет', 'svrauto': 'SWHEELOFFSET', 'pwrs': 'et'},
    'dia': {'rus': 'Центральное отверстие', 'svrauto': 'SDIA', 'pwrs': 'dia'},
    'color': {'rus': 'Цвет', 'svrauto': 'SCOLOR', 'pwrs': 'color'},
    'rim_type': {'rus': 'Тип', 'svrauto': 'STYPE', 'pwrs': 'rim_type'},
    'treatment': {'rus': 'Обработка', 'svrauto': 'SPROCESSWAY', 'pwrs': None},
    'for_car': {'rus': 'Назначение', 'svrauto': 'SAUTOLIST', 'pwrs': None},
    # fasteners
    'fast_type': {'rus': 'Тип крепежа', 'svrauto': 'SFIXTYPE'},
    'outer_diam': {'rus': 'Внешний диаметр', 'svrauto': 'SOUTDIAMRING'},
    'inner_diam': {'rus': 'Внутренний диаметр', 'svrauto': 'SINDIAMRING'},
    'nut_height': {'rus': 'Высота гайки', 'svrauto': 'SHEIGHTNUT'},
    'thread_diam': {'rus': 'Диаметр резьбы', 'svrauto': 'STHREADIAM'},
    'thread_length': {'rus': 'Длина резьбы', 'svrauto': 'STHREADLENGTH'},
    'key_size': {'rus': 'Размер под ключ', 'svrauto': 'SKEYSIZE'},
    'fast_shape': {'rus': 'Форма сопряжения', 'svrauto': 'SSHAPE'},
    'fast_pitch': {'rus': 'Шаг резьбы', 'svrauto': 'SPITCH'},
    # secrets
    'lock_type': {'rus': 'Тип секретки', 'svrauto': 'SLOCKSTYPE'},
    'thread_step': {'rus': 'Шаг резьбы', 'svrauto': 'SSTEP'},
    'head_size': {'rus': 'Размер головки', 'svrauto': 'SHEADSIZE'},
    'head_form': {'rus': 'Форма головки', 'svrauto': 'SHEADFORM'},
    # batteries
    'capacity': {'rus': 'Ёмкость', 'sak': None},
    'polarity': {'rus': 'Полярность', 'sak': None},
    'current': {'rus': 'Пусковой ток', 'sak': None},
    'voltage': {'rus': 'Номинальное напряжение', 'sak': None},
    'dimensions': {'rus': 'Габариты', 'sak': None},
    'cleats': {'rus': 'Тип клемм', 'sak': None},
}

suppliers = [svrauto, pwrs, trektyre, sak]
applied_sa_addresses = ('Твардовского/3', 'Шамшиных', 'Фабричная93', 'Кирова232', 'Ипподромск')
