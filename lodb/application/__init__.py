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
from lodb.extensions import cache, csrf, debug_toolbar
from lodb import commands


def app_factory(config=ProductionConfig):
    """An application factory, that creates a new Flask app.
    :param config: The configuration object to use. Defaults to production
    """
    app = Flask(__name__)
    configure_app(app, config)
    register_extensions(app)
    register_blueprints(app)
    # register_errorhandlers(app)
    register_filters(app)
    # register_hooks(app)
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
    cache.init_app(app)
    csrf(app)
    debug_toolbar.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    # for blueprint in blueprints:
    #     app.register_blueprint(blueprint)

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


# def register_hooks(app):
#     """Configure hook."""
#     @app.before_request
#     def before_request():
#         print('Before request hook')


def configure_logging(app):
    """Configure logging."""
    loggers = [app.logger]
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    for logger in loggers:
        logger.setLevel(app.config['LOG_LEVEL'])
        logger.addHandler(stream_handler)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.install_schema)


# import logging.config
# from flask import Flask, Blueprint, render_template
# from flask_restful import Api, Resource
# app = Flask(__name__)
#
# logging.config.fileConfig('logging.ini')
# log = logging.getLogger(__name__)
#
# api_blueprint = Blueprint('api', __name__, url_prefix='/api')
#
# api = Api(api_blueprint)
#
#
# class APIRecord(Resource):
#     def get(self, id):
#         return id
#
#     def delete(self, id):
#         return id
#
#     def put(self, id):
#         return id
#
#
# class APIList(Resource):
#     def get(self):
#         return 'list'
#
#     def post(self):
#         return 'create'
#
# api.add_resource(APIList, '/eg/')
# api.add_resource(APIRecord, '/eg/<int:id>')
#
# app.register_blueprint(api_blueprint)
#
# # https://github.com/mattupstate/flask-jsonschema
#
# #
# #
# # @app.route('/hello')
# # def hello():
# #     return render_template('hello.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
