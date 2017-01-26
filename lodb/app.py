#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
from flask.helpers import get_debug_flag
from lodb.application import app_factory
from lodb.config import DevelopmentConfig, ProductionConfig
CONFIG = DevelopmentConfig if get_debug_flag() else ProductionConfig
app = app_factory(CONFIG)

if __name__ == '__main__':
    app.run(debug=True)
