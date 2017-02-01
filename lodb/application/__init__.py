#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
import sys
import logging

from flask import Flask, jsonify
from flask.helpers import get_debug_flag
from inspect import getmembers, isfunction
from flask_restful_swagger_2 import get_swagger_blueprint
from flask_cors import CORS

from lodb.config import ProductionConfig
from lodb.extensions import extensions
from lodb.encoders import JSONEncoder
from lodb.api.exceptions import APIException
from lodb.api.blueprint import get_api_blueprint
from lodb.api.schema import Schema
from lodb.api.swagger import get_swagger_docs
from lodb import commands


def app_factory(config=ProductionConfig):
    """An application factory - creates a new Flask app.
    :param config: The configuration object to use. Defaults to production
    """
    app = Flask(__name__)
    configure_app(app, config)
    register_extensions(app)
    register_error_handlers(app)
    register_filters(app)
    register_hooks(app)
    register_blueprints(app)
    configure_logging(app)
    register_commands(app)
    register_encoders(app)
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
    # Prepare a blueprint to serve the combined list of swagger document objects and register it
    app.register_blueprint(get_swagger_blueprint(get_swagger_docs(app), app.config['API_SWAGGER_URL'], title=app.config['API_TITLE'], api_version=app.config['API_VERSION']))
    # Allow CORS for the Swagger URL so swagger-ui can access it
    CORS(app, resources={r"%s.json" % app.config['API_SWAGGER_URL']: {"origins": "*"}})
    return None


def register_error_handlers(app):
    """Register error handlers."""

    # Handle API errors
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # If not in debug mode, then handle all other errors
    if not get_debug_flag():
        @app.errorhandler(Exception)
        def handle_exception(error):
            response = jsonify({'error': 'Server error'})
            response.status_code = 400
            return response

    return None


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
        Schema().build()


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


def register_encoders(app):
    """Register Encoders."""
    app.json_encoder = JSONEncoder
    return None

