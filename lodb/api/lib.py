#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '07/02/2017'.
"""

from lodb.api.schema import Schema
from lodb.api.resource import RecordAPIResource, ListAPIResource, SchemaAPIResource


def list_resources(app):
    """
    Iterator; list of all resources
    :param app:
    :return:
    """

    # Dictionary of all resources to be added
    resources = {
        # FIXME: Update <str:id> to ensure mongo GUID
        '/{slug}/<string:identifier>': RecordAPIResource,
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
            yield slug, endpoint.format(slug=slug), resource
