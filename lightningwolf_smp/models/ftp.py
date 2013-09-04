#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db


class FtpGroup(db.Model):
    __tablename__ = 'ftp_group'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(30), unique=True, nullable=False)
    gid = db.Column(db.Integer, nullable=False)
    members = db.Column(db.String(255), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', backref=db.backref('ftp_group', lazy='dynamic'))

    def __repr__(self):
        return '<FtpGroup %r>' % self.group_name

    def __unicode__(self):
        return self.group_name


class FtpUsers(db.Model):
    __tablename__ = 'ftp_user'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(30), nullable=False)
    passwd = db.Column(db.String(30), nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    gid = db.Column(db.Integer, nullable=False)
    homedir = db.Column(db.String(255), nullable=False)
    shell = db.Column(db.String(255), nullable=False)
    last_accessed = db.Column(db.DateTime, nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer = db.relationship('User', backref=db.backref('ftp_user', lazy='dynamic'))

    def __repr__(self):
        return '<FtpUsers %r>' % self.userid

    def __unicode__(self):
        return self.userid


class FtpLoginHistory(db.Model):
    __tablename__ = 'ftp_login_history'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(30), nullable=False)
    client_ip = db.Column(db.String(39), nullable=False)
    server_ip = db.Column(db.String(39), nullable=False)
    protocol = db.Column(db.Text, nullable=False)
    when = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<FtpLoginHistory %r>' % self.userid

    def __unicode__(self):
        return self.userid


"""
http://www.proftpd.org/docs/howto/SQL.html
"""