#!/usr/bin/env python
# coding=utf8
from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    request,
    url_for,
    abort
)

from flask.ext.lwadmin.navbar import create_navbar_fd
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
    from lightningwolf_smp.utils.user import get_user
    user = get_user(id)
    if user is None:
        abort(404)

    if request.method == 'GET':
        form = FormUserEdit(
            email=user.email,
            perm=user.get_perm()
        )

    if request.method == 'POST':
        form = FormUserEdit()
        form.setId(user.get_id())
        if form.validate_on_submit():
            from lightningwolf_smp.utils.user import edit_user
            rs = edit_user(
                user=user,
                email=form.data['email'],
                password=form.data['password'],
                credential=form.data['perm']
            )
            if rs is True:
                flash(u'User `%s` data changed' % user.get_username(), 'success')
                return redirect(url_for('user.user_list'))
            else:
                flash(u'An error occurred while updating the user', 'error')

    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template('user/edit.html', lw_navbar=navbar, form=form, user=user)


@user.route('/admin/user/<int:id>/delete', methods=["POST"])
@admin_permission.require(http_exception=403)
def user_del(id):
    from lightningwolf_smp.utils.user import get_user
    user = get_user(id)
    if user is None:
        abort(404)
    user.delete()
    return redirect(url_for('user.user_list'))