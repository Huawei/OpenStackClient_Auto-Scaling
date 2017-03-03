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
import argparse
import logging

from osc_lib.command import command

from asclient.common import parser_builder as bpb
from asclient.common import parsetypes
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource

LOG = logging.getLogger(__name__)


class CreateAutoScalingPolicy(command.Command):
    _description = _("Create Auto Scaling policy")

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_name_arg(parser)
        pb.Policy.add_group_opt(parser, required=True)
        policy_type_help = "Auto Scaling policy type"
        pb.Policy.add_policy_type_opt(parser, help_=policy_type_help,
                                      required=True)
        pb.Policy.add_cool_down_opt(parser)
        pb.Policy.add_alarm_id_opt(parser)
        # pb.Policy.add_recurrence_opt(parser)
        pb.Policy.add_recurrence_type_opt(parser)
        pb.Policy.add_recurrence_value_opt(parser)
        pb.Policy.add_launch_time_opt(parser)
        pb.Policy.add_start_time_opt(parser)
        pb.Policy.add_end_time_opt(parser)
        pb.Policy.add_action_opt(parser)

        return parser

    def take_action(self, args):

        groups = self.app.client_manager.auto_scaling.groups
        policies = self.app.client_manager.auto_scaling.policies

        launch_time = args.launch_time
        # validate launch time
        if args.type == 'RECURRENCE':
            parse = parsetypes.date_type('%H:%M')
            parse(args.launch_time)
        elif args.type == 'SCHEDULED':
            parse = parsetypes.date_type('%Y-%m-%dT%H:%M')
            parse(args.launch_time)
            launch_time += 'Z'

        group_id = groups.find(args.group).id
        kwargs = {
            "alarm_id": args.alarm_id,
            "start_time": args.start_time,
            "end_time": args.end_time,
            "cool_down": args.cool_down,
            "recurrence_type": args.recurrence_type,
            "recurrence_value": args.recurrence_value,
            "launch_time": launch_time,
        }

        if args.action:
            kwargs.update(args.action)

        created = policies.create(group_id, args.name, args.type, **kwargs)
        return "Policy %s created" % created.id


class EditAutoScalingPolicy(command.Command):
    _description = _("Edit Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(EditAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'edit')
        policy_name_help = "Change policy name to"
        pb.Policy.add_policy_name_opt(parser, help_=policy_name_help,
                                      required=False)
        policy_type_help = "Change policy type to"
        pb.Policy.add_policy_type_opt(parser, help_=policy_type_help,
                                      required=False)
        pb.Policy.add_cool_down_opt(parser)
        pb.Policy.add_alarm_id_opt(parser)
        pb.Policy.add_recurrence_type_opt(parser)
        pb.Policy.add_recurrence_value_opt(parser)
        pb.Policy.add_launch_time_opt(parser)
        pb.Policy.add_start_time_opt(parser)
        pb.Policy.add_end_time_opt(parser)
        pb.Policy.add_action_opt(parser)
        return parser

    def take_action(self, args):
        policies = self.app.client_manager.auto_scaling.policies
        policy = policies.find(args.policy)

        launch_time = args.launch_time
        # validate launch time
        if args.type == 'RECURRENCE':
            parse = parsetypes.date_type('%H:%M')
            parse(args.launch_time)
        elif args.type == 'SCHEDULED':
            parse = parsetypes.date_type('%Y-%m-%dT%H:%M')
            parse(args.launch_time)
            launch_time += 'Z'

        kwargs = {
            "type_": args.type,
            "name": args.name,
            "alarm_id": args.alarm_id,
            "launch_time": launch_time,
            "start_time": args.start_time,
            "end_time": args.end_time,
            "recurrence_type": args.recurrence_type,
            "recurrence_value": args.recurrence_value,
            "cool_down": args.cool_down,
        }

        if args.action:
            kwargs.update(args.action)
        policies.edit(policy.id, **kwargs)
        return "done"


class ListAutoScalingPolicy(command.Lister):
    _description = _("List Auto Scaling Policies")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_group_opt(parser, required=True)
        pb.Policy.add_policy_name_opt(parser)
        pb.Policy.add_policy_type_opt(parser)
        bpb.Base.add_limit_opt(parser)
        bpb.Base.add_offset_opt(parser)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.auto_scaling.groups
        group_id = group_mgr.find(args.group).id

        policy_mgr = self.app.client_manager.auto_scaling.policies
        policies = policy_mgr.list(group_id, name=args.name, type_=args.type,
                                   offset=args.offset, limit=args.limit)

        columns = resource.AutoScalingPolicy.list_column_names
        data = [p.get_display_data(columns) for p in policies]
        return columns, data


class ShowAutoScalingPolicy(command.ShowOne):
    _description = _("Show Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'show')
        return parser

    def take_action(self, args):
        policy_mgr = self.app.client_manager.auto_scaling.policies
        policy = policy_mgr.find(args.policy)
        columns = resource.AutoScalingPolicy.show_column_names
        formatter = resource.AutoScalingPolicy.formatter
        data = policy.get_display_data(columns, formatter=formatter)
        return columns, data


class DeleteAutoScalingPolicy(command.Command):
    _description = _("Delete Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'delete')
        return parser

    def take_action(self, args):
        policy_mgr = self.app.client_manager.auto_scaling.policies
        policy = policy_mgr.find(args.policy)
        policy_mgr.delete(policy.id)
        return 'done'


class PauseAutoScalingPolicy(command.Command):
    _description = _("Pause Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(PauseAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'pause')
        return parser

    def take_action(self, args):
        policy_mgr = self.app.client_manager.auto_scaling.policies
        policy = policy_mgr.find(args.policy)
        policy_mgr.pause(policy.id)
        return 'done'


class ExecuteAutoScalingPolicy(command.Command):
    _description = _("Execute Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(ExecuteAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'execute')
        return parser

    def take_action(self, args):
        policy_mgr = self.app.client_manager.auto_scaling.policies
        policy = policy_mgr.find(args.policy)
        policy_mgr.execute(policy.id)
        return 'done'


class ResumeAutoScalingPolicy(command.Command):
    _description = _("Resume Auto Scaling Policy")

    def get_parser(self, prog_name):
        parser = super(ResumeAutoScalingPolicy, self).get_parser(prog_name)
        pb.Policy.add_policy_id_arg(parser, 'resume')
        return parser

    def take_action(self, args):
        policy_mgr = self.app.client_manager.auto_scaling.policies
        policy = policy_mgr.find(args.policy)
        policy_mgr.resume(policy.id)
        return 'done'
