# encoding: utf-8

import json
import logging
import pytest
import ckan.plugins as plugins
from ckan.plugins.toolkit import url_for

import ckanext.validationapi.error as error

LOG = logging.getLogger(__name__)
VALIDATOR_PLUGIN = 'validationapi'
TEST_VALIDATORS = 'weird_validators'

@pytest.mark.ckan_config('ckan.plugins', f"{VALIDATOR_PLUGIN} {TEST_VALIDATORS}")
@pytest.mark.usefixtures('with_plugins', 'clean_db')
class TestValidationController(object):

    def validate_url(self):
        return url_for('validationapi.validate')

    # -----------
    # Error Tests
    # -----------

    def test_wrong_http_method_error(self, app):
        response = app.get(
            url=self.validate_url(),
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_HTTP_METHOD_ERROR

    def test_wrong_content_type_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="text/plain",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_CONTENT_TYPE_ERROR

    def test_no_request_body_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.NO_REQUEST_DATA_ERROR

    def test_no_json_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params="this is not json",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.CANNOT_DECODE_JSON_ERROR

    def test_no_json_object_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params='"this is not a json object"',
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_JSON_TYPE_ERROR

    def test_wrong_json_structure_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params=json.dumps({'this': 'is not the right structure'}),
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_JSON_STRUCTURE_ERROR

    def test_unknown_validator_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params=json.dumps({'validator': 'idontexist', 'value': 5 }),
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.UNKNOWN_VALIDATOR_ERROR

    def test_unexpected_arguments_error(self, app):
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params=json.dumps({'validator': 'three_is_neither_two_nor_four', 'value': 'WUT?'}),
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.UNEXPECTED_ARGUMENTS_ERROR

    # -------------
    # Success Tests
    # -------------

    @pytest.mark.parametrize("data", [
        {'validator_name': 'int_validator', 'submitted_value': 42, 'expected_result': str(42)},
        {'validator_name': 'boolean_validator',
            'submitted_value': True, 'expected_result': str(True)},
        {'validator_name': 'email_validator', 'submitted_value': 'jane.doe@company.com',
            'expected_result': 'jane.doe@company.com'},
        {'validator_name': 'isodate', 'submitted_value': '2018-11-07',
            'expected_result': '2018-11-07 00:00:00'},
        {'validator_name': 'foolidator', 'submitted_value': 'WUT?',
            'expected_result': 'FOOOO ---> WUT? <--- BAAAAR'},
        {'validator_name': 'vier_ist_trumpf', 'submitted_value': 'WUT?', 'expected_result': 'Hurra!'},
    ])
    def test_valid_value_returns_200_with_correct_structure(self, app, data):
        validator_name = data['validator_name']
        submitted_value = data['submitted_value']
        expected_result = data['expected_result']
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params=json.dumps({'validator': validator_name, 'value': submitted_value}),
            status=200
        )
        data = json.loads(str(response.body))
        assert data['validator'] == validator_name
        assert data['success'] is True
        assert data['value'] == submitted_value
        assert data['result'] == expected_result

    @pytest.mark.parametrize("data", [
        {'validator_name': 'int_validator', 'submitted_value': '42x'},
        {'validator_name': 'email_validator', 'submitted_value': 'jane.doeATcompany.com'},
        {'validator_name': 'isodate', 'submitted_value': '2018-13-07'},
    ])
    def test_invalid_value_returns_200_with_correct_structure(self, app, data):
        validator_name = data['validator_name']
        submitted_value = data['submitted_value']
        response = app.post(
            url=self.validate_url(),
            content_type="application/json",
            params=json.dumps({ 'validator': validator_name, 'value': submitted_value }),
            status=200
        )
        data = json.loads(str(response.body))
        assert data['validator'] == validator_name
        assert data['success'] is False
        assert data['value'] == submitted_value

# import json
# import logging

# from routes import url_for as url_for
# import ckan.plugins as plugins
# import ckan.tests.helpers as helpers

# import ckanext.validationapi.error as error


# class TestValidationController(helpers.FunctionalTestBase):

#     def setup(self):
#         super(TestValidationController, self).setup()
#         if not plugins.plugin_loaded(VALIDATOR_PLUGIN):
#             plugins.load(VALIDATOR_PLUGIN)
#         if not plugins.plugin_loaded(TEST_VALIDATORS):
#             plugins.load(TEST_VALIDATORS)
#         self.validate_url = url_for(
#             controller='ckanext.validationapi.controller:ValidationController',
#             action='validate'
#         )
#         self.app = self._get_test_app()


#     def teardown(self):
#         plugins.unload(VALIDATOR_PLUGIN)
#         plugins.unload(TEST_VALIDATORS)






