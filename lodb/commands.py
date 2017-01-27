# -*- coding: utf-8 -*-
"""Click commands.

"""

import click
import requests
from urllib.parse import urlparse


@click.command()
@click.argument('url')
def install_schema(url):
    """Import schema - either JSON schema or XSD to be converted to JSON schema """
    parsed_url = urlparse(url)
    # Is this a remote file
    if parsed_url.netloc:
        r = requests.get(url)
    else:
        print('LOCAL')
    # value = click.prompt('Please enter a valid integer', type=int, default=2)
    # print(value)
    print('hey')