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


domain = Blueprint('domain', __name__)


user_permission = app_permissions['user']
admin_permission = app_permissions['admin']


@domain.route("/admin/domain/list", methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
def domain_list():
    from lightningwolf_smp.models.domain import DomainPager
    from lightningwolf_smp.blueprints.configs.domain import configuration
    page = request.args.get('page', 1)
    pager = DomainPager(page=page)
    pager.initialize(configuration=configuration)

    navbar = create_navbar_fd(navbar_conf, 'key.domain.domain_list')
    return render_template(
        'domain/list.html',
        lw_navbar=navbar,
        page=page,
        pager=pager,
        configuration=configuration
    )


@domain.route('/admin/domain/create', methods=["GET", "POST"])
@login_required
@admin_permission.require(http_exception=403)
def domain_create():
    pass