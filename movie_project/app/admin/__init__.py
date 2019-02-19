#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm


from flask import Blueprint

admin = Blueprint('admin', __name__)

import app.admin.views
