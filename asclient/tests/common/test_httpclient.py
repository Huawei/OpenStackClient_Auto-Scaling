#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from asclient.tests import base
from asclient.common import httpclient

from keystoneauth1 import exceptions as exc
import mock


class TestHttpClient(base.BaseTestCase):

    def test_endpoint_override(self):
        endpoint_override = "http://baidu.com"
        client = httpclient.OpenStackHttpClient(mock.MagicMock(),
                                                endpoint=endpoint_override)
        self.assertEqual(client.endpoint_override, endpoint_override)

    @mock.patch("keystoneauth1.adapter.LegacyJsonAdapter.request")
    def test_convert_http_error(self, mocked):
        client = httpclient.OpenStackHttpClient(mock.MagicMock())

        mock_resp = mock.Mock()
        mock_resp.status_code = 413
        mock_resp.json.return_value = {
            'error_code': '413',
            'error_description': 'Request Entity Too Large',
        }
        mock_resp.headers = {
            'Content-Type': 'application/json',
            'x-openstack-request-id': mock.sentinel.fake_request_id,
            'retry-after': 10,
        }
        http_error = exc.from_response(mock_resp, 'POST', 'fake_url')
        mocked.side_effect = http_error
        self.assertRaises(exc.RequestEntityTooLarge, client.request)
