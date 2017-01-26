#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import logging
from lodb.config.default import DefaultConfig


class ProductionConfig(DefaultConfig):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.WARN