#!/usr/bin/env python
# coding=utf8
from flask import Blueprint, request, redirect, render_template, url_for, session, current_app
from flask.ext.login import login_user, logout_user
from flask.ext.principal import Principal, Identity, AnonymousIdentity, identity_changed
from lightningwolf_smp.forms.login import LoginForm


login = Blueprint('login', __name__)


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
