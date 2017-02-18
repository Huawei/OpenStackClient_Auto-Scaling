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


class ListQuota(command.Lister):
    _description = _("list auto scaling quotas")

    def get_parser(self, prog_name):
        parser = super(ListQuota, self).get_parser(prog_name)
        parser.add_argument(
            '--group',
            metavar="<group>",
            required=False,
            help=_("list quota of group (ID or name)"),
        )
        return parser

    def take_action(self, args):
        quota_mgr = self.app.client_manager.auto_scaling.quotas
        group_mgr = self.app.client_manager.auto_scaling.groups
        group_id = group_mgr.find(args.group).id if args.group else None
        quotas = quota_mgr.list(as_group_id=group_id)
        columns = resource.AutoScalingQuota.list_column_names
        return columns, (q.get_display_data(columns) for q in quotas)
