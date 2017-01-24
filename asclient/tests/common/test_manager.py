#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import mock
import six

from asclient.common import httpclient
from asclient.common import resource
from asclient.tests import base
from asclient.tests import fakes


class TestManager(base.BaseTestCase):
    _headers = {"Accept": "application/json"}

    def __init__(self, *args, **kwargs):
        super(TestManager, self).__init__(*args, **kwargs)
        self.instance = None
        self.resource = None
        self.manager = None

    def setUp(self):
        super(TestManager, self).setUp()
        http_client = httpclient.OpenStackHttpClient(mock.MagicMock())
        self.manager = fakes.FakeManager(http_client)
        self.instance = dict(uuid=fakes.FAKE_RESOURCE_ID,
                             name=fakes.FAKE_RESOURCE_NAME)
        self.resource = fakes.FakeResource(None, self.instance)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_get(self, mocked):
        mocked.return_value = fakes.create_response(self.instance)
        result = self.manager.get(self.resource)

        self.assertTrue(result.has_attached())
        self.assertIsInstance(result, resource.Resource)
        expect_url = (fakes.FAKE_RESOURCE_ITEM_URL % fakes.FAKE_RESOURCE_ID)
        mocked.assert_called_once_with(expect_url,
                                       "GET",
                                       params={},
                                       headers=self._headers)

        result = self.manager.get(self.resource, raw=True)
        self.assertIsInstance(result, resource.DictWithMeta)
        self.assertEqual(result, self.instance)

        # return None
        resp = fakes.create_response()
        mocked.return_value = resp
        result = self.manager.get(self.resource)
        self.assertEqual(result, resp.text)
        self.assertIsInstance(result, resource.StrWithMeta)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_list(self, mocked):
        json = {"resources": [self.instance]}
        mocked.return_value = fakes.create_response(json)
        result = self.manager.list()
        self.assertEqual(1, len(result))
        self.assertEqual([self.resource], result)
        self.assertIsInstance(result, resource.ListWithMeta)
        self.assertIsInstance(result[0], fakes.FakeResource)
        expect_url = fakes.FAKE_RESOURCE_COLLECTION_URL
        mocked.assert_called_once_with(expect_url,
                                       "GET",
                                       headers=self._headers,
                                       params={})

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_list_return_string(self, mocked):
        json = {"resources": ["a", "b", "c"]}
        mocked.return_value = fakes.create_response(json)
        result = self.manager.list()
        self.assertEqual(3, len(result))
        self.assertEqual(json['resources'], result)
        self.assertIsInstance(result, resource.ListWithMeta)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_patch(self, mocked):
        mocked.return_value = fakes.create_response(self.instance)
        result = self.manager.update(self.resource)
        self.assertFalse(result.has_attached())
        self.assertIsInstance(result, fakes.FakeResource)
        expect_url = (fakes.FAKE_RESOURCE_ITEM_URL % fakes.FAKE_RESOURCE_ID)
        mocked.assert_called_once_with(expect_url,
                                       "PATCH",
                                       json=self.resource,
                                       headers=self._headers)

        # return raw
        result = self.manager.update(self.resource, raw=True)
        self.assertIsInstance(result, resource.DictWithMeta)
        self.assertEqual(result, self.instance)

        # return None
        resp = fakes.create_response()
        mocked.return_value = resp
        result = self.manager.update(self.resource)
        self.assertEqual(result, resp.text)
        self.assertIsInstance(result, resource.StrWithMeta)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_put(self, mocked):
        mocked.return_value = fakes.create_response(self.instance)
        result = self.manager.update_all(self.resource)
        self.assertFalse(result.has_attached())
        self.assertIsInstance(result, fakes.FakeResource)
        expect_url = (fakes.FAKE_RESOURCE_ITEM_URL % fakes.FAKE_RESOURCE_ID)
        mocked.assert_called_once_with(expect_url,
                                       "PUT",
                                       json=self.resource,
                                       headers=self._headers)
        # return raw
        result = self.manager.update_all(self.resource, raw=True)
        self.assertIsInstance(result, resource.DictWithMeta)
        self.assertEqual(result, self.instance)

        # return None
        resp = fakes.create_response()
        mocked.return_value = resp
        result = self.manager.update_all(self.resource)
        self.assertEqual(result, resp.text)
        self.assertIsInstance(result, resource.StrWithMeta)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_delete(self, mocked):
        mocked.return_value = fakes.create_response()
        result = self.manager.delete(self.resource)
        self.assertEqual(tuple(), result)
        self.assertIsInstance(result, resource.TupleWithMeta)
        expect_url = (fakes.FAKE_RESOURCE_ITEM_URL % fakes.FAKE_RESOURCE_ID)
        mocked.assert_called_once_with(expect_url,
                                       "DELETE",
                                       headers=self._headers)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_create(self, mocked):
        mocked.return_value = fakes.create_response(self.instance)
        result = self.manager.create(self.resource)
        self.assertIsInstance(result, fakes.FakeResource)
        self.assertEqual(result.original, self.instance)
        self.assertFalse(result.has_attached())
        expect_url = fakes.FAKE_RESOURCE_COLLECTION_URL
        mocked.assert_called_once_with(expect_url,
                                       "POST",
                                       json=self.resource,
                                       headers=self._headers)

        result = self.manager.create()
        mocked.assert_called_with(expect_url, "POST", headers=self._headers)

    @mock.patch("keystoneauth1.adapter.Adapter.request")
    def test_manager_create_return_none(self, mocked):
        mocked.return_value = fakes.create_response()
        result = self.manager.create(self.resource)
        self.assertIsInstance(result, resource.TupleWithMeta)
        self.assertEqual(result, ())
        expect_url = fakes.FAKE_RESOURCE_COLLECTION_URL
        mocked.assert_called_once_with(expect_url,
                                       "POST",
                                       json=self.resource,
                                       headers=self._headers)

    def test_mixin_meta(self):
        resp = fakes.create_response()

        text = self.manager.mixin_meta('text', resp)
        self.assertEqual('text', text)
        self.assertIsInstance(text, resource.StrWithMeta)

        text = self.manager.mixin_meta(u'text', resp)
        self.assertEqual('text', text)
        self.assertIsInstance(text, resource.UnicodeWithMeta)

        list_item = ['a', 'b', 'c']
        list_mixin = self.manager.mixin_meta(list_item, resp)
        self.assertEqual(list_item, list_mixin)
        self.assertIsInstance(list_mixin, resource.ListWithMeta)

        tuple_item = ('a', 'b', 'c')
        tuple_mixin = self.manager.mixin_meta(tuple_item, resp)
        self.assertEqual(tuple_item, tuple_mixin)
        self.assertIsInstance(tuple_mixin, resource.TupleWithMeta)

        byte_item = six.binary_type('abc')
        byte_mixin = self.manager.mixin_meta(byte_item, resp)
        self.assertEqual(byte_item, byte_mixin)
        if six.PY2:
            self.assertIsInstance(byte_mixin, resource.StrWithMeta)
        elif six.PY3:
            self.assertIsInstance(byte_mixin, resource.BytesWithMeta)
