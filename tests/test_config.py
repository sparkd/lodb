# -*- coding: utf-8 -*-
"""Test configs."""
from lodb.application import app_factory
from lodb.config import DevelopmentConfig, ProductionConfig


def test_production_config():
    """Production config."""
    app = app_factory(ProductionConfig)
    assert app.config['ENV'] == 'prod'
    assert app.config['DEBUG'] is False


def test_dev_config():
    """Development config."""
    app = app_factory(DevelopmentConfig)
    assert app.config['ENV'] == 'dev'
    assert app.config['DEBUG'] is True
