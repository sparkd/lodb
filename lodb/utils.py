#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '26/01/2017'.
"""
import pytz
import datetime


def utc_timestamp():
    now = datetime.datetime.utcnow()
    return now.replace(tzinfo=pytz.utc)


class AttrDict(dict):
    """
    Dictionary with values accessible as an attribute
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

