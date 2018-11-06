# coding: utf-8
"""
This module implements various type of errors for ckanext-validationapi.
"""

import logging

LOG = logging.getLogger(__name__)

class ValidationError(Exception):
    """
    Generic class for validation errors.
    """

    def error_code(self):
        return self.error_code

class WrongHTTPMethod(ValidationError):
    """
    validationapi allows only HTTP POST.
    """

    def __init__(self, msg):
        super(WrongHTTPMethod, self).__init__(msg)
        self.error_code = 1

class WrongContentType(ValidationError):
    """
    validationapi allows only content type 'application/json'.
    """

    def __init__(self, msg):
        super(WrongContentType, self).__init__(msg)
        self.error_code = 2

class NoRequestDataFound(ValidationError):
    """
    No data could be found in request body.
    """

    def __init__(self, msg):
        super(NoRequestDataFound, self).__init__(msg)
        self.error_code = 3

class CannotDecodeJSON(ValidationError):
    """
    The request body could not be decoded to JSON.
    """

    def __init__(self, msg):
        super(CannotDecodeJSON, self).__init__(msg)
        self.error_code = 4

class WrongJSONType(ValidationError):
    """
    There was JSON, but not an object.
    """

    def __init__(self, msg):
        super(WrongJSONType, self).__init__(msg)
        self.error_code = 5

class WrongJSONStructure(ValidationError):
    """
    The JSON payload does not contain "validator" and "value" attributes.
    """

    def __init__(self, msg):
        super(WrongJSONStructure, self).__init__(msg)
        self.error_code = 6

class UnknownValidator(ValidationError):
    """
    The requested validator does not exist.
    """

    def __init__(self, msg):
        super(UnknownValidator, self).__init__(msg)
        self.error_code = 7

class UnexpectedArguments(ValidationError):
    """
    The validator function has an unexpected number of arguments.
    """

    def __init__(self, msg):
        super(UnexpectedArguments, self).__init__(msg)
        self.error_code = 8

class OtherError(ValidationError):
    """
    An unexpected error.
    """

    def __init__(self, msg):
        super(OtherError, self).__init__(msg)
        self.error_code = 20



