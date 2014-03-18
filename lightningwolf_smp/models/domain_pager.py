#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_lwadmin.pager import Pager
from lightningwolf_smp.application import db
from lightningwolf_smp.models.domain_query import DomainQuery

dq = DomainQuery(db=db)


class DomainPager(Pager):
    def initialize(self, configuration):
        from lightningwolf_smp.forms.domain import FormDomainFilter
        self.configure(configuration)
        filter_data = self.get_filter_data()
        self.set_filter_form(FormDomainFilter(**filter_data))
        self.set_count(dq.admin_get_domain_list_count(filter_data))
        self.calculate_pages()

    @staticmethod
    def get_pk():
        return 'id'

    def get_results(self):
        if self.results is None:
            self.results = dq.admin_get_domain_list(
                self.get_filter_data(),
                offset=self.get_offset(),
                limit=self.get_limit()
            )

        return self.results
