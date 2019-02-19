#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol
from app import db, app

if __name__ == "__main__":
    admin = Admin.query.filter_by(name='imoocmovie').first()
    from werkzeug.security import generate_password_hash

    admin.pwd = generate_password_hash('123456')
    db.session.add(admin)
    db.session.commit()
