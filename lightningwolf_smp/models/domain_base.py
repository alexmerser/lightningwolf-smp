#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class Domain(Base):
    __tablename__ = 'domain'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, nullable=True)
    domain_name = Column(String(255), unique=True, nullable=False)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('domain', lazy='dynamic'))

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def __repr__(self):
        return '<Domain %r>' % self.domain_name

    def __unicode__(self):
        return self.domain_name


