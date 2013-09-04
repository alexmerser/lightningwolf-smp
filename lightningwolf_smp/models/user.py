#!/usr/bin/env python
# coding=utf8
import json
import bcrypt
import hashlib


from lightningwolf_smp.application import db
from sqlalchemy.dialects.mysql import MEDIUMTEXT


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    salt = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    permissions = db.Column(MEDIUMTEXT, nullable=False)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_correct_password(self, password):
        salted = hashlib.sha512(password + self.salt).hexdigest().encode('utf-8')
        hashed = self.password.encode('utf-8')
        return bool(bcrypt.hashpw(salted, hashed) == hashed)

    def roles(self):
        return json.loads(self.permissions)['role']

    def __repr__(self):
        return '<User %r>' % self.login

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username

    # Flask-LwAdmin integration
    def __unicode__(self):
        return self.username
