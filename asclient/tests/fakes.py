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
import mock

from oslo_serialization import jsonutils
from requests import Response

from asclient.common import display
from asclient.common import manager
from asclient.common import resource as r
from asclient.common import utils


# fake request id
FAKE_REQUEST_ID = 'req-0594c66b-6973-405c-ae2c-43fcfc00f2e3'

# fake resource id
FAKE_RESOURCE_ID = '0594c66b-6973-405c-ae2c-43fcfc00f2e3'
FAKE_RESOURCE_NAME = 'name-0594c66b-6973-405c-ae2c-43fcfc00f2e3'

# fake resource response key
FAKE_RESOURCE_ITEM_URL = '/resources/%s'
FAKE_RESOURCE_COLLECTION_URL = '/resources'


def create_response(json=None):
    resp = Response()
    resp.headers['x-openstack-request-id'] = FAKE_REQUEST_ID
    if json:
        resp.json = mock.MagicMock()
        resp.json.return_value = json
    return resp


def create_response_with_compute_header():
    resp = Response()
    resp.headers['x-compute-request-id'] = FAKE_REQUEST_ID
    return resp


class FakeResource(r.Resource, display.Display):
    pass


class FakeManager(manager.Manager):
    resource_class = FakeResource

    def __init__(self, http_client=None):
        super(FakeManager, self).__init__(http_client)

    def get(self, resource, **kwargs):
        resource_url = FAKE_RESOURCE_ITEM_URL % utils.get_id(resource)
        return self._get(resource_url, **kwargs)

    def list(self):
        return self._list(FAKE_RESOURCE_COLLECTION_URL, key='resources')

    def update(self, resource, **kwargs):
        return self._update(FAKE_RESOURCE_ITEM_URL % utils.get_id(resource),
                            resource,
                            **kwargs)

    def update_all(self, resource, **kwargs):
        resource_url = FAKE_RESOURCE_ITEM_URL % utils.get_id(resource)
        return self._update_all(resource_url, resource, **kwargs)

    def create(self, resource=None):
        return self._create(FAKE_RESOURCE_COLLECTION_URL, json=resource)

    def delete(self, resource):
        return self._delete(FAKE_RESOURCE_ITEM_URL % utils.get_id(resource))


class FakeRaw(object):
    version = 110


class FakeHTTPResponse(object):
    version = 1.1

    def __init__(self, status_code, reason, headers, content):
        self.headers = headers
        self.content = content
        self.status_code = status_code
        self.reason = reason
        self.raw = FakeRaw()

    def getheader(self, name, default=None):
        return self.headers.get(name, default)

    def getheaders(self):
        return self.headers.items()

    def read(self, amt=None):
        b = self.content
        self.content = None
        return b

    def iter_content(self, chunksize):
        return self.content

    def json(self):
        return jsonutils.loads(self.content)


class FakeWorkspaceV1Client(object):

    def __init__(self, **kwargs):
        self.client = mock.Mock()
