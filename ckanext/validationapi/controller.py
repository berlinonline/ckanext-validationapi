# coding: utf-8
"""
This module implements the main controller for ckanext-validationapi.
"""

import inspect
import logging

from ckan.common import c, request, response
from ckan.logic import UnknownValidator
from ckan.plugins.toolkit import get_validator
import ckan.lib.base as base
import ckan.lib.helpers as h
from ckan.lib.navl.dictization_functions import Invalid

LOG = logging.getLogger(__name__)

class ValidationController(base.BaseController):
    """
    Main controller class for ckanext-validationapi.
    """

    def validate(self):
        """
        Main action of the ValidationController.

        Looks for "validator" and "value" in the JSON payload, tries
        to get and execute the validator and construct a JSON response
        based on its output.

        Errors are handled by returning a JSON document containing
        the error message.
        """
        validator_name = None
        original_value = None
        try:
            request_data = self._get_request_data()
            if 'validator' in request_data and 'value' in request_data:
                validator_name = request_data['validator']
                original_value = request_data['value']
                value = self.execute_validator(validator_name, request_data['value'])
                response_data = {
                    "success": True ,
                    "validator": validator_name ,
                    "value": original_value ,
                    "result": str(value)
                }
                return self._finish(200, response_data)
            else:
                raise ValueError(
                    'JSON Request needs to contain a "validator" and a '
                    '"value" attribute.'
                )
        except Invalid, e:
            response_data = {
                "success": False ,
                "validator": validator_name ,
                "value": original_value ,
                "message": str(e)
            }
            return self._finish(200, response_data)
        except ValueError, e:
            response_message = 'Bad Request - %s' % (e)
            response_data = {
                "success": False ,
                "validator": validator_name ,
                "value": original_value ,
                "message": response_message
            }
            return self._finish(400, response_data)

    def execute_validator(self, validator_name, value):
        """
        Execute a validator and return its output.

        Possible forms of validators are discussed here:
        https://docs.ckan.org/en/latest/extensions/adding-custom-fields.html#custom-validators

        a callable object taking a single parameter: validator(value)
        a callable object taking two parameters validator(value, context)
        a callable object taking four parameters: validator(key, flattened_data, errors, context)
        """
        try:
            validator = get_validator(validator_name)
            validator_signature = inspect.getargspec(validator)
            args = validator_signature[0]
            LOG.debug("{} args: {}".format(validator_name, args))
            num_args = len(args)
            if (inspect.ismethod(validator)):
                # if this is a method, we need to ignore the first
                # parameter (cls/self)
                num_args -= 1
            if num_args == 1:
                value = validator(value)
            elif num_args == 2:
                value = validator(value, c)
            elif num_args == 4:
                value = validator(value, {}, {}, c)
            else:
                raise ValueError(
                    "{} has an unexpected number of arguments: {}".format(validator_name, args)
                )
            return value
        except (UnknownValidator, TypeError), e:
            raise ValueError(e)

    def _finish(self, status_int, response_data=None):
        '''When a controller method has completed, call this method
        to prepare the response.
        @return response message - return this value from the controller
                                   method
                 e.g. return self._finish(404, 'Package not found')

        Shortened version of from ckan/controllers/api._finish()
        '''
        assert(isinstance(status_int, int))
        response.status_int = status_int
        response_msg = ''
        if response_data is not None:
            response.headers['Content-Type'] = 'application/json;charset=utf-8'
            response_msg = h.json.dumps(
                response_data,
                for_json=True)  # handle objects with for_json methods
        return response_msg

    def _get_request_data(self):
        '''Returns a dictionary, extracted from a request.

        Shortened version of ckan/controllers/api._get_request_data()
        '''

        request_data = None
        if request.method == 'POST' and request.content_type == 'application/json':
            try:
                request_data = request.body
            except Exception, inst:
                msg = "Could not extract request body data: %s" % \
                      (inst)
                raise ValueError(msg)
            if not request_data:
                msg = "Invalid request. Please use POST method" \
                    " for your request"
                raise ValueError(msg)
        if request_data and request.content_type != 'multipart/form-data':
            try:
                request_data = h.json.loads(request_data, encoding='utf8')
            except ValueError, e:
                raise ValueError('Error decoding JSON data. '
                                 'Error: %r '
                                 'JSON data extracted from the request: %r' %
                                 (e, request_data))
            if not isinstance(request_data, dict):
                raise ValueError('Request data JSON decoded to %r but '
                                 'it needs to be a dictionary.' % request_data)
        else:
            raise ValueError(
                "Validation API accepts only POST requests with "
                "content type 'application/json'.")

        return request_data

class SchemaError(Exception):
    """
    Errors when handling the JSON schema.
    """
