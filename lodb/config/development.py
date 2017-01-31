#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
from lodb.config.default import DefaultConfig


class DevelopmentConfig(DefaultConfig):
    ENV = 'dev'
    DEBUG = True
    TESTING = False
