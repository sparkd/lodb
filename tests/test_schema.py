from nose.tools import assert_true
import json

from test import TestClient


class TestSchema(TestClient):

    def test_schema_validation_valid_data(self):
        """ Test validation via schema """
        data = self._read_data_file('test-valid.json')
        response = self._post('/api/%s/' % self.schema_slug, data=json.dumps(data), content_type='application/json')
        self._assert_success(response)

    def test_schema_validation_invalid_data(self):
        """ Test schema raises exception on invalid data """
        data = self._read_data_file('test-invalid.json')
        response = self._post('/api/%s/' % self.schema_slug, status_code=400, data=json.dumps(data), content_type='application/json')
        assert_true('Validation error' in response)

