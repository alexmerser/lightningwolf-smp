#!/usr/bin/env python
# coding=utf8
import hashlib
import json
import bcrypt

from lightningwolf_smp.models import Base
from sqlalchemy import Column, Integer, String, Text, Boolean


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    salt = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    permissions = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)

    # Flask-Login integration
    @staticmethod
    def is_authenticated():
        return True

    def is_active(self):
        return self.active

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.id

    def is_correct_password(self, password):
        salted = hashlib.sha512(password + self.salt).hexdigest().encode('utf-8')
        hashed = self.password.encode('utf-8')
        return bool(bcrypt.hashpw(salted, hashed) == hashed)

    def roles(self):
        return json.loads(self.permissions)['role']

    def save(self, session):
        session.add(self)
        return session.commit()

    def delete(self, session):
        session.delete(self)
        return session.commit()

    def get_username(self):
        return self.username

    def get_perm(self):
        roles = self.roles()
        for role in roles:
            if role == 'admin':
                return 'admin'
        return 'user'

    def __repr__(self):
        return '<User %r>' % self.username

    def __unicode__(self):
        return self.username

