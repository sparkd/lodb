#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '31/01/2017'.
"""

import datetime
from flask.json import JSONEncoder as FlaskJSONEncoder
from bson.objectid import ObjectId


class JSONEncoder(FlaskJSONEncoder):
    """
    Custom Encoder for BSON result sets
    Converts BSON ObjectId to string, to avoid TypeError: ObjectId() is not JSON serializable
    :param obj:
    :return: Encoded doc
    """
    def default(self, obj):
        if type(obj) == ObjectId:
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        return JSONEncoder.default(self, obj)


