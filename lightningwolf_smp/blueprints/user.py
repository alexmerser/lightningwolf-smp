#!/usr/bin/env python
# coding=utf8
from flask import Blueprint, render_template
from flask.ext.login import login_required
from flask.ext.lwadmin import create_navbar_fd
from lightningwolf_smp.application import app_permissions, navbar_conf


user = Blueprint('user', __name__)


user_permission = app_permissions['user']
admin_permission = app_permissions['admin']


@user.route("/user", methods=["GET"])
@user_permission.require(http_exception=403)
def user_page():
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_page')
    return render_template('user/user.html', lw_navbar=navbar)


@user.route('/user/list', methods=["GET"])
@admin_permission.require(http_exception=403)
def user_list():
    from lightningwolf_smp.utils.user import get_user_list
    users = get_user_list()
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/list.html', lw_navbar=navbar, list=users)

@user.route('/user/create', methods=["GET", "POST"])
@admin_permission.require(http_exception=403)
def user_create():
    from lightningwolf_smp.forms.user import FormUserAdd
    form = FormUserAdd()
    if form.validate_on_submit():
        from lightningwolf_smp.utils.user import create_user
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/create.html', lw_navbar=navbar, form=form)
