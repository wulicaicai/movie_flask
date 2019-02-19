#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '92f52240955c4618ac62b2fafd8b0b24'  # 设置CSRF
app.config['REDIS_URL']='redis://localhost:6379/0'
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/')
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/users/')
app.debug = False  # 开启调试模式
db = SQLAlchemy(app)
rd = FlaskRedis(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
