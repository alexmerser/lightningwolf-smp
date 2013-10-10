#!/usr/bin/env python
# coding=utf8
from flask_lwadmin.config import ConfigParser


configuration = {
    'list': {
        'display': [
            {'key': 'id', 'label': 'Id'},
            {'key': 'domain_name', 'label': 'Domain Name'},
            {'key': 'customer_id', 'label': 'Customer'}
        ],
        'actions': [
            {
                'key': 'new',
                'label': 'New',
                'url': 'domain.domain_create',
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
    }
}
