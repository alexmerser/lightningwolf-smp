#!/usr/bin/env python
# coding=utf8
from flask_wtf import Form
from wtforms import (
    fields,
    validators
)

from lightningwolf_smp.utils.user import is_unique_email, is_unique_user


class FormUserAdd(Form):
    username = fields.TextField(
        label='Username',
        description=u'Enter username',
        validators=[
            validators.Required(message=u'Required field'),
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
            validators.Required(message=u'Required field'),
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
            validators.Required(message=u'Required field'),
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
        choices=[(u'user', u'User'), (u'admin', u'Admin')],
        validators=[
            validators.Required(message=u'Required field')
        ]
    )

    def validate_username(self, field):
        if not is_unique_user(field.data):
            raise validators.ValidationError('This username: %s is not unique in system.' % field.data)

    def validate_email(self, field):
        if not is_unique_email(field.data):
            raise validators.ValidationError('This e-mail: %s is not unique in system.' % field.data)


class FormUsernameFilter(Form):
    username = fields.TextField(
        label='Username',
        validators=[
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


class BaseFormUserChangePassword(Form):
    password = fields.PasswordField(
        label='Password',
        validators=[
            validators.EqualTo(
                'repassword',
                message=u'Passwords must be identical'
            )
        ]
    )

    repassword = fields.PasswordField('Repeat Password')


class FormUserChangeEmail(Form):
    def setId(self, id):
        self.id = id

    email = fields.TextField(
        label='Email',
        description=u'Enter the user\'s email',
        validators=[
            validators.Required(message=u'Required field'),
            validators.Length(
                min=7,
                max=120,
                message=u'E-mail must be a minimum of %d and maximum of %d characters' % (7, 120)
            ),
            validators.Email(message=u'Invalid e-mail address')
        ]
    )

    def validate_email(self, field):
        if not is_unique_email(field.data, id=self.id):
            raise validators.ValidationError('This e-mail: %s is not unique in system.' % field.data)


class FormUserEdit(BaseFormUserChangePassword, FormUserChangeEmail):
    perm = fields.SelectField(
        label='User Roles',
        choices=[(u'user', u'User'), (u'admin', u'Admin')],
        validators=[
            validators.Required(message=u'Required field')
        ]
    )
