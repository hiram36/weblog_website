# -*- coding:utf8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import weblogapp, pgdb, login_mgr, openid
from .forms import LoginForm
from .models import UcUsers
from datetime import datetime

# Set "homepage" to index.html
@weblogapp.route('/')
@weblogapp.route('/index')
def index():
    #return "Hello, PostgreSQL."
    #init_user = { 'nickname': 'PostgreSQL' } # fake user
    reg_user = g.user

    init_posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]

    return render_template("index.html", title="Welcome to WeBlog", user = reg_user, posts = init_posts )



@weblogapp.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        #flash('Login requested for OpenID="' + login_form.openid.data + '", remember_me=' + str(login_form.remember_me.data))
        session['remember_me'] = login_form.remember_me.data
        return openid.try_login(login_form.openid.data, ask_for=['nickname', 'email'])

    return render_template("login.html", title="Sign In page", form = login_form, providers = weblogapp.config['OPENID_PROVIDERS'] )

@weblogapp.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            db_session.add(UcUsers(name, email, session['openid']))
            db_session.commit()
            return redirect(openid.get_next_url())
    return render_template('create_profile.html', next=openid.get_next_url())



@openid.after_login
def create_or_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invaild login. Please try again.')
        return redirect(url_for('login'))

    register_user = UcUsers.query.filter_by(email=resp.email).first()
    if register_user is None:
        reg_nickname = resp.nickname
        if reg_nickname is None or reg_nickname == "":
            reg_nickname = resp.email.split('@')[0]

        register_user = UcUsers(nickname=reg_nickname, email=resp.email, gmt_create=datetime.now(), gmt_modify = datetime.now())
        pgdb.session.add(register_user)
        pgdb.session.commit()
    else:
        flash(u'Successfully signed in.')
        g.user = register_user
        return redirect(openid.get_next_url())

    remember_me = False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    login_user(register_user, remember = remember_me)
    #return redirect(request.args.get('next') or url_for('login'))
    return redirect(url_for('create_profile', next=openid.get_next_url(),nickname = resp.nickname, email=resp.email))


@login_mgr.user_loader
def load_user(id):
    return UcUsers.query.get(int(id))


@weblogapp.before_request
def lookup_current_user():
    g.user = current_user
 
    if 'openid' in session:
        openid = session['openid']
        g.user = UcUsers.query.filter_by(openid=openid).first()



@weblogapp.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out...')
    return redirect(openid.get_next_url())
