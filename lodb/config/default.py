#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
import os
import logging


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CACHE_TYPE = 'simple'
    LOG_LEVEL = logging.DEBUG
    APP_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SCHEMA_DIR = os.path.abspath(os.path.join(APP_DIR, 'config', 'schemas'))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.environ.get('FLASK_APP_SECRET', 'secret-key')  # TODO: Change me
    MONGO_URI = "mongodb://localhost:27017/lodb_test"
    PAGINATION_DEFAULT_LIMIT = 100
    PAGINATION_MAX_LIMIT = 500

