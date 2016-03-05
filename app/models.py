# -*- coding:utf8 -*-
from app import pgdb
import datetime

class UcUsers(pgdb.Model):

    __tablename__ = 'uc_users'

    id = pgdb.Column(pgdb.Integer, primary_key = True)
    nickname = pgdb.Column(pgdb.String(64), index = True, unique = True)
    email = pgdb.Column(pgdb.String(120), index = True, unique = True)
    posts = pgdb.relationship('Post', backref='author', lazy='dynamic')
    gmt_create = pgdb.Column(pgdb.DateTime)
    gmt_modify = pgdb.Column(pgdb.DateTime)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_userid(self):
        return str(self.id)


    def __repr__(self):
        return '<User %r>' % (self.nickname)



class Post(pgdb.Model):
 
    __tablename__ = 'post'

    id = pgdb.Column(pgdb.Integer, primary_key = True)
    user_id = pgdb.Column(pgdb.Integer, pgdb.ForeignKey('uc_users.id'))
    body = pgdb.Column(pgdb.String(140))
    gmt_create = pgdb.Column(pgdb.DateTime)
    gmt_modify = pgdb.Column(pgdb.DateTime)

    def __repr__(self):
        return '<Post %r>' % (self.body)
