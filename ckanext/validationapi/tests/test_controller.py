# encoding: utf-8

import json
import logging

from routes import url_for as url_for
import ckan.plugins as plugins
import ckan.tests.helpers as helpers

import ckanext.validationapi.error as error

LOG = logging.getLogger(__name__)
PLUGIN_NAME = 'validationapi'

class TestValidationController(helpers.FunctionalTestBase):

    def setup(self):
        super(TestValidationController, self).setup()
        if not plugins.plugin_loaded(PLUGIN_NAME):
            plugins.load(PLUGIN_NAME)
        self.validate_url = url_for(
            controller='ckanext.validationapi.controller:ValidationController',
            action='validate'
        )

    def teardown(self):
        plugins.unload(PLUGIN_NAME)

    def test_wrong_http_method_error(self):
        app = self._get_test_app()
        
        response = app.get(
            url=self.validate_url,
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_HTTP_METHOD_ERROR

    def test_wrong_content_type_error(self):
        app = self._get_test_app()

        response = app.post(
            url=self.validate_url,
            content_type="text/plain",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_CONTENT_TYPE_ERROR

    def test_no_request_body_error(self):
        app = self._get_test_app()

        response = app.post(
            url=self.validate_url,
            content_type="application/json",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.NO_REQUEST_DATA_ERROR

    def test_no_json_error(self):
        app = self._get_test_app()

        response = app.post(
            url=self.validate_url,
            content_type="application/json",
            params="this is not json",
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.CANNOT_DECODE_JSON_ERROR

    def test_no_json_object_error(self):
        app = self._get_test_app()

        response = app.post_json(
            url=self.validate_url,
            params='"this is not a json object"',
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_JSON_TYPE_ERROR

    def test_wrong_json_structure_error(self):
        app = self._get_test_app()

        response = app.post_json(
            url=self.validate_url,
            params={"this": "is not the right structure"},
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.WRONG_JSON_STRUCTURE_ERROR

    def test_unknown_validator_error(self):
        app = self._get_test_app()

        response = app.post_json(
            url=self.validate_url,
            params={"validator": "idontexist", "value": 5 },
            status=400
        )
        data = json.loads(str(response.body))
        assert data['error']['code'] is error.UNKNOWN_VALIDATOR_ERROR

