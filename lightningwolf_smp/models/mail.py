#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models import Base
from lightningwolf_smp.application import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class MailVirtualDomain(Base):
    __tablename__ = 'mail_virtual_domain'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('mail_virtual_domain', lazy='dynamic'))

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return '<MailVirtualDomain %r>' % self.name

    def __unicode__(self):
        return self.name


class MailVirtualUser(Base):
    __tablename__ = 'mail_virtual_user'

    id = Column(Integer, primary_key=True)

    domain_id = Column(Integer, ForeignKey('mail_virtual_domain.id'))
    domain = relationship('MailVirtualDomain', backref=backref('mail_virtual_user', lazy='dynamic'))

    password = Column(String(106), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return '<MailVirtualUser %r>' % self.email

    def __unicode__(self):
        return self.email


class MailVirtualAlias(Base):
    __tablename__ = 'mail_virtual_alias'

    id = Column(Integer, primary_key=True)

    domain_id = Column(Integer, ForeignKey('mail_virtual_domain.id'))
    domain = relationship('MailVirtualDomain', backref=backref('mail_virtual_alias', lazy='dynamic'))

    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return '<MailVirtualAlias %r -> %r>' % (self.source, self.destination)

    def __unicode__(self):
        return self.source + " -> " + self.destination


"""
https://library.linode.com/email/postfix/postfix2.9.6-dovecot2.0.19-mysql
"""