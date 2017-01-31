#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import jsonschema
from flask import request, current_app, jsonify
from flask_restful import Resource, reqparse
import json

from lodb.api.schema import schema_load
from lodb.api.mongo import mongo_get_collection, mongo_query_collection
from lodb.parsers import pagination_parser
# from lodb.encoders import BSONEncoder

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
        self.schema = schema_load(slug)
        self.collection = mongo_get_collection(slug)


class RecordAPIResource(APIResource):
    """
    API resource for single record
    """

    # FIXME: Add validator decorator - http://stackoverflow.com/questions/24238743/flask-decorator-to-verify-json-and-json-schema
    # Pagination: https://github.com/postrational/rest_api_demo/blob/master/rest_api_demo/api/blog/parsers.py

    def get(self, id):
        # MONGO: find one or 404
        return id

    def delete(self, id):
        return id

    def put(self, id):
        return id


class ListAPIResource(APIResource):

    def get(self):
        pagination = pagination_parser()
        # Convert page and limit to skip and limit
        query_args = dict(limit=pagination['limit'])
        # If page is greater than 1, then skip x records
        if pagination['page'] > 1:
            query_args['skip'] = (pagination['page']-1)*pagination['limit']

        # Query MongoDB - gets result cursor
        cursor = mongo_query_collection(self.slug, query_args)

        # return json.dumps(list(cursor), default=BSONEncoder)

        # Return JSON dict of records and total
        return jsonify({
            'total': cursor.count(),
            'records': list(cursor)
        })

    def post(self):
        data = request.get_json(silent=True)
        try:
            jsonschema.validate(data, self.schema)
        except jsonschema.exceptions.ValidationError:
            raise
        else:
            # FIXME: Handle errors, and responses
            # FIXME: Look at https://github.com/nathancahill/flask-inputs
            # FIXME: Look at https://github.com/xmm/flask-restful-example
            # FIXME: https://github.com/zalando/connexion
            try:
                result = self.collection.insert(data)
            except Exception as e:
                current_app.logger.error(e)
            else:
                current_app.logger.info('Record %s(%s) inserted', self.slug, data['_id'])

        return 'create'


class SchemaAPIResource(APIResource):
    def get(self):
        return self.schema


class SchemaListAPIResource(APIResource):
    """
    List all api resources
    """
    def get(self):
        return self.schema