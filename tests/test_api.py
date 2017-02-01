from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from jsonschema import validate
from pathlib import Path
import jsonschema
import json
import os
import codecs


from jsonschema import Draft4Validator
from lodb.application import app_factory
from lodb.config import TestConfig


class TestAPISchema(object):
    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        cls.app = app_factory(TestConfig).test_client()
        cls.schema_slug = 'test'
        cls.data_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data')

    @classmethod
    def teardown_class(cls):
        """This method is run once for each class _after_ all tests are run"""

    def _read_data_file(self, filename):
        with open(os.path.join(self.data_dir, filename)) as data_json:
            return json.load(data_json)

    @staticmethod
    def _response_to_json(response):
        """
        Convert binary test_client response to JSON
        :param response:
        :return:
        """
        return json.loads(response.get_data(as_text=True))

    # def test_api_schema_endpoint_exists(self):
    #     """ Test validation via schema """
    #     response = self.app.get('/api/%s.schema.json' % self.schema_slug)
    #     assert_equal(response.status_code, 200)
    #
    # def test_api_schema_endpoint_returns_valid_json_schema(self):
    #     """ Test validation via schema """
    #     response = self.app.get('/api/%s.schema.json' % self.schema_slug)
    #     schema = self._response_to_json(response)
    #     Draft4Validator(schema)
    #
    # def test_api_creating_new_record_instance(self):
    #     data = self._read_data_file('test-valid.json')
    #     self.app.post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
    #
    # def test_api_updating_record_instance(self):
    #     pass
    #     # data = self._read_data_file('test-valid.json')
    #     # self.app.post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
    #
    # def test_api_deleting_record_instance(self):
    #     pass

    def test_api_listing_records(self):
        response = self.app.get('/api/%s/' % self.schema_slug)
        # json_response = self._response_to_json(response)
        # print(json_response)
        # pass