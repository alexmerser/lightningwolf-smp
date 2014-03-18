#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models.user_base import User
from flask import (
    url_for
)
from flask.ext.login import current_user


class UserAdmin(User):
    def set_edit_button(self, pre):
        pre['url'] = url_for('user.user_edit', user_id=self.id)
        return pre

    def set_del_button(self, pre):
        """
        Check for del button in Pager. If current_user is the same as user then Del button is not visable
        :param pre: Flask-LwAdmin action dictionary
        :return: Flask-LwAdmin action dictionary
        """
        pre['url'] = url_for('user.user_del', user_id=self.id)
        if current_user.username == self.username:
            pre['disabled'] = True
            pre['label'] = 'It\'s you'
            pre['icon'] = None
        return pre

