# -*- coding: utf-8 -*-
"""
    Controversy --- app.py 
    ~~~~~~~~~~~~~~~~~~~~~~

    Controversy: joint mining of news text and social media to discover controversial points in news.
    
    Runs server.

    :version: 0.3
    :copyright: (c) 2015 I Lourentzou, G Dyer, A Sharma, C Zhai. Some rights reserved.
    :license: CC BY-NC-SA 4.0, see LICENSE for more details.
"""
from flask import Flask, session, redirect, render_template, request, Blueprint, flash, abort
from jinja2 import TemplateNotFound
from functools import wraps
from api import api
from mturk import mturk 
from config import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
import db
import forms
from digest import digest


application = Flask(__name__)

application.register_blueprint(api, url_prefix='/api')
application.register_blueprint(mturk, url_prefix='/training')
application.secret_key = SECRET_KEY

application.config['RECAPTCHA_PUBLIC_KEY'] = CAPTCHA_PUBLIC
application.config['RECAPTCHA_PRIVATE_KEY'] = CAPTCHA_PRIVATE
application.config['version'] = 'v0.3'
application.config['testing'] = DEBUG


def get_added_styles():
    webkit = digest('webkit.css') if session.get('webkit') == 'webkit' else None
    safari = digest('safari.css') if session.get('safari') == 'safari' else None
    return webkit, safari


@application.errorhandler(500)
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


@application.route('/bourbaki')
def bourbaki():
    username = 'bourbaki@illinois.edu'
    session['username'] = username
    session['user'] = db.dump_user(username)
    return redirect('/')


@application.route('/login/<username>', methods=['GET', 'POST'])
@application.route("/login", defaults={'username': None}, methods=['GET', 'POST'])
def login(username):
    if loggedin():
        return redirect('/')
    
    form = forms.Login()
    if form.validate_on_submit():
        session['username'] = form.username
        session['user'] = db.dump_user(form.username)
        return redirect('/')
    return render_template('login.html',
                           title='Login',
                           form=form,
                           css=digest('login.css'),
                           username=username or '')


@application.route("/set_webkit")
def set_webkit():
    session['webkit'] = 'webkit'
    return 'yes'


@application.route("/set_safari")
def set_safari():
    session['safari'] = 'safari'
    return 'yes'


@application.route("/register", methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        flash("thanks, %s; please confirm your password" % first_name(form.name.data))
        return redirect('login/%s' % form.username)
    return render_template('register.html',
                           title='Register',
                           form=form,
                           css=digest('login.css'),
                           logged_in = loggedin())


@application.route("/logout")
@require_login
def logout():
    u = session['username']
    session.pop('username', None)
    session.pop('user', None)
    flash("%s, you were logged out" % u)
    return redirect('/login')


@application.route("/account", methods=['GET', 'POST'])
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
                           version=application.config['version'])


@application.route("/account/forget")
@require_login
def clear_queries():
    db.clear_queries(session['username'])
    return redirect('account')

    
@application.route("/partial/<path>")
@require_login
def serve_ang(path):
    try:
        return render_template('partials/%s' % path, user=session['user'])
    except TemplateNotFound:
        return abort(404)


@application.route("/")
@require_login
def index():
    """all pages for the app are loaded through here.
    Angular handles partials, which are rendered through ``/partial``
    """
    webkit, safari = get_added_styles()
    return render_template('app.html',
            user=session['user'],
            safari=safari,
            webkit=webkit,
            css=digest('app.css'),
            js=digest('home.js'),
            angular='Home')


@application.route("/not-supported")
def not_supported():
    return render_template('not-supported.html')


@application.template_filter('first_name')
def first_name(s):
    return s.split(' ')[0]


def clean_rd(rd):
    """relative delta --> nice string
    """
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    res = []
    res_append = res.append
    for a in attrs:
        if getattr(rd, a) and getattr(rd, a) > 1:
            res_append('%d %s' % (getattr(rd, a), a))
    return res[0] if len(res) else 'a second'


@application.template_filter('pretty_date')
def pretty_date(u):
    """mysql timestamp --> nice strftime + " ... ago"
    """
    now = datetime.fromtimestamp(time.time())
    then_secs = (u - datetime(1970, 1, 1)).total_seconds()
    then = datetime.fromtimestamp(then_secs)
    delta = clean_rd(relativedelta(now, then))
    return '%s ago' % delta, then.strftime('%A, %d %B')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=4040, debug=DEBUG)
