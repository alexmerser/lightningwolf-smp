#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models.domain_base import Domain

from flask import (
    url_for
)


class DomainAdmin(Domain):

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
