# -*- coding: utf-8 -*-
"""
    app.py
    ~~~~~~

    Controversy, joint mining of news text and social media to discover controversial points in news. Runs server.

    :copyright: (c) 2015 Ismini Lourentzou, Graham Dyer, Lisa Huang.
    :license: BSD, see LICENSE for more details.
    :author: Graham Dyer
"""
from flask import Flask, session, redirect, render_template, request, Blueprint, flash
from functools import wraps
from api import api
import db, random
from config import *
from form import *
app = Flask(__name__)


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


def genpage(title, unique, css=[], js=[], angular=''):
    return render_template("%s.html" % title,
        page =
            {
                "title" : title,
                "custom_css" : map(lambda x: "%s.css" % x, css),
                "custom_js" : map(lambda x: "%s.js" % x, js),
                "angular" : angular
            },
        unique = unique
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if loggedin():
        return redirect('/')
    from_register = request.args.get('e')

    unique = {
        'login_details' : ('''Please log in or <a href='register'>create a free account</a>''' if not from_register else '''Thanks; log in with your new credentials!''')
    }

    if from_register:
        unique['email'] = request.args.get('e')
    if request.method == 'GET':
        redirect_url = request.args.get('redirect', '/')
        unique['redirect_url'] = redirect_url
    else:
        username = request.form['username']
        password = request.form['password']
        if not db.verify_user(username, password):
            unique.update({
                'login_details' : '''Authentication failed! Please <a href="register">get a free account</a> or try again.''',
                'extra_class' : 'warning',
                'email' : request.form['username']
            })
        else:
            session['username'] = username
            return redirect('/')
    return genpage("Login", unique, css=["login"])


@app.route("/register", methods=['GET', 'POST'])
def getaccount():
    #: see form.py
    unique = LOGIN

    if request.method == 'POST':
        m = None
        if any(len(res) not in range(3,50) for res in request.form.values()):
            m = 'Ensure proper inputs!'    
        elif db.user_exists(request.form['Id']):
            m = '''That user already exists; try <a href="../login?e=%s">logging in</a> if it's you!''' % (request.form['Id'])
        elif ' ' not in request.form['Name']:
            m  = 'Please enter your full name'
        else:
            db.create_user(request.form)
            return redirect('login?e=%s' % request.form['Id'])
        unique.update({
                'register_message' : m,
                'extra_class' : 'warning',
                'name' : request.form['Name'],
                'password' : request.form['Password'],
                'school' : request.form['School']
            })

    #: get
    unique['logged_in'] = loggedin()
    return genpage('Register', unique, css=['login'])


@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("you were logged out")
    return redirect('/login')


@app.route('/html/<path>')
@require_login
def serve_ang(path):
    unique = db.dump_user(session['username'])
    return render_template('partials/%s' % path, unique=unique)


@app.route("/")
@require_login
def index():
    unique = db.dump_user(session['username'])
    return genpage('App', unique, css=['home', 'cards'], js=['home'], angular='Home')


@app.template_filter('first_name')
def first_name(s):
    return s.split(' ')[0]


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.register_blueprint(api, url_prefix='/api')
    app.run(debug=True)
