#!/usr/bin/env python
# coding=utf8
from flask_lwadmin.config import ConfigParser

configuration = {
    'list': {
        'title': 'Users List',
        'display': [
            {'key': 'id', 'label': 'Id'},
            {'key': 'username', 'label': 'Username', 'icon': 'icon-user'},
            {'key': 'email', 'label': 'E-mail', 'icon': 'icon-envelope'}
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
                'icon': 'icon-edit',
                'call': 'set_edit_button'
            },
            {
                'key': 'delete',
                'label': 'Delete',
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
        },
        'filter': {
            'session_name': 'filter.user',
            'display': ['username'],
            'url': 'user.user_filter',
            'type': ConfigParser.URL_INTERNAL
        }
    },
    'create': {
        'title': 'Create Users',
        'form': None,
        'url': None,
        'display_blocks': [
            {
                'legend': None,
                'display': ['username', 'password', 'repassword', 'email', 'perm']
            }
        ],
        'submit_actions': [
            {
                'key': 'save',
                'label': 'Save',
                'class': 'btn btn-primary'
            },
            {
                'key': 'save_and_add',
                'label': 'Save and Add',
                'class': 'btn btn-primary'
            }
        ],
        'actions': [
            {
                'key': 'back',
                'label': 'Back to list',
                'url': None,
                'class': 'btn btn-warning',
                'icon': 'icon-backward'
            }
        ]
    },
    'update': {
        'title': 'Edit User',
        'form': None,
        'url': None,
        'display_blocks': [
            {
                'legend': None,
                'display': ['email', 'perm']
            },
            {
                'legend': 'Optional password change',
                'display': ['password', 'repassword']
            }
        ],
        'submit_actions': [
            {
                'key': 'save',
                'label': 'Save',
                'class': 'btn btn-primary'
            },
            {
                'key': 'save_and_add',
                'label': 'Save and Add',
                'class': 'btn btn-primary'
            }
        ],
        'actions': [
            {
                'key': 'back',
                'label': 'Back to list',
                'url': None,
                'class': 'btn btn-warning',
                'icon': 'icon-backward'
            }
        ]
    }
}
