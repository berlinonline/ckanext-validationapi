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

import ckanext.validationapi.error as error

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
                # The submitted value does validate:
                response_data = {
                    "success": True ,
                    "validator": validator_name ,
                    "value": original_value ,
                    "result": str(value)
                }
                return self._finish(200, response_data)
            else:
                raise error.WrongJSONStructure(
                    'JSON Request needs to contain a "validator" and a '
                    '"value" attribute.'
                )
        except Invalid, e:
            # The submitted value does not validate:
            response_data = {
                "success": False ,
                "validator": validator_name ,
                "value": original_value ,
                "message": str(e)
            }
            return self._finish(200, response_data)
        except error.ValidationError, e:
            # There was an error, validation could not be carried out:
            response_message = 'Bad Request - %s' % (e)
            response_data = {
                "success": False ,
                "validator": validator_name ,
                "value": original_value ,
                "error": {
                    "message": response_message ,
                    "code": e.error_code
                }
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
            num_args = len(args)
            if inspect.ismethod(validator):
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
                raise error.UnexpectedArguments(
                    "{} has an unexpected number of arguments: {}".format(validator_name, args)
                )
            return value
        except (UnknownValidator, TypeError), e:
            raise error.UnknownValidator(e)

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

        Originally inspired by ckan/controllers/api._get_request_data()
        '''

        request_data = None
        if request.method == 'POST':
            if request.content_type == 'application/json':
                try:
                    request_data = request.body
                except Exception, inst:
                    msg = "Could not extract request body data: %s" % \
                        (inst)
                    raise error.NoRequestDataFound(msg)
                if not request_data:
                    msg = "No request data found."
                    raise error.NoRequestDataFound(msg)
                try:
                    request_data = h.json.loads(request_data, encoding='utf8')
                except ValueError, e:
                    raise error.CannotDecodeJSON('Error decoding JSON data. '
                                     'Error: %r '
                                     'JSON data extracted from the request: %r' %
                                     (e, request_data))
                if not isinstance(request_data, dict):
                    raise error.WrongJSONType('Request data JSON decoded to %r but '
                                     'it needs to be a dictionary.' % request_data)
            else:
                raise error.WrongContentType(
                    "Validation API accepts only POST requests with "
                    "content type 'application/json'.")
        else:
            raise error.WrongHTTPMethod(
                "Validation API accepts only POST requests with "
                "content type 'application/json'.")

        return request_data

