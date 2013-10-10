#!/usr/bin/env python
# coding=utf8
from flask_lwadmin.config import ConfigParser
from lightningwolf_smp.models.user import get_user_filters
from lightningwolf_smp.forms.user import (
    FormUsernameFilter,
    FormUserBatchActions
)

filter_data = get_user_filters()

configuration = {
    'list': {
        'display': [
            {'key': 'id', 'label': 'Id'},
            {'key': 'username', 'label': 'Username'},
            {'key': 'email', 'label': 'E-mail'}
        ],
        'actions': [
            {
                'key': 'new',
                'label': 'New',
                'url': 'user.user_create',
                'type': ConfigParser.URL_INTERNAL,
                'class': 'btn btn-primary'
            }
        ],
        'object_actions': [
            {
                'key': 'edit',
                'label': 'Edit',
                'url': 'user.user_edit',
                'type': ConfigParser.URL_PK,
                'icon': 'icon-edit',
                'call': 'set_edit_button'
            },
            {
                'key': 'delete',
                'label': 'Delete',
                'url': 'user.user_del',
                'type': ConfigParser.URL_PK,
                'icon': 'icon-trash icon-white',
                'confirm': True,
                'confirm_message': 'Are you sure?',
                'class': 'btn btn-small btn-danger',
                'call': 'set_del_button'
            }
        ],
        'batch': {
            'url': 'user.user_batch',
            'type': ConfigParser.URL_INTERNAL,
            'form': FormUserBatchActions()
        },
        'filter': {
            'url': 'user.user_filter',
            'type': ConfigParser.URL_INTERNAL,
            'form': FormUsernameFilter(**filter_data)
        }
    }
}
