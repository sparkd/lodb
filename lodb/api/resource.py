#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

from flask_restful import Resource


class APIResource(Resource):
    """
    Base API resource.
    Receives schema slug as parameter
    """
    def __init__(self, slug):
        self.slug = slug
        # TODO - Load schema??


class RecordAPIResource(APIResource):
    """
    API resource for single record
    """

    def get(self, id):
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
        return 'schema def'
