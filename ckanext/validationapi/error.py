# coding: utf-8
"""
This module implements various type of errors for ckanext-validationapi.
"""

import logging

LOG = logging.getLogger(__name__)
VALIDATION_ERROR = 0
WRONG_HTTP_METHOD_ERROR = 1
WRONG_CONTENT_TYPE_ERROR = 2
NO_REQUEST_DATA_ERROR = 3
CANNOT_DECODE_JSON_ERROR = 4
WRONG_JSON_TYPE_ERROR = 5
WRONG_JSON_STRUCTURE_ERROR = 6
UNKNOWN_VALIDATOR_ERROR = 7
UNEXPECTED_ARGUMENTS_ERROR = 8
OTHER_ERROR = 20


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
        self.error_code = WRONG_HTTP_METHOD_ERROR

class WrongContentType(ValidationError):
    """
    validationapi allows only content type 'application/json'.
    """

    def __init__(self, msg):
        super(WrongContentType, self).__init__(msg)
        self.error_code = WRONG_CONTENT_TYPE_ERROR

class NoRequestDataFound(ValidationError):
    """
    No data could be found in request body.
    """

    def __init__(self, msg):
        super(NoRequestDataFound, self).__init__(msg)
        self.error_code = NO_REQUEST_DATA_ERROR

class CannotDecodeJSON(ValidationError):
    """
    The request body could not be decoded to JSON.
    """

    def __init__(self, msg):
        super(CannotDecodeJSON, self).__init__(msg)
        self.error_code = CANNOT_DECODE_JSON_ERROR

class WrongJSONType(ValidationError):
    """
    There was JSON, but not an object.
    """

    def __init__(self, msg):
        super(WrongJSONType, self).__init__(msg)
        self.error_code = WRONG_JSON_TYPE_ERROR

class WrongJSONStructure(ValidationError):
    """
    The JSON payload does not contain "validator" and "value" attributes.
    """

    def __init__(self, msg):
        super(WrongJSONStructure, self).__init__(msg)
        self.error_code = WRONG_JSON_STRUCTURE_ERROR

class UnknownValidator(ValidationError):
    """
    The requested validator does not exist.
    """

    def __init__(self, msg):
        super(UnknownValidator, self).__init__(msg)
        self.error_code = UNKNOWN_VALIDATOR_ERROR

class UnexpectedArguments(ValidationError):
    """
    The validator function has an unexpected number of arguments.
    """

    def __init__(self, msg):
        super(UnexpectedArguments, self).__init__(msg)
        self.error_code = UNEXPECTED_ARGUMENTS_ERROR

class OtherError(ValidationError):
    """
    An unexpected error.
    """

    def __init__(self, msg):
        super(OtherError, self).__init__(msg)
        self.error_code = OTHER_ERROR



