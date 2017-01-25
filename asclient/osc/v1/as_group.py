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

from asclient.common.i18n import _
from asclient.v1 import resource
from osc_lib.command import command

LOG = logging.getLogger(__name__)


class ListAutoScalingGroup(command.Lister):
    _description = _("List Auto-Scaling group")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingGroup, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.autoscaling.group_mgr
        groups = group_mgr.list()
        columns = resource.AutoScalingGroup.list_column_names
        return columns, (g.get_display_data(columns) for g in groups)
