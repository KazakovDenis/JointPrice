# -*- coding: utf-8 -*-
# https://github.com/KazakovDenis
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
app.config.from_object(Configuration)
app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
