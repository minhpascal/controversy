# -*- coding: utf-8 -*-
from flask import url_for
from hashlib import md5
def digest(static):
    with open('static/%s' % static) as f:
        return "%s?v=%s" % (url_for('static', filename=static), md5(f.read()).hexdigest())
