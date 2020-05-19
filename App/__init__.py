# -*- coding: utf-8 -*-
__author__ = 'xiejdm'


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object("config")
app.config['JSON_AS_ASCII'] = False     # 设置不显示的是utf-8编码，直接显示中文
db = SQLAlchemy(app)
restless = APIManager(app, flask_sqlalchemy_db=db)

from App import models, route
