#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '27/01/2017'.
"""

from flask import Blueprint
from flask_restful import Api, Resource

from lodb.api.schema import schema_load_all
from lodb.api.resource import RecordAPIResource, ListAPIResource, SchemaAPIResource


def get_api_blueprint(app):
    """
    Build API blueprint, initiating an endpoint for all schemas
    :param app:
    :return:
    """

    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(api_blueprint)

    # Dictionary of all resources to be added
    resources = {
        '/{slug}/<int:id>': RecordAPIResource,
        '/{slug}/': ListAPIResource,
        '/{slug}.json': SchemaAPIResource
    }

    print('API')

    # FIXME: ???
    with app.app_context():

        # TODO: Get custom classes.

        for slug in schema_load_all().keys():
            for endpoint, resource in resources.items():
                slugged_endpoint = endpoint.format(slug=slug)
                # Add the resource - we need to manually specify the endpoint
                # so we don't get collisions with multiple schemas
                api.add_resource(resource, slugged_endpoint, endpoint=slugged_endpoint, resource_class_args=(slug,))

    return api_blueprint
