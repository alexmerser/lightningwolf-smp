#!/usr/bin/env python
# coding=utf8
import os


from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.jqueryuibootstrap import JqueryUiBootstrap
from flask.ext.lwadmin import LwAdmin
from flask.ext.lwadmin.navbar import Navbar
from flask.ext.login import LoginManager, current_user
from flask.ext.principal import (
    Principal, 
    Permission, 
    ActionNeed, 
    RoleNeed, 
    identity_loaded, 
    UserNeed)
from flask.ext.babel import Babel
from raven.contrib.flask import Sentry
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# Configuration Loader
app.config.from_object('lightningwolf_smp.Config')
envvar = 'LIGHTNINGWOLF_SETTINGS'
if os.environ.get(envvar, None):
    app.config.from_envvar(envvar)

# Babel
babel = Babel(app)

# Sentry
sentry = Sentry(app, dsn=app.config['SENTRY_DSN'])

# Debug Toolbar
toolbar = DebugToolbarExtension(app)

# SQLAlchemy handler
db = SQLAlchemy(app)


# Flask-Login
def init_login():
    login_manager = LoginManager()

    login_manager.login_view = "/login/"

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from lightningwolf_smp.models import User
        return db.session.query(User).get(user_id)

init_login()

# Flask-Principal

Principal(app, skip_static=True)

# Needs
admin_need = RoleNeed('admin')
user_need = RoleNeed('user')

# Permissions
user_permission = Permission(user_need)
user_permission.description = "User permission"
admin_permission = Permission(admin_need)
admin_permission.description = "Admin permission"

app_needs = {'admin': admin_need, 'user': user_need}
app_permissions = {'user': user_permission, 'admin': admin_permission}

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles():
            identity.provides.add(RoleNeed(role))

# Flask-JqueryUiBootstrap
JqueryUiBootstrap(app)

# LwAdmin
LwAdmin(app)

navbar_conf = {
    'brand': {'brand_name': 'SMP', 'brand_url': '/'},
    'permissions': app_permissions,
    'items': [
        {
            'key': 'key.user.user_list',
            'label': 'User',
            'url': 'user.user_list',
            'type': Navbar.URL_INTERNAL,
            'credential': 'admin'
        },
        {
            'key': 'key.domain.domain_list',
            'label': 'Domain',
            'url': 'domain.domain_list',
            'type': Navbar.URL_INTERNAL,
            'credential': 'admin'
        },
        {
            'key': 'key.main.admin_page',
            'label': 'Admin',
            'url': 'main.admin_page',
            'type': Navbar.URL_INTERNAL,
            'credential': 'admin'
        }
    ],
    'profile': [
        {
            'key': 'key.user.user_page',
            'label': current_user,
            'icon': 'icon-user',
            'url': 'user.user_page',
            'credential': 'user'
        },
        {
            'key': 'key.logout',
            'label': 'logout',
            'url': 'login.logout_page',
            'type': Navbar.URL_INTERNAL,
            'icon': 'icon-signout',
            'only_icon': True
        }
    ]
}
