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
import logging

from osc_lib.command import command

from asclient.common.i18n import _
from asclient.v1 import resource

LOG = logging.getLogger(__name__)


class ListProduct(command.Lister):
    _description = _("list product")

    def get_parser(self, prog_name):
        parser = super(ListProduct, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        products = client.products.list()
        columns = resource.Product.list_column_names
        outputs = [r.get_display_data(columns) for r in products]
        return columns, outputs
