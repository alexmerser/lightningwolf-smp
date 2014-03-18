#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models import Base
from lightningwolf_smp.application import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from flask import (
    url_for
)

from flask_lwadmin.pager import Pager

filter_display = ['domain_name']


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, nullable=True)
    domain_name = Column(String(255), unique=True, nullable=False)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('domain', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return '<Domain %r>' % self.domain_name

    def __unicode__(self):
        return self.domain_name

    def set_edit_button(self, pre):
        pre['url'] = url_for('domain.domain_edit', domain_id=self.id)
        return pre

    def set_del_button(self, pre):
        """
        Check for del button in Pager.
        :param pre: Flask-LwAdmin action dictionary
        :return: Flask-LwAdmin action dictionary
        """
        pre['url'] = url_for('domain.domain_delete', domain_id=self.id)
        return pre


def get_domain(domain_id):
    return db.session.query(Domain).get(domain_id)


class DomainPager(Pager):
    def initialize(self, configuration):
        from lightningwolf_smp.forms.domain import FormDomainFilter
        self.configure(configuration)
        filter_data = self.get_filter_data()
        self.set_filter_form(FormDomainFilter(**filter_data))
        self.set_count(get_domain_list_count(filter_data))
        self.calculate_pages()

    @staticmethod
    def get_pk():
        return 'id'

    def get_results(self):
        if self.results is None:
            self.results = get_domain_list(self.get_filter_data(), offset=self.get_offset(), limit=self.get_limit())

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
