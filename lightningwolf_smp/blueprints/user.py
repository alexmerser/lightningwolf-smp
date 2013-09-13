#!/usr/bin/env python
# coding=utf8
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    request,
    url_for
)

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


@user.route('/admin/user/list', methods=["GET"])
@admin_permission.require(http_exception=403)
def user_list():
    from lightningwolf_smp.utils.user import get_user_list
    users = get_user_list()
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/list.html', lw_navbar=navbar, list=users)

@user.route('/admin/user/create', methods=["GET", "POST"])
@admin_permission.require(http_exception=403)
def user_create():
    from lightningwolf_smp.forms.user import FormUserAdd
    form = FormUserAdd()
    if form.validate_on_submit():
        from lightningwolf_smp.utils.user import create_user
        rs = create_user(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password'],
            credential=form.data['perm']
        )
        if rs is True:
            flash(u'The new user is created', 'success')
            return redirect(url_for('user.user_list'))
        else:
            flash(u'An error occurred while creating the user', 'error')

    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/create.html', lw_navbar=navbar, form=form)

@user.route('/admin/user/<int:id>/edit', methods=["GET", "POST"])
@admin_permission.require(http_exception=403)
def user_edit(id):
    from lightningwolf_smp.forms.user import FormUserEdit

    if request.method == 'GET':
        from lightningwolf_smp.utils.user import get_user
        User = get_user(id)
        form = FormUserEdit(
            email=User.email,
            perm=User.get_perm()
        )

    # if form.validate_on_submit():
    #     from lightningwolf_smp.utils.user import create_user
    #     rs = create_user(
    #         username=form.data['username'],
    #         email=form.data['email'],
    #         password=form.data['password'],
    #         credential=form.data['perm']
    #     )
    #     if rs is True:
    #         flash(u'The new user is created', 'success')
    #         return redirect(url_for('user.user_list'))
    #     else:
    #         flash(u'An error occurred while creating the user', 'error')

    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/edit.html', lw_navbar=navbar, form=form, user=User)
