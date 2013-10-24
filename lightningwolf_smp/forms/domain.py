#!/usr/bin/env python
# coding=utf8
from flask_wtf import Form
from wtforms import (
    fields,
    validators
)


class FormDomainFilter(Form):
    domain_name = fields.TextField(
        label='Domain name',
        validators=[
            validators.Length(
                min=5,
                max=255,
                message=u'Domain name must be a minimum of %d and maximum of %d characters' % (2, 80)
            ),
            validators.Regexp(
                regex=r'^[a-z0-9-]+(\.[a-z0-9-]+)+$',
                message=u'Invalid Domain name'
            )
        ]
    )
