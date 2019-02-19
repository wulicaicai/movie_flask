#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm

from app import app
from flask_script import Manager

manage = Manager(app)

if __name__ == "__main__":
    app.run()
    