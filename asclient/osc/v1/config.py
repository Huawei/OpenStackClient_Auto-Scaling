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
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource

from osc_lib.command import command

LOG = logging.getLogger(__name__)


class CreateAutoScalingConfig(command.ShowOne):
    _description = _("Create Auto-Scaling configuration")

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingConfig, self).get_parser(prog_name)
        pb.Group.add_group_name_arg(parser)
        pb.Group.add_config_id_arg(parser, required=False)
        pb.Group.add_desired_ins_number_arg(parser, required=False)
        pb.Group.add_max_ins_number_arg(parser, required=False)
        pb.Group.add_min_ins_number_arg(parser, required=False)
        pb.Group.add_cool_down_time_arg(parser, required=False)
        pb.Group.add_lb_listener_arg(parser, required=False)
        return parser

    def take_action(self, args):
        config_mgr = self.app.client_manager.autoscaling.config_mgr
        groups = config_mgr.list()
        columns = resource.AutoScalingGroup.list_column_names
        return columns, (g.get_display_data(columns) for g in groups)
