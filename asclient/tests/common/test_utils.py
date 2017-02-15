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
from datetime import datetime
import time

from asclient.common import utils
from asclient.tests import base


class TestUtils(base.BaseTestCase):
    def test_get_id(self):
        self.assertEqual(4, utils.get_id(4))

        class TmpObject(object):
            uuid = 4

        self.assertEqual(4, utils.get_id(TmpObject))

    def test_remove_empty_from_dict(self):
        d = dict(k1=None, k2='', k3='abc')
        self.assertEqual({'k3': 'abc'}, utils.remove_empty_from_dict(d))

    def test_str_range(self):
        str_range = utils.str_range(1, 4)
        self.assertEqual(["1", "2", "3"], str_range)

    def test_time_format(self):
        # Unix timestamp mapped to yyyy-MM-dd HH:mm:ss
        dt = datetime(2017, 1, 22, hour=18, minute=25, second=10)
        longtime = time.mktime(dt.timetuple())
        formatted = utils.format_time(longtime)
        self.assertEqual(formatted, '2017-01-22 18:25:10')

        # if time-long is Unix millisecond timestamp
        formatted = utils.format_time(longtime * 1000)
        self.assertEqual(formatted, '2017-01-22 18:25:10')

        # None mapped to ''
        formatted = utils.format_time(None)
        self.assertEqual(formatted, '')
