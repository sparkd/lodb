#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '27/01/2017'.
"""


class SchemaParseError(Exception):
    """
    Raised when a JSON schema could not be parsed
    """


class DuplicateSlugError(Exception):
    """
    Raised when multiple schemas have the same slug
    """


