#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
import sys
import logging

from flask import Flask, Blueprint
from inspect import getmembers, isfunction
from lodb.config import ProductionConfig
from lodb.extensions import extensions
from lodb.api.blueprint import get_api_blueprint
from lodb.api.schema import schema_init
from lodb import commands


def app_factory(config=ProductionConfig):
    """An application factory - creates a new Flask app.
    :param config: The configuration object to use. Defaults to production
    """
    app = Flask(__name__)
    configure_app(app, config)
    register_extensions(app)
    # register_errorhandlers(app)
    register_filters(app)
    register_hooks(app)
    register_blueprints(app)
    configure_logging(app)
    register_commands(app)
    return app


def configure_app(app, config):
    """Configure app."""
    app.config.from_object(config)


def register_extensions(app):
    """Register Flask extensions.

    :app: The Flask app.
    """
    for extension in extensions:
        extension.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(get_api_blueprint(app))
    return None


# def register_errorhandlers(app):
#     """Register error handlers."""
#     def render_error(error):
#         """Render error template."""
#         # If a HTTPException, pull the `code` attribute; default to 500
#         error_code = getattr(error, 'code', 500)
#         return render_template('errors/{0}.html'.format(error_code)), error_code
#
#     for errcode in [401, 404, 500]:
#         app.errorhandler(errcode)(render_error)
#
#     return None


def register_filters(app):
    """Configure template filters. - Register all filter functions """
    from lodb import filters
    for func_name, func in getmembers(filters, isfunction):
        app.jinja_env.filters[func_name] = func


# I don't like this firing before request - need these to run when app starts
# As there could be quite a bit of work versioning json schemas
def register_hooks(app):
    """Configure hook."""
    @app.before_first_request
    def before_first_request():
        # On start up, parse, validate and load schemas
        app.logger.info('Before first request: initiating schema')
        schema_init()


def configure_logging(app):
    """Configure logging."""
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.addHandler(stream_handler)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.install_schema)

