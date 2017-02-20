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

from asclient.common import parser_builder as bpb
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource
from osc_lib.command import command


class ListAutoScalingLog(command.Lister):
    _description = _("List Auto Scaling instances")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingLog, self).get_parser(prog_name)
        pb.Instance.add_group_opt(parser)
        pb.Log.add_start_time_option(parser)
        pb.Log.add_end_time_opt(parser)
        bpb.Base.add_limit_opt(parser)
        bpb.Base.add_offset_opt(parser)
        return parser

    def take_action(self, args):
        as_groups_mgr = self.app.client_manager.auto_scaling.groups
        group_id = as_groups_mgr.find(args.group).id

        mgr = self.app.client_manager.auto_scaling.logs
        logs = mgr.list(group_id, start_time=args.start_time,
                        end_time=args.end_time, limit=args.limit,
                        offset=args.offset)
        columns = resource.AutoScalingLog.list_column_names
        data = [log.get_display_data(columns) for log in logs]
        return columns, data
