#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'

from flask import (
    redirect,
    url_for,
    flash,
    render_template,
    g
)

from lightningwolf_smp.application import app
from lightningwolf_smp.blueprints.main import main
from lightningwolf_smp.blueprints.login import login
from lightningwolf_smp.blueprints.user import user
from lightningwolf_smp.blueprints.domain import domain


"""Blueprints"""
app.register_blueprint(main)
app.register_blueprint(login)
app.register_blueprint(user)
app.register_blueprint(domain)


@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login.login_page'))


@app.errorhandler(403)
def authorisation_failed(e):
    flash(
        (
            'Your current identity is {id}. You need special privileges to access this page'
        ).format(id=g.identity.user.username)
    )

    return redirect(url_for('login.login_page'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('jqueryuibootstrap_404.html', error=error), 404


def main():
    app.run()
