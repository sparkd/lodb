#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import os
from lodb.config.default import DefaultConfig


class TestConfig(DefaultConfig):
    DEBUG = True
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/lodb_test"
    SCHEMA_DIR = os.path.abspath(os.path.join(DefaultConfig.PROJECT_ROOT, 'tests', 'schemas'))