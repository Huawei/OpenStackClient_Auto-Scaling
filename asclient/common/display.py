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
from osc_lib import utils


class Display(object):
    """Provide functions for display resource"""

    # get columns used for listing resource(multiple records)
    # Resource inherit Display must override this field to specify
    # the columns which should be used when display resource list.
    # Return Examples: ("Column A", "columnb", "column c")
    list_column_names = ()

    # if not specified, will use list column names by default
    # get columns used for show resource(single record)
    show_column_names = list_column_names

    # column to resource property mapping
    column_2_property = {}

    def get_mapped_properties(self, column_names):
        """get mapped fields mapping to an exists field"""
        mapped = []
        for column_name in column_names:
            if column_name in self.column_2_property:
                mapped.append(self.column_2_property[column_name])
            else:
                mapped.append(column_name)
        return mapped

    def get_display_data(self, column_names, formatter=None):
        """get data mapped to column names

        column names will be auto transferred(convert to lowercase and
        blank with be replaced with underscore) to find mapping attributes
        example: "Attr A" --> attr_a, "Attr" --> "attr".
        ** all column names after transferred should be a property of resource

        :param formatter: column formatter
        :param column_names: columns to be returned
        :return: data mapping to column_names
        :rtype: tuple
        """
        properties = self.get_mapped_properties(column_names)
        return utils.get_item_properties(self,
                                         properties,
                                         formatters=formatter)
