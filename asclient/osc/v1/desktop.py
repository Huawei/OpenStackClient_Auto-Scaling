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

import six
from osc_lib.command import command

from asclient.common import parser_builder as p
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource

LOG = logging.getLogger(__name__)


class ListDesktop(command.Lister):
    _description = _("list desktops")

    def get_parser(self, prog_name):
        parser = super(ListDesktop, self).get_parser(prog_name)
        pb.Desktop.add_status_option(parser)
        pb.Desktop.add_desktop_ip_option(parser)
        pb.Desktop.add_user_name_option(parser, False)
        pb.Desktop.add_computer_name_option(parser)
        pb.Desktop.add_marker_option(parser)
        p.BaseParser.add_limit_option(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktops = client.desktops.list(args.desktop_ip, args.status,
                                        args.user_name, args.computer_name,
                                        args.marker, args.limit)
        columns = resource.Desktop.list_column_names
        data = [r.get_display_data(columns) for r in desktops]
        return columns, data


class ListDesktopDetail(command.Lister):
    _description = _("list desktops with detail")

    def get_parser(self, prog_name):
        parser = super(ListDesktopDetail, self).get_parser(prog_name)
        pb.Desktop.add_status_option(parser)
        pb.Desktop.add_desktop_ip_option(parser)
        pb.Desktop.add_user_name_option(parser)
        pb.Desktop.add_computer_name_option(parser)
        pb.Desktop.add_marker_option(parser)
        p.BaseParser.add_limit_option(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktops = client.desktops.list_detail(args.desktop_ip,
                                               args.status,
                                               args.user_name,
                                               args.computer_name,
                                               args.marker,
                                               args.limit)
        columns = resource.Desktop.list_detail_column_names
        data = [r.get_display_data(columns) for r in desktops]
        return columns, data


class RebootDesktop(command.Command):
    _description = _("reboot desktop")

    def get_parser(self, prog_name):
        parser = super(RebootDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'reboot')
        pb.Desktop.add_hard_or_soft_arg(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)
        client.desktops.reboot(desktop.desktop_id, args.force)
        return "done"


class CreateDesktop(command.Command):
    _description = _("Create a new desktop")

    def get_parser(self, prog_name):
        parser = super(CreateDesktop, self).get_parser(prog_name)

        user_name_desc = _("Desktop Login UserName (character "
                           "[a-zA-Z0-9-_] allowed, start with alphabet, "
                           "length between 1-20)")
        pb.Desktop.add_user_name_option(parser, True, user_name_desc)
        pb.Desktop.add_user_mail_option(parser)

        computer_name_desc = _("Desktop Computer name (must be unique, "
                               "character [a-zA-Z0-9-_] allowed, start "
                               "with alphabet, length between 1-15)")
        pb.Desktop.add_computer_name_option(
            parser, True, computer_name_desc
        )

        pb.Desktop.add_product_id_option(parser)
        pb.Desktop.add_image_id_option(parser)
        pb.Desktop.add_root_volume_option(parser)
        pb.Desktop.add_data_volume_option(parser)
        pb.Desktop.add_security_group_option(parser)
        pb.Desktop.add_nic_option(parser)
        return parser

    def take_action(self, args):
        desktops = self.app.client_manager.workspace.desktops
        network = self.app.client_manager.network
        security_groups = [dict(id=network.find_security_group(sg).id)
                           for sg in args.security_groups]
        for nic in args.nics:
            subnet = network.find_subnet(nic["subnet_id"])
            nic["subnet_id"] = subnet.id
        job = desktops.create(args.computer_name, args.user_name,
                              args.user_email, args.product_id,
                              args.root_volume, data_volumes=args.data_volumes,
                              image_id=args.image_id,
                              security_groups=security_groups, nics=args.nics)
        return 'Request Received, job id: ' + job["job_id"]


class StartDesktop(command.Command):
    _description = _("Start desktop")

    def get_parser(self, prog_name):
        parser = super(StartDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'start')
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)
        client.desktops.start(desktop.desktop_id)
        return "done"


class StopDesktop(command.Command):
    _description = _("Stop desktop")

    def get_parser(self, prog_name):
        parser = super(StopDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'stop')
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)
        client.desktops.stop(desktop.desktop_id)
        return "done"


class DeleteDesktop(command.Command):
    _description = _("Delete desktop")

    def get_parser(self, prog_name):
        parser = super(DeleteDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'delete')
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)
        client.desktops.delete(desktop.desktop_id)
        return "done"


class EditDesktop(command.Command):
    _description = _("Edit desktop meta properties")

    def get_parser(self, prog_name):
        parser = super(EditDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'edit')
        computer_name_desc = _("Desktop Computer name (must be unique, "
                               "character [a-zA-Z0-9-_] allowed, start "
                               "with alphabet, length between 1-15)")
        pb.Desktop.add_computer_name_option(
            parser, True, computer_name_desc
        )
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)
        client.desktops.edit(desktop.desktop_id, args.computer_name)
        return 'done'


class ShowDesktop(command.ShowOne):
    _description = _("Show desktop detail")

    def get_parser(self, prog_name):
        parser = super(ShowDesktop, self).get_parser(prog_name)
        pb.Desktop.add_desktop_id_arg(parser, 'show')
        return parser

    def take_action(self, args):
        compute = self.app.client_manager.compute
        client = self.app.client_manager.workspace
        desktop = client.desktops.find(args.desktop_id)

        # replace security groups
        # sg_list = [utils.find_resource(compute.security_groups,
        #                                sg['id']).name
        #            for sg in desktop.security_groups]
        # desktop.security_groups = sg_list
        desktop.security_groups = [sg['id'] for sg in desktop.security_groups]

        addresses = []
        for address in six.itervalues(desktop.addresses):
            addresses += address
        desktop.addresses = addresses

        columns = resource.Desktop.show_column_names
        formatter = resource.Desktop.formatter
        return columns, desktop.get_display_data(columns, formatter=formatter)
