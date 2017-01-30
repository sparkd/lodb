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
from flask import current_app as app
from jsonschema import Draft4Validator
from jsonschema.exceptions import SchemaError

from lodb.exceptions import DuplicateSlugError, SchemaParseError
from lodb.api.mongo import mongo_get_collection, mongo_ensure_index

re_title = re.compile('([\w-]+)\.')


def schema_get_title_from_path(schema_file_path):
    """
    Extract title from file name - matches string up to first full stop
    example.schema.json => example
    :param schema_file_path:
    :return:
    """
    filename = os.path.basename(schema_file_path)
    m = re_title.match(filename)
    return m.group(0)


def schema_file_list(schema_dir):
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
                schema['title'] = schema_get_title_from_path(schema_file)
            # Convert schema title to a slug - this will be used in the API URL
            slug = slugify(schema['title'])
            # As we're keying by slug, there is a chance of collisions
            # Check if a duplicate schema key exists, and if it does raise an Exception
            if slug in schemas:
                raise DuplicateSlugError(slug)
            # Keyed by slug
            schemas[slug] = schema

    return schemas


def schema_init():
    """
    Start up function, validates & loads schema into mongo db
    :return:
    """
    for slug, schema in schema_file_list(app.config['SCHEMA_DIR']).items():
        # Validate schema syntax
        try:
            Draft4Validator.check_schema(schema)
        except SchemaError:
            app.logger.error('Schema \'%s\' - invalid schema' % slug)
            raise SchemaParseError(slug)
        else:
            saved_schema = schema_load(slug)
            # If we have an existing saved schema, check if the new schema has changed
            # If it has, we want to save a copy of the new schema so changed can be traced
            if saved_schema:
                if schema_diff(schema, saved_schema):
                    app.logger.error('New version of schema \'%s\' detected - updating saved schema' % slug)
                    schema_save(slug, schema)
            else:
                schema_save(slug, schema)

    # Add created_at & slug indexes if they don't already exist
    mongo_ensure_index('schema', 'created_at')
    mongo_ensure_index('schema', 'slug')


def schema_save(slug, schema):
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
    mongo_get_collection('schema').insert_one(data)


def schema_diff(schema, saved_schema):
    """
    Calculate the difference between two schemas
    :return: bool
    """
    # To compare, convert both to JSON with sorted keys - these can
    # then be used in basic string comparison
    return json.dumps(schema, sort_keys=True) != json.dumps(saved_schema, sort_keys=True)


def schema_load(slug):
    """
    Load current version of schema
    :param slug:
    :return: JSON Schema
    """
    record = mongo_get_collection('schema').find_one({'slug': slug}, sort=[("created_at", pymongo.DESCENDING)])
    return record.get('schema') if record else None


def schema_load_all():
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

    records = mongo_get_collection('schema').group(
        key={"slug": 1},
        initial={},
        condition={},
        reduce=map_reduce
    )
    # Dict comprehension - build dict of schema definitions keyed by slug
    return {r.get('slug'): r.get('schema') for r in records}
