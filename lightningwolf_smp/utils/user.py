#!/usr/bin/env python
# coding=utf8
import uuid
import hashlib
import json
import bcrypt


from lightningwolf_smp.application import db
from lightningwolf_smp.models import User
from sqlalchemy import exc


admin_permisions = {
    'role': ['admin', 'user']
}
user_permisions = {
    'role': ['user']
}


def get_user_list():
    return db.session.query(User)


def get_user(id):
    return db.session.query(User).get(id)


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
        user_credentials = admin_permisions
    else:
        user_credentials = user_permisions

    user = User(
        username=username,
        email=email,
        salt=salt,
        password=hashed,
        permissions=json.dumps(user_credentials, indent=4, sort_keys=True)
    )

    try:
        db.session.add(user)
        db.session.commit()
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


def is_unique_email(email):
    if User.query.filter_by(email=email).first() is None:
        return True
    return False
