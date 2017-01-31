#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '30/01/2017'.
"""
from flask_restful import reqparse
from flask import current_app


def pagination_parser():
    """
    Pagination parser - extract limit and page from request parameters
    :return: dict - parsed arguments
    """
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('limit', type=int, help='Records per page', default=current_app.config['PAGINATION_DEFAULT_LIMIT'])
    request_parser.add_argument('page', type=int, help='Page number', default=1)
    args = request_parser.parse_args()

    # Ensure parameters do not exceed maximum limit
    if args['limit'] > current_app.config['PAGINATION_MAX_LIMIT']:
        args['limit'] = current_app.config['PAGINATION_MAX_LIMIT']

    return args

