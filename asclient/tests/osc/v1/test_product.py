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

from asclient.osc.v1 import product
from asclient.tests import base
from asclient.v1 import product_mgr
from asclient.v1 import resource


class TestProductList(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestProductList, self).setUp()
        self.cmd = product.ListProduct(self.app, None)

    @mock.patch.object(product_mgr.ProductManager, "_list")
    def test_product_list(self, mocked_list):
        self.check_parser(self.cmd, [], ())
        products = [
            {
                "product_id": "workspace.c2.large.windows",
                "flavor_id": "computev2-2",
                "type": "BASE",
                "descriptions": "desc1"
            },
            {
                "product_id": "workspace.c2.xlarge.windows",
                "flavor_id": "computev2-3",
                "type": "BASE",
                "descriptions": "desc2"
            }
        ]
        mocked_list.return_value = [resource.Product(None, p, attached=True)
                                    for p in products]
        columns, data = self.cmd.take_action(None)
        mocked_list.assert_called_once_with("/products", key='products')
        self.assertEquals(resource.Product.list_column_names, columns)
        expected = [
            ("workspace.c2.large.windows", "computev2-2", "BASE", "desc1"),
            ("workspace.c2.xlarge.windows", "computev2-3", "BASE", "desc2"),
        ]
        self.assertEquals(expected, data)
