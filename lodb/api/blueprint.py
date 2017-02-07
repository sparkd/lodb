#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '27/01/2017'.
"""

from flask import Blueprint
from flask_restful_swagger_2 import Api

from lodb.api.schema import Schema
from lodb.api.resource import RecordAPIResource, ListAPIResource, SchemaAPIResource, SchemaListAPIResource


def get_api_blueprint(app):
    """
    Build API blueprint, initiating an endpoint for all schemas
    :param app:
    :return:
    """
    api_blueprint = Blueprint('api', __name__, url_prefix=app.config['API_URL_PREFIX'])
    api = Api(api_blueprint, add_api_spec_resource=False)

    # Dictionary of all resources to be added
    resources = {
        # FIXME: Update <str:id> to ensure mongo GUID
        '/{slug}/<string:identifier>/': RecordAPIResource,
        '/{slug}/': ListAPIResource,
        '/{slug}.schema.json': SchemaAPIResource
    }

    # Get all slugs from json schema files - use the config json schema
    # files as the schema source of truth - if a config file is deleted
    # it can then persist in the mongo collection for data versioning
    # But will not be available via the API
    for slug in Schema().list_files(app.config['SCHEMA_DIR']).keys():
        for endpoint, resource in resources.items():
            slugged_endpoint = endpoint.format(slug=slug)
            # Add the resource - we need to manually specify the endpoint
            # so we don't get collisions with multiple schemas
            api.add_resource(resource, slugged_endpoint, endpoint=slugged_endpoint, resource_class_args=(slug,))

    # Add the
    api.add_resource(SchemaListAPIResource, '/')

    return api_blueprint
