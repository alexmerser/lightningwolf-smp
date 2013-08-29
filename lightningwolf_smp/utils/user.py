#!/usr/bin/env python
# coding=utf8
import uuid
import hashlib
import json
import bcrypt


from lightningwolf_smp.application import db
from lightningwolf_smp.models import User


admin_permisions = {
    'role': ['admin', 'user']
}
user_permisions = {
    'role': ['user']
}


def create_user(username, email, password, credential):
    salt = hashlib.md5(str(uuid.uuid4())).hexdigest()
    salted = hashlib.sha512(password + salt).hexdigest()
    hashed = bcrypt.hashpw(salted, bcrypt.gensalt(12))

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
    db.session.add(user)
    db.session.commit()
