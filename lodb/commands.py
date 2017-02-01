# -*- coding: utf-8 -*-
"""Click commands.

"""

import click
import requests

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


@click.command()
@click.argument('uri')
def install_schema(uri):
    """Import schema - either JSON schema or XSD to be converted to JSON schema """
    parsed_url = urlparse(uri)
    # Is this a remote file
    if parsed_url.netloc:
        r = requests.get(uri)
    else:
        print('LOCAL')
    # value = click.prompt('Please enter a valid integer', type=int, default=2)
    # print(value)
    print('hey')
