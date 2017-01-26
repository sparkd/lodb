# -*- coding: utf-8 -*-
"""Click commands.

"""

import click


@click.command()
@click.argument('file')
def install_schema(file):
    """Import schema."""
    print(file)
