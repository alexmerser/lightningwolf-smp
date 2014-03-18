#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hashlib
import json
import bcrypt

from email_validation import valid_email_address
from lightningwolf_smp.models.user_base import User
from lightningwolf_smp.models.user_admin import UserAdmin


admin_permissions = {
    'role': ['admin', 'user']
}
user_permissions = {
    'role': ['user']
}


class UserQuery(object):

    def __init__(self, db):
        self.db = db

    def get_user(self, user_id):
        return self.db.session.query(User).get(user_id)

    def get_user_by_username(self, username):
        return self.db.session.query(User).filter(User.username == username).first()

    def create_user(self, username, email, password, credential='user', active=True, cli=False):
        salt = hashlib.md5(str(uuid.uuid4())).hexdigest()
        salted = hashlib.sha512(password + salt).hexdigest()
        hashed = bcrypt.hashpw(salted, bcrypt.gensalt(12))

        if cli:
            if not self.is_unique_user(username):
                return "This username: %s is not unique in system. Try again" % username
            if not self.is_valid_email(email):
                return "This e-mail: %s is not valid. Try again" % email
            if not self.is_unique_email(email):
                return "This e-mail: %s is not unique in system. Try again" % email

        if credential == 'admin':
            user_credentials = admin_permissions
        else:
            user_credentials = user_permissions

        user = User(
            username=username,
            email=email,
            salt=salt,
            password=hashed,
            permissions=json.dumps(user_credentials, indent=4, sort_keys=True),
            active=active
        )
        user.save(self.db.session)
        return True

    def edit_user(self, user, email, password, credential='user', cli=False):
        if cli:
            if not self.is_valid_email(email):
                return "This e-mail: %s is not valid. Try again" % email
            if not self.is_unique_email(email, user.get_id()):
                return "This e-mail: %s is not unique in system. Try again" % email

        if password:
            salted = hashlib.sha512(password + user.salt).hexdigest()
            user.password = bcrypt.hashpw(salted, bcrypt.gensalt(12))

        if credential == 'admin':
            user_credentials = admin_permissions
        else:
            user_credentials = user_permissions
        user.permissions = json.dumps(user_credentials, indent=4, sort_keys=True)

        user.email = email

        user.save(self.db.session)
        return True

    def edit_password(self, user, password):
        salted = hashlib.sha512(password + user.salt).hexdigest()
        user.password = bcrypt.hashpw(salted, bcrypt.gensalt(12))

        user.save(self.db.session)
        return True

    def promote(self, user):
        user.permissions = json.dumps(admin_permissions, indent=4, sort_keys=True)

        user.save(self.db.session)
        return True

    def is_unique_user(self, username):
        if self.db.session.query(User).filter_by(username=username).first() is None:
            return True

        return False

    @staticmethod
    def is_valid_email(email):
        if not valid_email_address(email):
            return False
        return True

    def is_unique_email(self, email, user_id=None):
        if id is not None:
            if self.db.session.query(User).filter_by(email=email).filter(User.id != user_id).first() is None:
                return True
        else:
            if self.db.session.query(User).filter_by(email=email).first() is None:
                return True

        return False

    def admin_get_user_list(self, filter_data, offset=0, limit=100):
        query = self.db.session.query(UserAdmin)
        if 'username' in filter_data:
            if filter_data['username'] is not None:
                query = query.filter(User.username.like('%' + filter_data['username'] + '%'))
        return query.offset(offset).limit(limit)

    def admin_get_user_list_count(self, filter_data):
        query = self.db.session.query(UserAdmin)
        if 'username' in filter_data:
            if filter_data['username'] is not None:
                query = query.filter(User.username.like('%' + filter_data['username'] + '%'))
        return query.count()
