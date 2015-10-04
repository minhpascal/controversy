# -*- coding: utf-8 -*-
"""
    Controversy --- app.py 
    ~~~~~~~~~~~~~~~~~~~~~~

    Controversy: joint mining of news text and social media to discover controversial points in news.
    
    Runs server.

    :copyright: (c) 2015 |contributors|.
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, session, redirect, render_template, request, Blueprint, flash, abort, url_for
from jinja2 import TemplateNotFound
from functools import wraps
from api import api
from config import *
from datetime import datetime
from hashlib import md5
import db
import forms


app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.secret_key = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = CAPTCHA_PUBLIC
app.config['RECAPTCHA_PRIVATE_KEY'] = CAPTCHA_PRIVATE
app.config['testing'] = DEBUG
app.config['version'] = 'v0.2'


# from Yishen Chen: github.com/dsrcl
def digest(static):
    with open('static/%s' % static) as f:
        return "%s?v=%s" % (url_for('static', filename=static), md5(f.read()).hexdigest())


@app.errorhandler(500)
def handle_500(error):
    app.logger.exception(error)
    import twilio
    from twilio.rest import TwilioRestClient
    from flask import jsonify
    from error import UsageError
    client = TwilioRestClient(TWILIO_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(body="problem on Linode: %s" % repr(error), to=ADMIN_PHONE, from_="+19089982913")
    raise UsageError('our-fault', status_code=500)


def loggedin():
    return session.get('username') is not None


def require_login(view):
    @wraps(view)
    def protected_view(*args, **kwargs):
        if loggedin():
            return view(*args, **kwargs)
        else:
            return redirect('/login')
    return protected_view


@app.route('/login/<username>', methods=['GET', 'POST'])
@app.route("/login", defaults={'username': None}, methods=['GET', 'POST'])
def login(username):
    if loggedin():
        return redirect('/')
    
    form = forms.Login()
    if form.validate_on_submit():
        session['username'] = form.username
        session['user'] = db.dump_user(form.username)
        return redirect('/')
    return render_template('login.html', title='Login', form=form, css=digest("login.css"), username=username or '')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        flash("thanks, %s; please confirm your password" % first_name(form.name.data))
        return redirect('login/%s' % form.username)
    return render_template('register.html', title='Register', form=form, css=digest('login.css'), logged_in = loggedin())


@app.route("/logout")
@require_login
def logout():
    u = session['username']
    session.pop('username', None)
    session.pop('user', None)
    flash("%s, you were logged out" % u)
    return redirect('/login')


@app.route("/account", methods=['GET', 'POST'])
@require_login
def account():
    form = forms.Login()
    if form.validate_on_submit():
        db.drop_account(session['username'])
        flash("Account destroyed with vengeance!")
        return logout()

    return render_template('account.html',
                           user=session['user'],
                           angular='Account',
                           js='static/account.js',
                           history=db.user_history(session['username']),
                           css=digest('account.css'),
                           form=form,
                           version=app.config['version'])


@app.route("/account/clear-queries")
@require_login
def clear_queries():
    db.clear_queries(session['username'])
    return redirect('account')

    
@app.route("/html/<path>")
@require_login
def serve_ang(path):
    try:
        return render_template('partials/%s' % path, user=session['user'])
    except TemplateNotFound:
        return abort(404)


@app.route("/")
@require_login
def index():
    return render_template('app.html',
            user=session['user'],
            css=digest('app.css'),
            js=digest('home.js'),
            angular='Home')


@app.route("/not-supported")
def not_supported():
    return render_template('not-supported.html')


@app.template_filter('first_name')
def first_name(s):
    return s.split(' ')[0]


@app.template_filter('pretty_date')
def pretty_date(u):
    return datetime.strptime(u, db.mysql_date()).strftime("%A, %d %B")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4040, debug=DEBUG)
