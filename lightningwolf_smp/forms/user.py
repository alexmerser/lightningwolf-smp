#!/usr/bin/env python
# coding=utf8
from flask_wtf import Form
from wtforms import (
    fields,
    validators
)


class FormUserAdd(Form):
    username = fields.TextField(
        label='Username',
        description=u'Enter username',
        validators=[
            validators.Required(mesage=u'Required field'),
            validators.Length(
                min=2,
                max=80,
                message=u'Username must be a minimum of %d and maximum of %d characters' % (2, 80)
            ),
            validators.Regexp(
                regex=r'^[\w_\.]+$',
                message=u'The user name can contain only letters, numbers, and character _ and .'
            )
        ]
    )

    password = fields.PasswordField(
        label='Password',
        validators=[
            validators.Required(mesage=u'Required field'),
            validators.EqualTo(
                'repassword',
                message=u'Passwords must be identical'
            )
        ]
    )

    repassword = fields.PasswordField('Repeat Password')

    email = fields.TextField(
        label='Email',
        description=u'Enter the user\'s email',
        validators=[
            validators.Required(mesage=u'Required field'),
            validators.Length(
                min=7,
                max=120,
                message=u'E-mail must be a minimum of %d and maximum of %d characters' % (7, 120)
            ),
            validators.Email(message=u'Invalid e-mail address')
        ]
    )

    perm = fields.SelectField(
        label='User Roles',
        choices=[('user', 'User'), ('admin', 'Admin')],
        validators=[
            validators.Required(mesage=u'Required field')
        ]
    )