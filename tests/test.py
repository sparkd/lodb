from nose.tools import assert_equal
import json
import os

from jsonschema import Draft4Validator
from lodb.application import app_factory
from lodb.config import TestConfig


class TestClient(object):
    """
    Base test client - sets up app client and adds helper functions for get, post etc
    """
    @classmethod
    def setup_class(cls):
        """This method is run once for each class before any tests are run"""
        cls.app = app_factory(TestConfig).test_client()
        cls.schema_slug = 'test'
        cls.data_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'data')

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

    def _call(self, method, endpoint, **kwargs):
        func = getattr(self.app, method)
        status_code = kwargs.pop('status_code', 200)
        response = func(endpoint, **kwargs)
        assert_equal(response.status_code, status_code)
        return self._response_to_json(response)

    @staticmethod
    def _assert_success(response):
        assert_equal(response['status'], 'success')