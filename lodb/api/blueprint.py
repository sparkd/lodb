#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '27/01/2017'.
"""

from flask import Blueprint
from flask_restful import Api

from lodb.api.lib import list_resources
from lodb.api.resource import SchemaListAPIResource


def get_api_blueprint(app):
    """
    Build API blueprint, initiating an endpoint for all schemas
    :param app:
    :return:
    """
    api_blueprint = Blueprint('api', __name__, url_prefix=app.config['API_URL_PREFIX'])
    api = Api(api_blueprint)

    for slug, endpoint, resource in list_resources(app):
        # Add the resource - we need to manually specify the endpoint
        # so we don't get collisions with multiple schemas
        api.add_resource(resource, endpoint, endpoint=endpoint, resource_class_args=(slug,))

    # Add the list of schema resources
    api.add_resource(SchemaListAPIResource, '/')

    return api_blueprint
