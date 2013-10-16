#!/usr/bin/env python
# coding=utf8
import uuid
import hashlib
import json
import bcrypt


from flask import session
from flask import url_for
from flask.ext.login import current_user
from flask_lwadmin.pager import Pager
from sqlalchemy import exc
from lightningwolf_smp.application import db


admin_permissions = {
    'role': ['admin', 'user']
}
user_permissions = {
    'role': ['user']
}


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    salt = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    permissions = db.Column(db.Text, nullable=False)

    # Flask-Login integration
    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

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

    def save(self):
        db.session.add(self)
        return db.session.commit()

    def delete(self):
        db.session.delete(self)
        return db.session.commit()

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

    # Flask-LwAdmin integration
    def __unicode__(self):
        return self.username

    def set_edit_button(self, pre):
        pre['url'] = url_for('user.user_edit', user_id=self.id)
        return pre

    def set_del_button(self, pre):
        """
        Check for del button in Pager. If current_user is the same as user then Del button is not visable
        :param pre: Flask-LwAdmin action dictionary
        :return: Flask-LwAdmin action dictionary
        """
        pre['url'] = url_for('user.user_del', user_id=self.id)
        if current_user.username == self.username:
            pre['disabled'] = True
            pre['label'] = 'It\'s you'
            pre['icon'] = None
        return pre


def get_user(user_id):
    return db.session.query(User).get(user_id)


def create_user(username, email, password, credential='user', cli=False):
    salt = hashlib.md5(str(uuid.uuid4())).hexdigest()
    salted = hashlib.sha512(password + salt).hexdigest()
    hashed = bcrypt.hashpw(salted, bcrypt.gensalt(12))

    if cli:
        if not is_unique_user(username):
            return "This username: %s is not unique in system. Try again" % username
        if not is_valid_email(email):
            return "This e-mail: %s is not valid. Try again" % email
        if not is_unique_email(email):
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
        permissions=json.dumps(user_credentials, indent=4, sort_keys=True)
    )

    try:
        user.save()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def edit_user(user, email, password, credential='user', cli=False):
    if cli:
        if not is_valid_email(email):
            return "This e-mail: %s is not valid. Try again" % email
        if not is_unique_email(email, user.get_id()):
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

    try:
        user.save()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def edit_password(user, password):
    salted = hashlib.sha512(password + user.salt).hexdigest()
    user.password = bcrypt.hashpw(salted, bcrypt.gensalt(12))

    try:
        user.save()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False


def is_unique_user(username):
    if User.query.filter_by(username=username).first() is None:
        return True

    return False


def is_valid_email(email):
    from email_validation import valid_email_address

    if not valid_email_address(email):
        return False

    return True


def is_unique_email(email, user_id=None):
    if id is not None:
        if User.query.filter_by(email=email).filter(User.id != user_id).first() is None:
            return True
    else:
        if User.query.filter_by(email=email).first() is None:
            return True

    return False


class UserPager(Pager):
    def __init__(self, max_per_page=10, page=1):
        Pager.__init__(self, max_per_page=max_per_page, page=page)
        self.filter_data = {}

    def initialize(self, configuration):
        # TODO: filter_data in this moment is get in blueprint for configuration too!
        self.filter_data = get_user_filters()
        self.set_count(get_user_list_count(self.filter_data))
        Pager.initialize(self, configuration)

    def get_pk(self):
        return 'id'

    def get_results(self):
        if self.results is None:
            self.results = get_user_list(self.filter_data, offset=self.get_offset(), limit=self.get_limit())

        return self.results


def get_user_list(filter_data, offset=0, limit=100):
    query = db.session.query(User)
    if 'username' in filter_data:
        if filter_data['username'] is not None:
            query = query.filter(User.username.like('%' + filter_data['username'] + '%'))
    return query.offset(offset).limit(limit)


def get_user_list_count(filter_data):
    query = db.session.query(User)
    if 'username' in filter_data:
        if filter_data['username'] is not None:
            query = query.filter(User.username.like('%' + filter_data['username'] + '%'))
    return query.count()


def get_user_filters():
    if 'filter.user' in session:
        return session['filter.user']
    else:
        return {"username": None}


def set_user_filters(filter_data):
    session['filter.user'] = filter_data
