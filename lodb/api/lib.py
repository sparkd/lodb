#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""

import os
import glob
import json

from lodb.app import app


def list_schemas():
    schema_files = glob.glob(os.path.join(app.config['SCHEMA_DIR'], './*.json'))
    for schema_file in schema_files:
        with open(schema_file) as f:
            schema = json.load(f)
            print(schema)

        # print(schema_file)

    # print(schema_files)

if __name__ == '__main__':
    # with app.test_request_context('/'):
    with app.app_context():
        list_schemas()


