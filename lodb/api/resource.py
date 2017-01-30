#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

from flask_restful import Resource
from lodb.api.schema import schema_load

class APIResource(Resource):
    """
    Base API resource.
    Receives schema slug as parameter, and loads the appropriate schema
    """
    def __init__(self, slug):
        """
        Load the schema for this resource
        :param slug: Schema slog
        """
        self.slug = slug
        self.schema = schema_load(slug)


class RecordAPIResource(APIResource):
    """
    API resource for single record
    """

    def get(self, id):
        # MONGO: find one or 404
        return id

    def delete(self, id):
        return id

    def put(self, id):
        return id


class ListAPIResource(APIResource):
    def get(self):
        return 'list-' + self.slug

    def post(self):
        return 'create'


class SchemaAPIResource(APIResource):
    def get(self):
        return self.schema
