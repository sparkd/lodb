#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '01/02/2017'.
"""


def get_swagger_docs(app):

    # A list of swagger document objects
    docs = [
        {
            'tags': ['user'],
            'description': 'Returns a user',
            'parameters': [
                {
                    'name': 'user_id',
                    'description': 'User identifier',
                    'in': 'path',
                    'type': 'integer'
                }
            ],
            'responses': {
                '200': {
                    'description': 'User',
                    'examples': {
                        'application/json': {
                            'id': 1,
                            'name': 'somebody'
                        }
                    }
                }
            }
        }
    ]

    return docs


