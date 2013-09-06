#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db


class SmpLog(db.Model):
    __tablename__ = 'smp_log'

    id = db.Column(db.Integer, primary_key=True)
    action_time = db.Column(db.DateTime, index=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    domain = db.Column(db.String(255), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Text, nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', backref=db.backref('smp_log', lazy='dynamic'))

    def __repr__(self):
        return '<SmpLog %r>' % self.action

    def __unicode__(self):
        return self.action
