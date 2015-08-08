# -*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~
    Forms referenced in app.
"""
from flask_wtf import Form#, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
import db


class Register(Form):
    name = StringField('name', validators=[DataRequired()], description={'placeholder': "What's your name?"}) 
    email = StringField('email', validators=[DataRequired(), Email()], description={'placeholder': "What's your email address?"})
    school = StringField('school', validators=[DataRequired()]) 
    password = PasswordField('password', validators=[DataRequired()], description={'placeholder': "Simple password"})
    #recaptcha = RecaptchaField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.username = None

    def validate(self):
        #: have WTF do base validation
        rv = Form.validate(self)
        if not rv:
            return False

        username = self.email.data
        if ' ' not in self.name.data or any(map(lambda x: x.isdigit(), self.name.data)) or any(map(lambda x: len(x) < 2, self.name.data.split(' '))):
            self.name.errors.append("full name, please")
            return False

        if db.user_exists(username):
            self.email.errors.append("that user already exists!")
            return False

        db.create_user(username, self.name.data, self.password.data, self.school.data)
        self.username = username
        return True


class Login(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.username = None
    
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        username = self.email.data
        if not db.user_exists(username):
            self.email.errors.append('Unknown username!')
            return False

        if not db.verify_user(username, self.password.data):
            self.password.errors.append('Invalid password!')
            return False

        self.username = username
        db.logged_in(username)
        return True
