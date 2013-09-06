#!/usr/bin/env python
# coding=utf8
"""Lightningwolf Server Management Panel

Usage:
  smp.py start
  smp.py init:config
  smp.py init:db
  smp.py user:create <username> <useremail> <userpass> [--credential=<C>]
  smp.py (-h | --help)
  smp.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --credential=C  The C credential [default: admin] (admin|user)

"""
from docopt import docopt

from flask import (
    redirect,
    url_for,
    flash,
    g)

from lightningwolf_smp.application import app
from lightningwolf_smp.blueprints import main
from lightningwolf_smp.blueprints import login


"""Blueprints"""
app.register_blueprint(main)
app.register_blueprint(login)


@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login.login_page'))


@app.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to access this page').format(id=g.identity.user.username))

    return redirect(url_for('login.login_page'))


def main():
    __version__ = app.config['VERSION']
    arguments = docopt(__doc__, version=__version__)
    if arguments['start']:
        app.run()
    else:
        from lightningwolf_smp.utils.console import parse_arguments
        parse_arguments(arguments)

if __name__ == '__main__':
    main()
