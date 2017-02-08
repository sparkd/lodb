#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""


from flask import request, jsonify
from flask_restful import reqparse, Resource

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

    @staticmethod
    def success(**kwargs):
        kwargs['status'] = 'success'
        return jsonify(kwargs)

    @staticmethod
    def fail(**kwargs):
        kwargs['status'] = 'failure'
        return jsonify(kwargs)


class RecordAPIResource(APIResource):
    """
    API resource for single record
    """

    def __init__(self, slug):
        super(RecordAPIResource, self).__init__(slug)
        self.doc = Document(slug)

    def get(self, identifier):
        """
        :param identifier:
        :return:
         ---
         description: Returns a {slug} record
         ---
        """
        return jsonify({
            'schema': Schema().load(self.slug),
            'record': self.doc.read(identifier)
        })

    def delete(self, identifier):
        """
        :param identifier:
        :return:
         ---
         description: Deletes a {slug} record
         ---
        """
        self.doc.delete(identifier)
        return self.success()

    def put(self, identifier):
        """
        :param identifier:
        :return:
         ---
         description: Updates a {slug} record
         ---
        """
        data = request.get_json()
        update_result = self.doc.update(identifier, data)
        # Mongo 2.x does not return an update_result.modified_count - even though record is updated
        # This is breaking travis build, so we'll just check a document's been matched
        if update_result.matched_count == 1:
            return self.success(message="Record updated")
        else:
            return self.fail(message="Record not updated")


class ListAPIResource(APIResource):

    def get(self):
        """
        List records
        :return:
         ---
         description: List {slug} records
         ---
        """
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
            'schema': Schema().load(self.slug),
            'records': list(cursor)
        })

    def post(self):
        """
        Create a record
        :return:
         ---
         description: Creates a {slug} record
         ---
        """
        data = request.get_json()
        result = Document(self.slug).create(data)
        return self.success(inserted_id=result.inserted_id)


class SchemaAPIResource(APIResource):
    def get(self):
        schema = Schema().load(self.slug)
        return jsonify(schema)


class SchemaListAPIResource(Resource):
    """
    Resource for listing all available schemas
    """
    @staticmethod
    def get():
        schemas = Schema().load_all()
        return jsonify(schemas)
