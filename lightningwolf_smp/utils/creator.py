#!/usr/bin/env python
# coding=utf8
from lightningwolf_smp.application import db
from lightningwolf_smp.models import *


def generate():
        # db.drop_all()
        db.create_all()
