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
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command


class ListAutoScalingInstance(command.Lister):
    _description = _("List Auto Scaling instances")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingInstance, self).get_parser(prog_name)
        pb.Instance.add_group_opt(parser)
        pb.Instance.add_lifecycle_status_opt(parser)
        pb.Instance.add_health_status_opt(parser)
        bpb.Base.add_limit_opt(parser)
        bpb.Base.add_offset_opt(parser)
        return parser

    def take_action(self, args):
        mgr = self.app.client_manager.auto_scaling.instances
        as_groups_mgr = self.app.client_manager.auto_scaling.groups

        group_id = as_groups_mgr.find(args.group).id
        instances = mgr.list(group_id, lifecycle_status=args.lifecycle_status,
                             health_status=args.health_status,
                             limit=args.limit, offset=args.offset)
        # return columns, output
        columns = resource.AutoScalingInstance.list_column_names
        data = [i.get_display_data(columns) for i in instances]
        return columns, data


class RemoveAutoScalingInstance(command.Command):
    _description = _("Batch remove Auto Scaling instances")

    def get_parser(self, prog_name):
        parser = super(RemoveAutoScalingInstance, self).get_parser(prog_name)
        pb.Instance.add_group_opt(parser)
        pb.Instance.add_instances_opt(parser, 'removed')
        pb.Instance.add_delete_instance_opt(parser)
        return parser

    def take_action(self, args):
        mgr = self.app.client_manager.auto_scaling.instances

        # TODO(woo) do we need to verify instance
        #            and support instance name input
        as_groups_mgr = self.app.client_manager.auto_scaling.groups
        group_id = as_groups_mgr.find(args.group).id
        instances = mgr.list(group_id)

        instance_id_list = []
        mapped_by_name = {}
        for instance in instances:
            instance_id_list.append(instance.id)
            mapped_by_name[instance.name] = instance.id

        # convert user input to real instance id
        converted = []
        for id_or_name in args.instances:
            if id_or_name in instance_id_list:
                converted.append(id_or_name)
            elif id_or_name in mapped_by_name:
                converted.append(mapped_by_name[id_or_name])
            else:
                msg = 'Instance with id or name "%s" is not belong to Group %s'
                raise exceptions.CommandError(msg % (id_or_name, group_id))

        mgr.remove_instances(group_id, instance_id_list,
                             delete_instance=args.delete)
        return 'done'


class AddAutoScalingInstance(command.Command):
    _description = _("Batch add Auto Scaling instances to group")

    def get_parser(self, prog_name):
        parser = super(AddAutoScalingInstance, self).get_parser(prog_name)
        pb.Instance.add_group_opt(parser)
        pb.Instance.add_instances_opt(parser, 'removed')
        pb.Instance.add_delete_instance_opt(parser)
        return parser

    def take_action(self, args):
        compute_client = self.app.client_manager.compute
        as_groups_mgr = self.app.client_manager.auto_scaling.groups
        group_id = as_groups_mgr.find(args.group).id
        instance_ids = [utils.find_resource(compute_client.servers, i).id
                        for i in args.instances]
        as_instance_mgr = self.app.client_manager.auto_scaling.instances
        as_instance_mgr.add_instances(group_id, instance_ids)
        return 'done'
