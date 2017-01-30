#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '29/01/2017'.
"""

from flask import current_app as app


def mongo_db(config_prefix='MONGO'):
    # print(app.extensions['pymongo'])
    client, db = app.extensions['pymongo'][config_prefix]
    return db


def mongo_get_collection(collection_name):
    """
    Get a collection ready for querying
    :param collection_name:
    :return: PyMongo Collection
    """
    return mongo_db()[collection_name]


def mongo_ensure_index(collection_name, field_name):
    """
    Create indexed if it doesn't exist - replaces deprecated pymongo.ensure_index
    :param collection_name:
    :param field_name:
    :return:
    """
    collection = mongo_get_collection(collection_name)
    if field_name not in collection.index_information():
        collection.create_index(field_name)
