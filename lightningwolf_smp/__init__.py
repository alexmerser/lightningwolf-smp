#!/usr/bin/env python
# coding=utf8
version = '0.0.1'


class Config(object):
    VERSION = version
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SENTRY_DSN = ''


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
