# -*- coding: utf-8 -*-
"""Click commands.

"""
import os
import json
import click
import requests
from flask.helpers import get_debug_flag
from xsdtojson import xsd_to_json_schema

# FIXME: This should get config from application context
from lodb.config import DevelopmentConfig, ProductionConfig
CONFIG = DevelopmentConfig if get_debug_flag() else ProductionConfig


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


@click.command()
@click.argument('uri')
def load_schema(uri):
    """Import schema - either JSON schema or XSD to be converted to JSON schema """
    file_name, file_ext = os.path.splitext(os.path.basename(uri))
    if file_ext != '.xsd':
        raise Exception('Only XSD files can be loaded at this point')
    parsed_url = urlparse(uri)
    # Is this a remote file
    if parsed_url.netloc:
        r = requests.get(uri)
        r.raise_for_status()
        json_schema = xsd_to_json_schema(r.content)
    else:
        json_schema = xsd_to_json_schema(uri)

    schema_file = os.path.join(CONFIG.SCHEMA_DIR, '{file_name}.schema.json'.format(file_name=file_name))
    # Write schema to file
    with open(schema_file, 'w') as f:
        f.write(json_schema + '\n')

