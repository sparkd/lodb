#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import os
import re
import glob
import json
from slugify import slugify
from flask import current_app as app

from lodb.exceptions import DuplicateSlugError

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


def schema_list(schema_dir):
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
            # If schema title doesn't exist, use the filename (minus the ext)
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
    # FIXME: Start up function, loads schema into mongo db
    # And validates them
    # TODO: Move into schema file
    with app.app_context():
        for slug, schema in schema_list(app.config['SCHEMA_DIR']).items():
            print(slug)



def schema_save():
    """
    Save the schema into mongo DB
    :return:
    """


def schema_diff():
    """
    Has the schema changed
    :return:
    """


def schema_load(slug):
    """
    Load a schema based on its slug
    :return:
    """