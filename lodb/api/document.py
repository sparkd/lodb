#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '31/01/2017'.
"""

import bson
import jsonschema
from datetime import datetime
from flask import abort, current_app

from lodb.api.schema import Schema
from lodb.api.exceptions import APIException, APIValidationException
from lodb.api.collection import Collection
from lodb.utils import AttrDict


class Document(object):
    """
    CRUD Operations for Mongo Document
    """
    def __init__(self, slug):
        """
        Load the schema for the record
        :param slug: Schema slog
        """
        self.slug = slug
        self.schema = Schema().load(self.slug)
        self.collection = Collection(slug)

    def create(self, data):
        self.validate(data)
        self._timestamps(data, ['_created_on', '_updated_on'])
        try:
            result = self.collection.insert_one(data)
        except Exception as e:
            current_app.logger.error(e)
            raise APIException('Record could not be inserted')
        else:
            current_app.logger.info('Record %s(%s) inserted', self.slug, data['_id'])
            return result

    def read(self, identifier):
        # raise APIValidationException()
        try:
            return self.collection.find_one_or_404({'_id': bson.ObjectId(identifier)}, abort_message='Record not found')
        except bson.errors.InvalidId:
            abort(404, 'Record not found')

    def update(self, identifier, data):
        self.validate(data)
        record = self.read(identifier)
        # Add updated on date
        self._timestamps(data, ['_updated_on'])
        update_result = self.collection.update_one({'_id': bson.ObjectId(identifier)}, {'$set': data})
        # Mongo 2.* does not return an update_result
        # SO if we don't have an update result, load the record and check the _updated_on timestamp
        update_result = None

        if not update_result:
            updated_record = self.read(identifier)
            update_result = AttrDict(
                modified_count=1 if updated_record['_updated_on'] > record['_updated_on'] else 0
            )

        return update_result

    def delete(self, identifier):
        return self.collection.delete_one({'_id': bson.ObjectId(identifier)})

    def validate(self, data):
        """
        Validate data against schema
        Raise exception APIValidationException if validation fails
        :param data:
        :return:
        """
        try:
            jsonschema.validate(data, self.schema)
        except jsonschema.exceptions.ValidationError as err:
            msg = '{path}: {error}'.format(
                path=':'.join(err.path),
                error=err.message
            )
            raise APIValidationException(msg)

    @staticmethod
    def _timestamps(data, fields):
        for field in fields:
            data[field] = datetime.now()



