# -*- coding: utf-8 -*-
"""Click commands.

"""

import click


@click.command()
def schema():
    """Import schema."""
    print('IMPORT')
