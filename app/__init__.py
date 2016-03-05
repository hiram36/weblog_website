# -*- coding:utf8 -*-

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import Config


weblogapp = Flask(__name__)
weblogapp.config.from_object('config.DevelopmentConfig')
TRACK_MODIFICATIONS = weblogapp.config.setdefault('config.Config.SQLALCHEMY_TRACK_MODIFICATIONS', True)

pgdb = SQLAlchemy(weblogapp)

login_mgr = LoginManager()
login_mgr.init_app(weblogapp)
openid = OpenID(weblogapp, os.path.join(Config.BASE_DIR, 'tmp'))

#login_mgr.login_view = 'login'
login_mgr.login_view = 'create_profile'

from app import views, models


if __name__ ==  '__main__':
    weblogapp.run(host='0.0.0.0', port=8888, debug = True)
