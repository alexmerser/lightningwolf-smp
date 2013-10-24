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

from flask.ext.login import login_required
from flask.ext.lwadmin.navbar import create_navbar_fd
from lightningwolf_smp.application import app_permissions, navbar_conf


user = Blueprint('user', __name__)


user_permission = app_permissions['user']
admin_permission = app_permissions['admin']


@user.route("/user", methods=["GET"])
@login_required
@user_permission.require(http_exception=403)
def user_page():
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_page')
    return render_template('user/user.html', lw_navbar=navbar)


@user.route('/admin/user/list', methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
def user_list():
    from lightningwolf_smp.models.user import UserPager
    from lightningwolf_smp.blueprints.configs.user import configuration
    page = request.args.get('page', 1)
    pager = UserPager(page=page)
    pager.initialize(configuration=configuration)

    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template(
        'user/list.html',
        lw_navbar=navbar,
        page=page,
        pager=pager,
        configuration=configuration
    )


@user.route('/admin/user/filter', methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
def user_filter():
    from lightningwolf_smp.models.user import UserPager
    from lightningwolf_smp.blueprints.configs.user import configuration
    pager = UserPager(page=1)
    pager.initialize(configuration=configuration)

    action = request.args.get('action', '')
    if action == '_reset':
        from flask_wtf import Form
        form = Form()
    else:
        from lightningwolf_smp.forms.user import FormUsernameFilter
        form = FormUsernameFilter()

    if form.validate_on_submit():
        if action == '_reset':
            pager.reset_filter_data()
        else:
            pager.set_filter_data({'username': form.data['username']})
    else:
        flash(u'An error occurred in filter form', 'error')

    return redirect(url_for('user.user_list'))


@user.route('/admin/user/batch', methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
def user_batch():
    flash(u'Work in progress', 'error')
    return redirect(url_for('user.user_list'))


@user.route('/admin/user/create', methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def user_create():
    from lightningwolf_smp.forms.user import FormUserAdd
    form = FormUserAdd()
    if form.validate_on_submit():
        from lightningwolf_smp.models.user import create_user
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

    from lightningwolf_smp.blueprints.configs.user import configuration
    configuration['create']['form'] = form
    configuration['create']['url'] = url_for('user.user_create')
    configuration['create']['actions'][0]['url'] = url_for('user.user_list')
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template(
        'user/create.html',
        lw_navbar=navbar,
        configuration=configuration['create']
    )


@user.route('/admin/user/<int:user_id>/edit', methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def user_edit(user_id):
    from lightningwolf_smp.forms.user import FormUserEdit
    from lightningwolf_smp.models.user import get_user
    user_object = get_user(user_id)
    if user_object is None:
        abort(404)

    if request.method == 'GET':
        form = FormUserEdit(
            email=user_object.email,
            perm=user_object.get_perm()
        )

    if request.method == 'POST':
        form = FormUserEdit()
        form.setId(user_object.get_id())
        if form.validate_on_submit():
            from lightningwolf_smp.models.user import edit_user
            rs = edit_user(
                user=user_object,
                email=form.data['email'],
                password=form.data['password'],
                credential=form.data['perm']
            )
            if rs is True:
                flash(u'User `%s` data changed' % user_object.get_username(), 'success')
                return redirect(url_for('user.user_list'))
            else:
                flash(u'An error occurred while updating the user', 'error')

    from lightningwolf_smp.blueprints.configs.user import configuration
    configuration['update']['title'] = 'Edit User: {0}'.format(user_object.get_username())
    configuration['update']['form'] = form
    configuration['update']['url'] = url_for('user.user_edit', user_id=user_object.get_id())
    configuration['update']['actions'][0]['url'] = url_for('user.user_list')
    navbar = create_navbar_fd(navbar_conf, 'key.user.user_list')
    return render_template(
        'user/update.html',
        lw_navbar=navbar,
        configuration=configuration['update']
    )


@user.route('/admin/user/<int:user_id>/delete', methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
def user_del(user_id):
    from flask_wtf import Form
    from lightningwolf_smp.models.user import get_user
    user_object = get_user(user_id)
    if user_object is None:
        abort(404)
    form = Form()
    if form.validate_on_submit():
        user_object.delete()
    else:
        flash(u'An error occurred while deleting the user', 'error')

    return redirect(url_for('user.user_list'))