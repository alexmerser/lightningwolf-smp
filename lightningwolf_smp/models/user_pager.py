#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_lwadmin.pager import Pager
from lightningwolf_smp.models.user_query import UserQuery
from lightningwolf_smp.application import db

uq = UserQuery(db=db)


class UserPager(Pager):
    def initialize(self, configuration):
        from lightningwolf_smp.forms.user import (
            FormUsernameFilter,
            FormUserBatchActions
        )
        self.configure(configuration)
        filter_data = self.get_filter_data()
        self.set_filter_form(FormUsernameFilter(**filter_data))
        self.set_batch_form(FormUserBatchActions())
        self.set_count(uq.admin_get_user_list_count(filter_data))
        self.calculate_pages()

    def get_pk(self):
        return 'id'

    def get_results(self):
        if self.results is None:
            self.results = uq.admin_get_user_list(self.get_filter_data(), offset=self.get_offset(), limit=self.get_limit())

        return self.results
