#!flask/bin/python
# -*- coding:utf8 -*-

from app import weblogapp

weblogapp.run(host='0.0.0.0', port=8888, debug = True)
