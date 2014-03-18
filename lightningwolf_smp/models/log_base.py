#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref


class SmpLog(Base):
    __tablename__ = 'smp_log'

    id = Column(Integer, primary_key=True)
    action_time = Column(DateTime, index=True, nullable=False)
    username = Column(String(80), nullable=False)
    domain = Column(String(255), nullable=False)
    action = Column(String(255), nullable=False)
    data = Column(Text, nullable=True)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('smp_log', lazy='dynamic'))

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def __repr__(self):
        return '<SmpLog %r>' % self.action

    def __unicode__(self):
        return self.action
