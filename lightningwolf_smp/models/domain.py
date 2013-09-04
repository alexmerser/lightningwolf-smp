#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db


class Domain(db.Model):
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    domain_name = db.Column(db.String(255), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('domain', lazy='dynamic'))

    def __repr__(self):
        return '<Domain %r>' % self.domain_name

    # Flask-LwAdmin integration
    def __unicode__(self):
        return self.domain_name
