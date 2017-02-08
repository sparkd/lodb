#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '01/02/2017'.
"""

import yaml
import inspect
from lodb.api.lib import list_resources


def get_swagger_docs(app):
    """
    Generate swaggers docs
    :param app:
    :return: swagger docs
    """
    docs = list()
    doc = {
        'paths': {},
        'info': {},
        'basePath': '',
        "swagger": "2.0"
    }
    for slug, endpoint, resource in list_resources(app):
        doc['paths'][endpoint] = {}
        # Loop through all the methods in the resources, and try and read
        # swagger yaml definition from the function docstring
        # If there's no do string, we won't add the function to the swagger definition
        for func_name, func in inspect.getmembers(resource, inspect.isfunction):
            swag_yaml = get_swagger_yaml(func.__doc__)
            if swag_yaml:
                endpoint_doc = {}
                for k, v in swag_yaml.items():
                    endpoint_doc[k] = v.format(slug=slug)
                func_args = inspect.signature(func)
                for func_arg in func_args.parameters:
                    if func_arg == 'self':
                        continue
                    endpoint_doc.setdefault('parameters', []).append({
                        "description": "{slug} {func_arg}".format(slug=slug, func_arg=func_arg),
                        "in": "path",
                        "name": "{func_arg}".format(func_arg=func_arg),
                        # FIXME: Get string type from path
                        "type": "uuid"
                    })

                endpoint_doc['responses'] = {
                    200: {
                        "description": slug,
                        "examples": {}
                    }
                }

                doc['paths'][endpoint][func_name] = endpoint_doc

    docs.append(doc)

    # api = get_api(app)
    # docs.append(api.get_swagger_doc())

    return docs


def get_swagger_yaml(docstring):
    separator = '---'
    if docstring and separator in docstring:
        swag_yaml_start = docstring.find(separator)
        swag_yaml_end = docstring.find(separator, swag_yaml_start + len(separator))
        yaml_doc = docstring[swag_yaml_start+len(separator):swag_yaml_end]
        try:
            return yaml.load(yaml_doc)
        except yaml.scanner.ScannerError:
            return False
