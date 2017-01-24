#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from asclient.common import display
from asclient.common import resource
from asclient.tests import base


class DisplayResource(resource.Resource, display.Display):

    @property
    def computed(self):
        return self.column_a + self.columnb


class OverrideResource(resource.Resource, display.Display):

    show_column_names = ('column_a', 'columnb')
    list_column_names = ('column_a', 'columnb', 'column_array')


class TestDisplay(base.BaseTestCase):
    instance = {
        'column_a': 'A1',
        'columnb': 'B1',
        'column_array': [1, 2, 3],
        'column_dict': {
            'key1': 'value1',
            'key2': 1,
        }
    }

    def test_get_display_data_for_columns(self):
        # prepare resource
        instance = self.instance
        r = DisplayResource(None, instance, attached=True)

        column_names = ('Column A', 'Columnb', 'column_array', 'Column Dict',
                        'computed')
        data = r.get_display_data(column_names)
        self.assertEqual(data, (instance['column_a'],
                                instance['columnb'],
                                instance['column_array'],
                                instance['column_dict'],
                                (instance['column_a']+instance['columnb'])))

        column_names = ('column_array', 'Column Dict', 'Column A', 'Columnb',
                        'computed')
        data = r.get_display_data(column_names)
        self.assertEqual(data, (instance['column_array'],
                                instance['column_dict'],
                                instance['column_a'],
                                instance['columnb'],
                                (instance['column_a'] + instance['columnb'])))

        column_names = ('column_array', 'Column Dict', 'Column A',)
        data = r.get_display_data(column_names)
        self.assertEqual(data, (instance['column_array'],
                                instance['column_dict'],
                                instance['column_a'],))

    def test_default_column_names(self):
        # return empty tuple if not override _list_column_names
        self.assertEqual(len(DisplayResource.list_column_names), 0)
        self.assertEqual(len(DisplayResource.show_column_names), 0)
        self.assertEqual(DisplayResource.show_column_names, ())
        self.assertEqual(DisplayResource.list_column_names, ())

    def test_override_column_names(self):
        instance = self.instance
        r = OverrideResource(None, instance)

        # override list column names by property _list_column_names
        self.assertEqual(r.show_column_names, ('column_a', 'columnb'))
        self.assertEqual(r.list_column_names, ('column_a', 'columnb', 'column_array'))

