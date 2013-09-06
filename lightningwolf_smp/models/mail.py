#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db


class MailVirtualDomain(db.Model):
    __tablename__ = 'mail_virtual_domain'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', backref=db.backref('mail_virtual_domain', lazy='dynamic'))

    def __repr__(self):
        return '<MailVirtualDomain %r>' % self.name

    def __unicode__(self):
        return self.name


class MailVirtualUser(db.Model):
    __tablename__ = 'mail_virtual_user'

    id = db.Column(db.Integer, primary_key=True)

    domain_id = db.Column(db.Integer, db.ForeignKey('mail_virtual_domain.id'))
    domain = db.relationship('MailVirtualDomain', backref=db.backref('mail_virtual_user', lazy='dynamic'))

    password = db.Column(db.String(106), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<MailVirtualUser %r>' % self.email

    def __unicode__(self):
        return self.email


class MailVirtualAlias(db.Model):
    __tablename__ = 'mail_virtual_alias'

    id = db.Column(db.Integer, primary_key=True)

    domain_id = db.Column(db.Integer, db.ForeignKey('mail_virtual_domain.id'))
    domain = db.relationship('MailVirtualDomain', backref=db.backref('mail_virtual_alias', lazy='dynamic'))

    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<MailVirtualAlias %r -> %r>' % (self.source, self.destination)

    def __unicode__(self):
        return self.source + " -> " + self.destination


"""
https://library.linode.com/email/postfix/postfix2.9.6-dovecot2.0.19-mysql
"""