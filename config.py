# -*- coding:utf8 -*-

import os


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    DEBUG = True
    TESTING = True

    OPENID_PROVIDERS = [
        #{ 'name': 'Google', 'url': 'https://www.google.com/accounts/o8id' },
        #{ 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
        #{ 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
        #{ 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
        { 'name': 'MyOpenID', 'url': 'https://www.weblog.com/joel_shen' }]

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'postgresql://weblogadmin:pgsql123@localhost:1921/weblogdb'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')

    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = True

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True
