#!/usr/bin/env python
# coding=utf8
"""Lightningwolf Server Management Panel

Usage:
  smp.py start
  smp.py init:config
  smp.py init:db
  smp.py user:create <username> <useremail> <userpass>
  smp.py (-h | --help)
  smp.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from flask import (
    request,
    Response,
    send_from_directory,
    redirect,
    url_for,
    flash,
    g,
    render_template)

from lightningwolf_smp.application import app
from lightningwolf_smp.blueprints import login


"""Blueprints"""
app.register_blueprint(login)


@app.route('/')
@app.route('/index')
def index_page():
    return redirect(url_for('login.login_page'))


@app.errorhandler(401)
def authentication_failed(e):
    flash('Authenticated failed.')
    return redirect(url_for('login.login_page'))


@app.errorhandler(403)
def authorisation_failed(e):
    flash(('Your current identity is {id}. You need special privileges to access this page').format(id=g.identity.user.login))

    return redirect(url_for('login.login_page'))

if '__main__' == __name__:
    __version__ = app.config['VERSION']
    arguments = docopt(__doc__, version=__version__)
    if arguments['start']:
        app.run()
    if arguments['init:config']:
        print(arguments)
    if arguments['init:db']:
        from lightningwolf_smp.application import db
        from lightningwolf_smp.models import *
        # db.drop_all()
        db.create_all()
        print "Tables in Database created"
    if arguments['user:create']:
        import uuid
        import hashlib
        import json
        import bcrypt

        from lightningwolf_smp.application import db
        from lightningwolf_smp.models import User

        password = arguments['<userpass>']
        salt = hashlib.md5(str(uuid.uuid4())).hexdigest()
        salted = hashlib.sha512(password + salt).hexdigest()
        hashed = bcrypt.hashpw(salted, bcrypt.gensalt(12))

        admin_permisions = {
            'role': ['admin', 'user']
        }
        user = User(
            username=arguments['<username>'],
            email=arguments['<useremail>'],
            salt=salt,
            password=hashed,
            permissions=json.dumps(admin_permisions, indent=4, sort_keys=True)
        )
        db.session.add(user)
        db.session.commit()

        print "User created"
