#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: wulicaicai
# IDE PyCharm

from flask import Blueprint

home = Blueprint('home', __name__)

import app.home.views
