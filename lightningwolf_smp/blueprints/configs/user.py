#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'
from flask_lwadmin.config import ConfigParser
from lightningwolf_smp.utils.user import get_user_filters
from lightningwolf_smp.forms.user import FormUsernameFilter, FormUserBatchActions

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
                'type': ConfigParser.URL_INTERNAL
            }
        ],
        'object_actions': [
            {
                'key': 'edit',
                'label': 'Edit'
            },
            {
                'key': 'delete',
                'label': 'Delete'
            }
        ],
        'batch': {
            'form': {
                'url': 'user.user_batch',
                'form': FormUserBatchActions()
            },
            'actions': [
                {
                    'key': 'delete',
                    'label': 'Delete'
                }
            ],
        },
        'filter': {
            'url': 'user.user_filter',
            'type': ConfigParser.URL_INTERNAL,
            'form': FormUsernameFilter(**filter_data)
        }
    }
}
