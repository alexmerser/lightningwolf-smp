#!/usr/bin/env python
# coding=utf8
from flask import Blueprint, render_template
from flask.ext.login import login_required
from flask.ext.lwadmin.navbar import create_navbar_fd
from lightningwolf_smp.application import app_permissions, navbar_conf


main = Blueprint('main', __name__)


user_permission = app_permissions['user']
admin_permission = app_permissions['admin']


@main.route('/')
@main.route('/index')
@login_required
def main_page():
    navbar = create_navbar_fd(navbar_conf)
    return render_template('main/index.html', lw_navbar=navbar)


@main.route("/admin", methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
def admin_page():
    navbar = create_navbar_fd(navbar_conf, 'key.main.admin_page')
    return render_template('main/admin.html', lw_navbar=navbar)
