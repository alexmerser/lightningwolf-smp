#!/usr/bin/env python
# coding=utf8
import uuid
import hashlib
import json
import bcrypt

from flask import session
from lightningwolf_smp.application import db
from lightningwolf_smp.models import User
from sqlalchemy import exc


admin_permissions = {
    'role': ['admin', 'user']
}
user_permissions = {
    'role': ['user']
}


def get_user_list(filter_data):
    query = db.session.query(User)
    if 'username' in filter_data:
        if filter_data['username'] is not None:
            query = query.filter(User.username.like('%' + filter_data['username'] + '%'))
    return query


def get_user(id):
    return db.session.query(User).get(id)


def get_user_filters():
    if 'filter.user' in session:
        return session['filter.user']
    else:
        return {"username": None}


def set_user_filters(filter_data):
    session['filter.user'] = filter_data


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


def is_unique_user(username):
    if User.query.filter_by(username=username).first() is None:
        return True

    return False


def is_valid_email(email):
    from email_validation import valid_email_address

    if not valid_email_address(email):
        return False

    return True


def is_unique_email(email, id=None):
    if id is not None:
        if User.query.filter_by(email=email).filter(User.id != id).first() is None:
            return True
    else:
        if User.query.filter_by(email=email).first() is None:
            return True

    return False
