#!/usr/bin/env python
# coding=utf8
from flask_wtf import Form
from wtforms import fields, validators


from lightningwolf_smp.application import sentry, db
from lightningwolf_smp.models import User


class LoginForm(Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError(u'Bad login or password')

        if not user.is_correct_password(self.password.data):
            raise validators.ValidationError(u'Bad login or password')

    def get_user(self):
        return db.session.query(User).filter_by(username=self.login.data).first()
