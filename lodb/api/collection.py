#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '29/01/2017'.
"""

from flask import abort, current_app
from pymongo import collection


class Collection(collection.Collection):
    """
    Custom sub-class of :class:`pymongo.collection.Collection` which automatically
    picks up the mongo db from flask extensions

    Has helper function  find_one_or_404: Find and return a single document, or raise a 404 Not Found
    """
    def __init__(self, name, config_prefix='MONGO'):
        """
        Initiate collection reference
        :param name: name of collection
        :param config_prefix:
        """
        client, database = current_app.extensions['pymongo'][config_prefix]
        super(Collection, self).__init__(database, name)

    def find_one_or_404(self, *args, **kwargs):
        """Find and return a single document, or raise a 404 Not Found
        exception if no document matches the query spec.
        """
        abort_message = kwargs.pop('abort_message', None)
        found = self.find_one(*args, **kwargs)
        if found is None:
            abort(404, abort_message)
        return found

    def create_index_if_not_exists(self, field_name):
        """
        Create index if it doesn't exist - replaces deprecated pymongo.ensure_index
        :param field_name:
        :return:
        """
        if field_name not in self.index_information():
            self.create_index(field_name)