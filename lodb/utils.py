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

