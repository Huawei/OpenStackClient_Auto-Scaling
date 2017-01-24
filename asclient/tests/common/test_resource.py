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
import six
from asclient.common import resource
from asclient.tests import base
from asclient.tests import fakes
from mock import mock


class SampleResource(resource.Resource):
    pass


class TestResource(base.BaseTestCase):
    def test_resource_repr(self):
        r = SampleResource(None, dict(foo='bar', baz='spam'))
        self.assertEqual('<SampleResource baz=spam, foo=bar>', repr(r))

    def test_init_with_attribute_info(self):
        r = SampleResource(None, dict(foo='bar', baz='spam'))
        self.assertTrue(hasattr(r, 'foo'))
        self.assertEqual('bar', r.foo)
        self.assertTrue(hasattr(r, 'baz'))
        self.assertEqual('spam', r.baz)

    def test_resource_lazy_getattr(self):
        fake_manager = mock.Mock()
        return_resource = SampleResource(None, dict(uuid=mock.sentinel.fake_id,
                                                    foo='bar',
                                                    name='fake_name'))
        fake_manager.get.return_value = return_resource

        r = SampleResource(fake_manager,
                           dict(uuid=mock.sentinel.fake_id, foo='bar'))
        self.assertTrue(hasattr(r, 'foo'))
        self.assertEqual('bar', r.foo)
        self.assertFalse(r.has_attached())

        # Trigger load
        self.assertEqual('fake_name', r.name)
        fake_manager.get.assert_called_once_with(mock.sentinel.fake_id)
        self.assertTrue(r.has_attached())

        # Missing stuff still fails after a second get
        self.assertRaises(AttributeError, getattr, r, 'abc')

    def test_eq(self):
        # Two resources of the same type with the same id: not equal
        r1 = SampleResource(None, {'id': 1, 'name': 'hi'})
        r2 = SampleResource(None, {'id': 1, 'name': 'hello'})
        self.assertNotEqual(r1, r2)

        # Two resources of different types: never equal
        r1 = SampleResource(None, {'id': 1})
        r2 = fakes.FakeResource(None, {'id': 1})
        self.assertNotEqual(r1, r2)

        # Two resources with no ID: equal if their info is equal
        r1 = SampleResource(None, {'name': 'joe', 'age': 12})
        r2 = SampleResource(None, {'name': 'joe', 'age': 12})
        self.assertEqual(r1, r2)

    def test_resource_object_with_request_id(self):
        resp_obj = fakes.create_response()
        r = SampleResource(None, {'name': '1'}, resp=resp_obj)
        self.assertEqual(fakes.FAKE_REQUEST_ID, r.request_id)

    def test_resource_object_with_compute_request_id(self):
        resp_obj = fakes.create_response_with_compute_header()
        r = SampleResource(None, {'name': '1'}, resp=resp_obj)
        self.assertEqual(fakes.FAKE_REQUEST_ID, r.request_id)


class ListWithMetaTest(base.BaseTestCase):
    def test_list_with_meta(self):
        resp = fakes.create_response()
        obj = resource.ListWithMeta([], resp)
        self.assertEqual([], obj)
        # Check request_ids attribute is added to obj
        self.assertTrue(hasattr(obj, 'request_id'))
        self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)


class DictWithMetaTest(base.BaseTestCase):
    def test_dict_with_meta(self):
        resp = fakes.create_response()
        obj = resource.DictWithMeta({}, resp)
        self.assertEqual({}, obj)
        # Check request_id attribute is added to obj
        self.assertTrue(hasattr(obj, 'request_id'))
        self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)


class TupleWithMetaTest(base.BaseTestCase):
    def test_tuple_with_meta(self):
        resp = fakes.create_response()
        expected_tuple = (1, 2)
        obj = resource.TupleWithMeta(expected_tuple, resp)
        self.assertEqual(expected_tuple, obj)
        # Check request_id attribute is added to obj
        self.assertTrue(hasattr(obj, 'request_id'))
        self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)


class StrWithMetaTest(base.BaseTestCase):
    def test_str_with_meta(self):
        resp = fakes.create_response()
        obj = resource.StrWithMeta('test-str', resp)
        self.assertEqual('test-str', obj)
        # Check request_id attribute is added to obj
        self.assertTrue(hasattr(obj, 'request_id'))
        self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)


class BytesWithMetaTest(base.BaseTestCase):
    def test_bytes_with_meta(self):
        resp = fakes.create_response()
        obj = resource.BytesWithMeta(b'test-bytes', resp)
        self.assertEqual(b'test-bytes', obj)
        # Check request_id attribute is added to obj
        self.assertTrue(hasattr(obj, 'request_id'))
        self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)


if six.PY2:
    class UnicodeWithMetaTest(base.BaseTestCase):
        def test_unicode_with_meta(self):
            resp = fakes.create_response()
            obj = resource.UnicodeWithMeta(u'test-unicode', resp)
            self.assertEqual(u'test-unicode', obj)
            # Check request_id attribute is added to obj
            self.assertTrue(hasattr(obj, 'request_id'))
            self.assertEqual(fakes.FAKE_REQUEST_ID, obj.request_id)
