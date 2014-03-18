#!/usr/bin/env python
# coding=utf8
import os
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from lightningwolf_smp.models import *
from lightningwolf_smp.application import app


def generate():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    my_path = os.path.dirname(__file__)
    my_ini = os.path.abspath(my_path + '/../alembic.ini')
    alembic_cfg = Config(my_ini)
    command.stamp(alembic_cfg, "head")
