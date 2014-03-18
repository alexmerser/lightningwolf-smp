#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lightningwolf_smp.models.domain_base import Domain
from lightningwolf_smp.models.domain_admin import DomainAdmin


filter_display = ['domain_name']


class DomainQuery(object):

    def __init__(self, db):
        self.db = db

    def get_domain(self, domain_id):
        return self.db.session.query(Domain).get(domain_id)

    def admin_get_domain_list(self, filter_data, offset=0, limit=100):
        query = self.db.session.query(DomainAdmin)
        if 'domain_name' in filter_data:
            if filter_data['domain_name'] is not None:
                query = query.filter(DomainAdmin.domain_name.like('%' + filter_data['domain_name'] + '%'))
        return query.offset(offset).limit(limit)

    def admin_get_domain_list_count(self, filter_data):
        query = self.db.session.query(DomainAdmin)
        if 'domain_name' in filter_data:
            if filter_data['domain_name'] is not None:
                query = query.filter(DomainAdmin.domain_name.like('%' + filter_data['domain_name'] + '%'))
        return query.count()
