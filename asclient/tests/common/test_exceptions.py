#   Copyright 2016 Huawei, Inc. All rights reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
from asclient.common import exceptions
from asclient.tests import base

from keystoneauth1 import exceptions as exc
import mock


class TestHTTPExceptions(base.BaseTestCase):

    def test_from_http_exception(self):
        mock_resp = mock.Mock()
        mock_resp.status_code = 413
        mock_resp.json.return_value = {
            "error": {
                'code': '413',
                'message': 'Request Entity Too Large',
            }
        }
        mock_resp.headers = {
            'Content-Type': 'application/json',
            'x-openstack-request-id': mock.sentinel.fake_request_id,
            'retry-after': 10,
        }
        http_error = exc.from_response(mock_resp, 'POST', 'fake_url')
        converted = exceptions.from_http_error(http_error)

        self.assertIsInstance(converted, exc.RequestEntityTooLarge)
        self.assertEqual(413, converted.http_status)
        self.assertEqual('POST', converted.method)
        self.assertEqual('fake_url', converted.url)
        self.assertEqual('[413] Request Entity Too Large', converted.message)
        self.assertEqual(0, converted.retry_after)
        self.assertEqual(mock.sentinel.fake_request_id, converted.request_id)

    def test_from_http_exception_with_no_body(self):
        mock_resp = mock.Mock()
        mock_resp.status_code = 404
        mock_resp.text = 'Text Message, Not Found'
        mock_resp.headers = {
            'Content-Type': 'text/plain',
            'x-openstack-request-id': mock.sentinel.fake_request_id,
            'retry-after': 10,
        }
        http_error = exc.from_response(mock_resp, 'POST', 'fake_url')
        converted = exceptions.from_http_error(http_error)

        self.assertIsInstance(converted, exc.NotFound)
        self.assertEqual(404, converted.http_status)
        self.assertEqual('POST', converted.method)
        self.assertEqual('fake_url', converted.url)
        self.assertEqual('Text Message, Not Found', converted.message)
        self.assertEqual(10, converted.retry_after)
        self.assertEqual(mock.sentinel.fake_request_id, converted.request_id)
