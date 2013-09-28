#!/usr/bin/env python
# coding=utf8
__author__ = 'ldath'
from flask_lwadmin.config import ConfigParser


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
        'batch_actions': [
            {
                'key': 'delete',
                'label': 'Delete'
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
        ]
    }
}
