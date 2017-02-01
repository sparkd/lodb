#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""


from flask import request, jsonify
from flask_restful import Resource, reqparse

from lodb.api.schema import Schema
from lodb.api.document import Document
from lodb.api.collection import Collection
from lodb.parsers import pagination_parser

parser = reqparse.RequestParser(bundle_errors=True)


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


class RecordAPIResource(APIResource):
    """
    API resource for single record
    """

    def __init__(self, slug):
        super(RecordAPIResource, self).__init__(slug)
        self.doc = Document(slug)

    def get(self, identifier):
        return jsonify(self.doc.read(identifier))

    def delete(self, identifier):
        self.doc.delete(identifier)
        return {'success': 1}

    def put(self, identifier):
        data = request.get_json(silent=True)
        self.doc.update(identifier, data)


class ListAPIResource(APIResource):

    def get(self):
        pagination = pagination_parser()
        # Convert page and limit to skip and limit
        query_args = dict(limit=pagination['limit'])
        # If page is greater than 1, then skip x records
        if pagination['page'] > 1:
            query_args['skip'] = (pagination['page']-1)*pagination['limit']

        # Query MongoDB - gets result cursor
        cursor = Collection(self.slug).find(**query_args)

        # Return JSON dict of records and total
        # Explicity pass through jsonify so it uses custom JSONEncoder
        return jsonify({
            'total': cursor.count(),
            'records': list(cursor)
        })

    def post(self):
        data = request.get_json(silent=True)
        Document(self.slug).create(data)


class SchemaAPIResource(APIResource):
    def get(self):
        schema = Schema().load(self.slug)
        return jsonify(schema)
