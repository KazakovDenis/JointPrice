# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from wtforms import Form, StringField, BooleanField, SelectField
from jointprices import db
from models import CarTire
from config import suppliers


def get_fields(form):
    return [i for i in form.__dict__ if '_' not in i]


class ProductForm(Form):
    article = StringField('Артикул')
    _supplier_choices = [(None, 'Все')] + [(supplier['title'], supplier['title']) for supplier in suppliers]
    supplier = SelectField('Поставщик', choices=_supplier_choices)
    secret = BooleanField('@', false_values=('false', 'None', None, False))
    count = StringField('Количество')
    price = StringField('Макс цена')


class CarTireSearch(ProductForm):
    _brand_choices = [(None, 'Все')] + [(item[0], item[0]) for item in db.session.query(CarTire.brand).distinct().all()]
    brand = SelectField('Марка', choices=_brand_choices)
    width = StringField('Ширина')
    height = StringField('Профиль')
    diameter = StringField('Диаметр')
    season = SelectField('Сезон', choices=[(None, 'Любой'), ('зимняя', 'Зимняя'), ('летняя', 'Летняя'),
                                           ('всесезонная', 'Всесезонная')])
    stud = SelectField('Шипы', choices=[(None, 'Не важно'), ('шипованная', 'Есть'), ('нешипованная', 'Нет')])


class CarRimSearch(ProductForm):
    pass


class TruckTireSearch(ProductForm):
    pass


class TruckRimSearch(ProductForm):
    pass


class BatterySearch(ProductForm):
    pass
