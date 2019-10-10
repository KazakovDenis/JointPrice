# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import render_template, request, flash
from jointprices import app
from models import CarTire
from forms import *


category_form = {
    'car-tires': CarTireSearch,
    'car-rims': CarRimSearch,
    'truck-tires': TruckTireSearch,
    'truck-rims': TruckRimSearch,
    'batteries': BatterySearch
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/', methods=['POST', 'GET'])
@app.route('/search/<category>', methods=['POST', 'GET'])
def search(category='car-tires'):
    try:
        form = category_form[category]()
    except KeyError:
        return render_template('404.html'), 404
    if request.method == 'POST':
        params = dict()
        for field in get_fields(form):
            value = request.form.get(f'{field}')
            if value and 'None' not in value:
                params[field] = int(value) if value.isdigit() else value
        found = CarTire.query.filter_by(**params).all()
        print(params, '\n', found)
        return render_template('search.html', form=form, products=found)

    return render_template('search.html', form=form)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
