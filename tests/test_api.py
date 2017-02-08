from nose.tools import assert_equal, assert_true
import json
import os

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

    def _post(self, endpoint, **kwargs):
        return self._call('post', endpoint, **kwargs)

    def _get(self, endpoint, **kwargs):
        return self._call('get', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._call('put', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._call('delete', endpoint, **kwargs)

    def _call(self, method, endpoint, status_code=200, **kwargs):
        func = getattr(self.app, method)
        response = func(endpoint, **kwargs)
        assert_equal(response.status_code, status_code)
        return self._response_to_json(response)

    @staticmethod
    def _assert_success(response):
        assert_equal(response['status'], 'success')

    def test_api_schema_endpoint_exists(self):
        """ Test schema endpoint exists """
        response = self.app.get('/api/%s.schema.json' % self.schema_slug)
        assert_equal(response.status_code, 200)

    def test_api_schema_endpoint_returns_valid_json_schema(self):
        """ Test schema returns valid json """
        response = self.app.get('/api/%s.schema.json' % self.schema_slug)
        schema = self._response_to_json(response)
        Draft4Validator(schema)

    def test_api_schema_list_returns_schemas(self):
        """ Test schema list returns schemas """
        response = self.app.get('/api/')
        schemas = self._response_to_json(response)
        assert_true(self.schema_slug in schemas.keys())

    def test_api_creating_record_instance(self):
        data = self._read_data_file('test-valid.json')
        response = self._post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
        self._assert_success(response)

    def test_api_reading_record_instance(self):
        # Create a record
        data = self._read_data_file('test-valid.json')
        creating_response = self._post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
        # Then get the same record, using inserted_id
        response = self._get('/api/%s/%s/' % (self.schema_slug, creating_response.get('inserted_id')), content_type='application/json')
        assert_equal(creating_response.get('inserted_id'), response.get('record').get('_id'))

    def test_api_updating_record_instance(self):
        data = self._read_data_file('test-valid.json')
        creating_response = self._post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
        # Change the data array
        data['price'] = 5
        data['name'] = 'Oranges'
        update_response = self._put('/api/%s/%s/' % (self.schema_slug, creating_response.get('inserted_id')), data=json.dumps(data), content_type='application/json')
        self._assert_success(update_response)
        # Load the record and check the values have been updated
        response = self._get('/api/%s/%s/' % (self.schema_slug, creating_response.get('inserted_id')), content_type='application/json')
        record = response.get('record')
        assert_equal(creating_response.get('inserted_id'), record.get('_id'))
        assert_equal(record['price'], data['price'])
        assert_equal(record['name'], data['name'])

    def test_api_deleting_record_instance(self):
        data = self._read_data_file('test-valid.json')
        creating_response = self._post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
        # Delete the record
        delete_response = self._delete('/api/%s/%s/' % (self.schema_slug, creating_response.get('inserted_id')), content_type='application/json')
        self._assert_success(delete_response)
        # Make sure the record has been deleted - trying to get it should return 404
        response = self.app.get('/api/%s/%s/' % (self.schema_slug, creating_response.get('inserted_id')), content_type='application/json')
        assert_equal(response.status_code, 404)

    def test_api_listing_records(self):
        response = self._get('/api/%s/' % self.schema_slug)
        assert_equal(sorted(['total', 'records', 'schema']), sorted(list(response.keys())))
