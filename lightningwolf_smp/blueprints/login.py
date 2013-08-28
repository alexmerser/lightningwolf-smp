#!/usr/bin/env python
# coding=utf8


from flask import Blueprint, request, redirect, render_template, url_for, session, current_app
from flask.ext.login import login_user, logout_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed
from flask_wtf import Form
from wtforms import fields, validators

from lightningwolf_smp.application import sentry, db
from lightningwolf_smp.models import User


login = Blueprint('login', __name__)


# Define login and registration forms (for flask-login)
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


@login.route("/logout")
def logout_page():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('login.login_page'))


@login.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.get_user()

        # Keep the user info in the session using Flask-Login
        login_user(user)

        # Tell Flask-Principal the identity changed
        identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

        return redirect(request.args.get("next") or url_for('login.success_page'))

    return render_template('jqueryuibootstrap_login.html', form=form)

@login.route("/success", methods=["GET", "POST"])
def success_page():
    return render_template('success.html')
