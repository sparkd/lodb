#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import os
import re
import glob
import json
import pymongo
from bson.code import Code
from slugify import slugify
from datetime import datetime
from flask import current_app
from jsonschema import Draft4Validator
from jsonschema.exceptions import SchemaError

# from lodb.api.mongo import mongo_get_collection, mongo_ensure_index

from lodb.api.collection import Collection


class Schema(object):

    re_title = re.compile('([\w-]+)')

    @property
    def collection(self):
        return Collection('schema')

    def list_files(self, schema_dir):
        """
        Return a list of schemas, keyed by file name (known unique value)
        :return:
        """
        schemas = {}
        schema_files = glob.glob(os.path.join(schema_dir, './*.json'))

        for schema_file in schema_files:
            with open(schema_file) as f:
                # Load the JSON Schema file
                schema = json.load(f)
                # If schema title doesn't exist, use the filename (minus the extension)
                if not schema.get('title'):
                    schema['title'] = self._schema_get_title_from_path(schema_file)
                # Convert schema title to a slug - this will be used in the API URL
                slug = slugify(schema['title'])
                # As we're keying by slug, there is a chance of collisions
                # Check if a duplicate schema key exists, and if it does raise an Exception
                if slug in schemas:
                    raise Exception('Duplicate slug %s' % slug)
                # Keyed by slug
                schemas[slug] = schema

        return schemas

    def _schema_get_title_from_path(self, schema_file_path):
        """
        Extract title from file name - matches string up to first full stop
        example.schema.json => example
        :param schema_file_path:
        :return:
        """
        filename = os.path.basename(schema_file_path)
        m = self.re_title.match(filename)
        return m.group(0)

    def build(self):
        """
        Start up function, validates & loads schema into mongo db
        :return:
        """
        for slug, schema in self.list_files(current_app.config['SCHEMA_DIR']).items():
            # Validate schema syntax
            try:
                Draft4Validator.check_schema(schema)
            except SchemaError:
                current_app.logger.error('Schema \'%s\' - invalid schema' % slug)
                raise Exception('Invalid schema %s' % slug)
            else:
                saved_schema = self.load(slug)
                # If we have an existing saved schema, check if the new schema has changed
                # If it has, we want to save a copy of the new schema so changed can be traced
                if saved_schema:
                    if self.is_diff(schema, saved_schema):
                        current_app.logger.error('New version of schema \'%s\' detected - updating saved schema' % slug)
                        self.save(slug, schema)
                else:
                    self.save(slug, schema)

        # Add created_at & slug indexes if they don't already exist
        for idx in ['created_at', 'slug']:
            self.collection.create_index_if_not_exists(idx)

    def save(self, slug, schema):
        """
        Save schema into mongo DB, with associated metadata
        :param slug:
        :param schema:
        :return: None
        """
        data = {
            'slug': slug,
            'schema': schema,
            'created_at': datetime.now()
        }
        self.collection.insert_one(data)

    @staticmethod
    def is_diff(a, b):
        """
        Compare the difference between two schemas
        :return: bool
        """
        # To compare, convert both to JSON with sorted keys - these can
        # then be used in basic string comparison
        return json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True)

    def load(self, slug):
        """
        Load current version of schema
        :param slug:
        :return: JSON Schema
        """
        record = self.collection.find_one({'slug': slug}, sort=[("created_at", pymongo.DESCENDING)])
        return record.get('schema') if record else None

    def load_all(self):
        """
        Load all schemas, keyed by slugged and only the most recent version
        :return: dict
        """
        # Map reduce function for the group method - adds in schema to the results
        map_reduce = Code("""
            function (curr, result) {
                result.schema = curr.schema
            }
        """)

        records = self.collection.group(
            key={"slug": 1},
            initial={},
            condition={},
            reduce=map_reduce
        )
        # Dict comprehension - build dict of schema definitions keyed by slug
        return {r.get('slug'): r.get('schema') for r in records}
