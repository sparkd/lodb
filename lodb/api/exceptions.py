#!/usr/bin/env python
# encoding: utf-8
"""
Created by Ben Scott on '27/01/2017'.
"""


class APIException(Exception):
    """
    Base exception
    """
    __name__ = 'Error'
    status_code = 400

    def to_dict(self):
        return {self.__name__: str(self)}


class APIValidationException(APIException):
    """
    Raised when a JSON schema could not be parsed
    """
    __name__ = 'Validation error'

