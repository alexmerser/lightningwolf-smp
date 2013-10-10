#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db
from flask import session
from flask_lwadmin.pager import Pager


class Domain(db.Model):
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    domain_name = db.Column(db.String(255), unique=True, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', backref=db.backref('domain', lazy='dynamic'))

    def __repr__(self):
        return '<Domain %r>' % self.domain_name

    def __unicode__(self):
        return self.domain_name


def get_domain(domain_id):
    return db.session.query(Domain).get(domain_id)


class DomainPager(Pager):
    def __init__(self, max_per_page=10, page=1):
        Pager.__init__(self, max_per_page=max_per_page, page=page)
        self.filter_data = {}

    def initialize(self, configuration):
        # TODO: filter_data in this moment is get in blueprint for configuration too!
        self.filter_data = get_domain_filters()
        self.set_count(get_domain_list_count(self.filter_data))
        Pager.initialize(self, configuration)

    @staticmethod
    def get_pk():
        return 'id'

    def get_results(self):
        if self.results is None:
            self.results = get_domain_list(self.filter_data, offset=self.get_offset(), limit=self.get_limit())

        return self.results


def get_domain_list(filter_data, offset=0, limit=100):
    query = db.session.query(Domain)
    if 'domain_name' in filter_data:
        if filter_data['domain_name'] is not None:
            query = query.filter(Domain.domain_name.like('%' + filter_data['domain_name'] + '%'))
    return query.offset(offset).limit(limit)


def get_domain_list_count(filter_data):
    query = db.session.query(Domain)
    if 'domain_name' in filter_data:
        if filter_data['domain_name'] is not None:
            query = query.filter(Domain.domain_name.like('%' + filter_data['domain_name'] + '%'))
    return query.count()


def get_domain_filters():
    if 'filter.domain' in session:
        return session['filter.domain']
    else:
        return {"domain_name": None}


def set_domain_filters(filter_data):
    session['filter.domain'] = filter_data
