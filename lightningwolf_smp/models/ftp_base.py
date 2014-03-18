#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.models import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, backref


class FtpGroup(Base):
    __tablename__ = 'ftp_group'

    id = Column(Integer, primary_key=True)
    group_name = Column(String(30), unique=True, nullable=False)
    gid = Column(Integer, nullable=False)
    members = Column(String(255), nullable=False)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('ftp_group', lazy='dynamic'))

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def __repr__(self):
        return '<FtpGroup %r>' % self.group_name

    def __unicode__(self):
        return self.group_name


class FtpUsers(Base):
    __tablename__ = 'ftp_user'

    id = Column(Integer, primary_key=True)
    userid = Column(String(30), nullable=False)
    passwd = Column(String(30), nullable=False)
    uid = Column(Integer, nullable=False)
    gid = Column(Integer, nullable=False)
    homedir = Column(String(255), nullable=False)
    shell = Column(String(255), nullable=False)
    last_accessed = Column(DateTime, nullable=True)

    customer_id = Column(Integer, ForeignKey('user.id'))
    customer = relationship('User', backref=backref('ftp_user', lazy='dynamic'))

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def __repr__(self):
        return '<FtpUsers %r>' % self.userid

    def __unicode__(self):
        return self.userid


class FtpLoginHistory(Base):
    __tablename__ = 'ftp_login_history'

    id = Column(Integer, primary_key=True)
    userid = Column(String(30), nullable=False)
    client_ip = Column(String(39), nullable=False)
    server_ip = Column(String(39), nullable=False)
    protocol = Column(Text, nullable=False)
    when = Column(DateTime, nullable=False)

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def __repr__(self):
        return '<FtpLoginHistory %r>' % self.userid

    def __unicode__(self):
        return self.userid


"""
http://www.proftpd.org/docs/howto/SQL.html
"""