# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from collections import Counter
from threading import Thread
from flask import render_template, request
from jointprices import app
from models import CarTire, CarRim, TruckRim, TruckTire, Battery
from config import all_product_parameters as aprp
from manage import update_db_entirely
from forms import *


@app.route('/')
def index():
    return render_template('index.html')


category_form = {
    'car-tires': (CarTire, CarTireSearch),
    'car-rims': (CarRim, CarRimSearch),
    'truck-tires': (TruckTire, TruckTireSearch),
    'truck-rims': (TruckRim, TruckRimSearch),
    'batteries': (Battery, BatterySearch)
}


@app.route('/search/<category>', methods=['POST', 'GET'])
def search(category):
    try:
        model = category_form[category][0]
        form = category_form[category][1]()
    except KeyError:
        return render_template('404.html'), 404

    if request.method == 'POST':
        params = dict()
        for field in get_fields(form):
            value = request.form.get(f'{field}') if field != 'secret' else None
            if value and 'None' not in value:
                params[field] = int(value) if value.isdigit() else value
        if params:
            # extracting records from db
            found_by_art = model.query.filter(model.article.contains(str(params.pop('article')))).all()\
                            if params.get('article') else None
            found_by_price = model.query.filter(model.purchase_price <= params.pop('price')).all()\
                            if params.get('price') else None
            found_by_count = model.query.filter(model.count >= params.pop('count')).all() if params.get('count') else None
            found_list = [item for item in (found_by_art, found_by_price, found_by_count) if item]

            # getting common items
            common_items = None
            if len(found_list) > 0:
                for i in range(len(found_list)):
                    if i == 0:
                        common_items = Counter(found_list[0])
                    else:
                        common_items &= Counter(found_list[i])
            found_by_other = model.query.filter_by(**params).order_by(model.purchase_price).all()
            found = list((common_items & Counter(found_by_other)).elements()) if common_items else found_by_other

            # grouping products by article
            articles = set([product.__dict__.get('article') for product in found])
            filtered = [item for item in [list(filter(lambda x: x.article == article, found)) for article in articles]
                        if item]
        else:
            filtered = None
        secret = request.form.get('secret')    # for hiding the purchase price from prying eyes
        return render_template('search.html', form=form, products=filtered, category=category, secret=secret)

    return render_template('search.html', form=form, category=category, GET=True)


@app.route('/<category>/<db_id>')
def render_product(category=None, db_id=None):
    model = category_form[category][0]
    product = model.query.filter_by(id=db_id).first_or_404()
    offers = model.query.filter_by(article=product.article).all()
    main_params = (product.title, product.img, product.count, product.updated, product.supplier, product.purchase_price,
                   product.retail_price, product.selling_price, product.low_price, product.id, product.address,
                   product._sa_instance_state, product.category)
    return render_template('product.html', product=product, main_params=main_params, titles=aprp, offers=offers)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404


@app.route('/update')
def update():
    Thread(target=update_db_entirely()).start()
