# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import render_template, request
from jointprices import app
from models import CarTire, Product
from config import all_product_parameters as aprp
from forms import *


@app.route('/')
def index():
    return render_template('index.html')


category_form = {
    'car-tires': CarTireSearch,
    'car-rims': CarRimSearch,
    'truck-tires': TruckTireSearch,
    'truck-rims': TruckRimSearch,
    'batteries': BatterySearch
}


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
            value = request.form.get(f'{field}') if field != 'secret' else None
            if value and 'None' not in value:
                params[field] = int(value) if value.isdigit() else value
        # hiding the purchase price from prying eyes
        secret = request.form.get('secret')
        found = CarTire.query.filter_by(**params).all()
        # grouping products by article
        articles = set([product.__dict__.get('article') for product in found])
        filtered = [list(filter(lambda x: x.article == article, found)) for article in articles]
        return render_template('search.html', form=form, products=filtered, secret=secret)

    return render_template('search.html', form=form)


@app.route('/products/<slug>')
def render_product(slug=None):
    product = CarTire.query.filter_by(id=slug).first_or_404()
    main_params = [product.title, product.img, product.count, product.updated, product.supplier, product.purchase_price,
                   product.retail_price, product.selling_price, product.low_price, product.id, product.address,
                   product._sa_instance_state, product.category]
    return render_template('product.html', product=product, main_params=main_params, titles=aprp)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
