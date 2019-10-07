# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from jointprices import app
from flask import render_template, request
from config import svrauto, pwrs, trektyre
from models import PriceList, get_response


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # здесь будет обработка формы поиска
        return render_template('index.html')

    found = None
    return render_template('index.html', products=found)


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404
