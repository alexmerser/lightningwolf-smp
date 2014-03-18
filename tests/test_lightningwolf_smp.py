#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import division
from __future__ import absolute_import

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
from lightningwolf_smp.models import *
from lightningwolf_smp.utils.generator import generate_test_data

session = None
engine = None
app = None


def setup_module(module):
    from lightningwolf_smp.application import app

    Session = sessionmaker()
    module.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    my_path = os.path.dirname(__file__)
    my_ini = os.path.abspath(my_path + '/../lightningwolf_smp/alembic.ini')

    alembic_cfg = Config(my_ini)
    command.stamp(alembic_cfg, "head")

    Session.configure(bind=module.engine)
    module.session = Session()
    module.session._model_changes = {}

    generate_test_data(module.session)

    app.config["TESTING"] = True
    module.app = app.test_client()


def test_assert():
    a = 1
    b = 1
    assert a == b
