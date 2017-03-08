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
import io

from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from asclient.common import parser_builder as bpb
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource


class CreateAutoScalingConfig(command.Command):
    _description = _("Create Auto Scaling instance configuration")

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingConfig, self).get_parser(prog_name)

        pb.Config.add_name_arg(parser)

        pb.Config.add_instance_opt(parser, required=False)
        pb.Config.add_flavor_option(parser, required=False)
        help_image = _("Image to assign to configuration (ID or name)")
        pb.Config.add_image_opt(parser, help_image, required=False)

        pb.Config.add_root_volume_opt(parser)
        pb.Config.add_data_volume_opt(parser)
        pb.Config.add_authentication_opt(parser)

        pb.Config.add_file_opt(parser)
        pb.Config.add_public_ip_option(parser)
        pb.Config.add_user_data_option(parser)
        pb.Config.add_metadata_opt(parser)

        return parser

    def take_action(self, args):
        compute = self.app.client_manager.compute
        mgr = self.app.client_manager.auto_scaling.configs

        image = None
        flavor = None
        disk = []
        if not args.instance_id:
            if not all((args.image, args.flavor, args.root_volume,)):
                msg = ("All Flavor/Image/Root-Volume is required when "
                       "instance-id is not provided")
                raise exceptions.CommandError(_(msg))
            image = utils.find_resource(compute.images, args.image).id
            flavor = utils.find_resource(compute.flavors, args.flavor).id

            args.root_volume.update(dict(disk_type='SYS'))
            disk.append(args.root_volume)
            for v in args.data_volumes:
                v.update(dict(disk_type='DATA'))
                disk.append(v)

        files = {}
        for f in args.file:
            dst, src = f.split('=', 1)
            try:
                files[dst] = io.open(src, 'rb')
            except IOError as e:
                msg = _("Can't open file '%(source)s': %(exception)s")
                raise exceptions.CommandError(
                    msg % dict(source=src, exception=e)
                )

        kwargs = {
            "instance_id": args.instance_id,
            "flavor_id": flavor,
            "image_id": image,
            "disk": disk,
            "files": files,
            "metadata": args.metadata,
            "key_name": args.key_name,
            "admin_pwd": args.admin_pass,
            "ip_type": args.ip_type,
            "bandwidth_size": args.bandwidth_size,
            "bandwidth_share_type": args.bandwidth_charging_mode,
            "bandwidth_charging_mode": args.bandwidth_charging_mode,
            "user_data": args.userdata,
        }

        config = mgr.create(args.name, **kwargs)
        return "Configuration %s created" % config.id


class ListAutoScalingConfig(command.Lister):
    _description = _("List Auto Scaling instance configuration")

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingConfig, self).get_parser(prog_name)
        help_name = _("list auto scaling instance configs with name")
        pb.Config.add_name_opt(parser, help_name, required=False)
        help_image = _("list auto scaling instance configs with image"
                       "(ID or Name)")
        pb.Config.add_image_opt(parser, help_image, required=False)
        bpb.Base.add_offset_opt(parser)
        bpb.Base.add_limit_opt(parser)
        return parser

    def take_action(self, args):
        mgr = self.app.client_manager.auto_scaling.configs
        image_id = None
        if args.image:
            image_client = self.app.client_manager.image
            image_id = utils.find_resource(image_client.images, args.image).id
        configs = mgr.list(name=args.name, image_id=image_id,
                           offset=args.offset, limit=args.limit)

        columns = resource.AutoScalingConfig.list_column_names
        output = [c.get_display_data(columns) for c in configs]
        return columns, output


class ShowAutoScalingConfig(command.ShowOne):
    _description = _("Show Auto Scaling instance configuration detail")

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingConfig, self).get_parser(prog_name)
        pb.Config.add_config_arg(parser)
        return parser

    def take_action(self, args):
        mgr = self.app.client_manager.auto_scaling.configs
        configs = mgr.find(args.config)
        columns = resource.AutoScalingConfig.show_column_names
        formatter = resource.AutoScalingConfig.formatter
        output = configs.get_display_data(columns, formatter=formatter)
        return columns, output


class DeleteAutoScalingConfig(command.Command):
    _description = _("Delete Auto Scaling instance configuration")

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'config',
            metavar="<config>",
            nargs="+",
            help=_("Configuration to delete (ID or name), Repeat option "
                   "to delete multiple configurations."),
        )
        return parser

    def take_action(self, args):
        mgr = self.app.client_manager.auto_scaling.configs
        config_ids = [mgr.find(config_id).id for config_id in args.config]
        mgr.delete(config_ids)
        return "done"
