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

from asclient.common import parser_builder as bpb
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource
from osc_lib.command import command

LOG = logging.getLogger(__name__)


class CreateAutoScalingGroup(command.Command):
    _description = _("Create Auto Scaling group")

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_name_arg(parser)
        pb.Group.add_network_opt(parser)
        pb.Group.add_subnet_opt(parser)
        pb.Group.add_security_group_opt(parser)

        pb.Group.add_config_id_opt(parser, required=False)
        pb.Group.add_desired_instance_opt(parser, required=False)
        pb.Group.add_max_instance_opt(parser, required=False)
        pb.Group.add_min_instance_opt(parser, required=False)
        pb.Group.add_cool_down_opt(parser, required=False)
        pb.Group.add_lb_listener_opt(parser, required=False)
        pb.Group.add_health_periodic_audit_method_arg(parser)
        pb.Group.add_health_periodic_audit_time_arg(parser)
        pb.Group.add_instance_terminate_policy_opt(parser)
        pb.Group.add_del_public_ip_opt(parser)
        # TODO  availability_zones
        # TODO notifications
        return parser

    def take_action(self, args):
        network = self.app.client_manager.network
        auto_scaling = self.app.client_manager.auto_scaling

        # manager
        groups = auto_scaling.groups
        configs = auto_scaling.configs

        network_id = network.find_network(args.network).id
        subnets = [network.find_subnet(subnet).id
                   for subnet in args.subnets]
        security_groups = [network.find_security_group(sg).id
                           for sg in args.security_groups]

        config_id = configs.find(args.config).id if args.config else None

        kwargs = {
            "as_config_id": config_id,
            "desire_instance_number": args.desire_instance,
            "max_instance_number": args.max_instance,
            "min_instance_number": args.min_instance,
            "cool_down_time": args.cool_down,
            "lb_listener_id": args.lb_listener,
            "health_periodic_audit_time": args.health_periodic_audit_time,
            "health_periodic_audit_method": args.health_periodic_audit_method,
            "instance_terminate_policy": args.instance_terminate_policy,
            "delete_public_ip": args.delete_public_ip
        }
        created = groups.create(args.name, network_id, subnets,
                                security_groups, **kwargs)
        return args


class ListAutoScalingGroup(command.Lister):
    _description = _("List Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_name_option(parser)
        pb.Group.add_group_status_option(parser)
        pb.Group.add_config_id_opt(parser)
        bpb.Base.add_limit_option(parser)
        bpb.Base.add_offset_option(parser)
        return parser

    def take_action(self, args):
        config_mgr = self.app.client_manager.auto_scaling.configs
        group_mgr = self.app.client_manager.auto_scaling.groups
        config_id = config_mgr.find(args.config).id if args.config else None
        groups = group_mgr.list(name=args.name, status=args.status,
                                as_config_id=config_id, limit=args.limit,
                                offset=args.offset)
        columns = resource.AutoScalingGroup.list_column_names
        return columns, (g.get_display_data(columns) for g in groups)


class ShowAutoScalingGroup(command.ShowOne):
    _description = _("Show Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_id_arg(parser)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.auto_scaling.groups
        group = group_mgr.find(args.group)
        columns = resource.AutoScalingGroup.show_column_names
        formatter = resource.AutoScalingGroup.formatter
        data = group.get_display_data(columns, formatter=formatter)
        return columns, data


class EditAutoScalingGroup(command.Command):
    _description = _("Edit Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(EditAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_id_arg(parser)
        return parser

    def take_action(self, args):
        config_mgr = self.app.client_manager.auto_scaling.configs
        group_mgr = self.app.client_manager.auto_scaling.groups
        config_id = config_mgr.find(args.config).id if args.config else None
        groups = group_mgr.list(name=args.name, status=args.status,
                                as_config_id=config_id, limit=args.limit,
                                offset=args.offset)
        columns = resource.AutoScalingGroup.list_column_names
        return columns, (g.get_display_data(columns) for g in groups)


class DeleteAutoScalingGroup(command.Command):
    _description = _("Delete Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_id_arg(parser)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.auto_scaling.groups
        group = group_mgr.find(args.group)
        group_mgr.delete(group.id)
        return 'done'


class PauseAutoScalingGroup(command.Command):
    _description = _("Pause Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(PauseAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_id_arg(parser)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.auto_scaling.groups
        group = group_mgr.find(args.group)
        group_mgr.pause(group.id)
        return 'done'


class ResumeAutoScalingGroup(command.Command):
    _description = _("Resume Auto Scaling Groups")

    def get_parser(self, prog_name):
        parser = super(ResumeAutoScalingGroup, self).get_parser(prog_name)
        pb.Group.add_group_id_arg(parser)
        return parser

    def take_action(self, args):
        group_mgr = self.app.client_manager.auto_scaling.groups
        group = group_mgr.find(args.group)
        group_mgr.resume(group.id)
        return 'done'
