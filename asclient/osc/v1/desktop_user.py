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

from asclient.common import parser_builder as bpb
from asclient.common.i18n import _
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource

LOG = logging.getLogger(__name__)


class ListDesktopUser(command.Lister):
    _description = _("list desktop users")

    def get_parser(self, prog_name):
        parser = super(ListDesktopUser, self).get_parser(prog_name)
        pb.DesktopUser.add_username_option(parser)
        pb.DesktopUser.add_email_option(parser)
        pb.DesktopUser.add_marker_option(parser)
        bpb.BaseParser.add_limit_option(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        users = client.desktop_users.list(name=args.user_name,
                                          email=args.user_email,
                                          marker=args.marker,
                                          limit=args.limit)
        columns = resource.DesktopUser.list_column_names
        outputs = [r.get_display_data(columns) for r in users]
        return columns, outputs


class ListLoginRecords(command.Lister):
    _description = _("list desktop login records")

    def get_parser(self, prog_name):
        parser = super(ListLoginRecords, self).get_parser(prog_name)
        pb.DesktopUser.add_start_time_option(parser)
        pb.DesktopUser.add_end_time_option(parser)
        pb.DesktopUser.add_user_name_option(parser)
        pb.DesktopUser.add_computer_name_option(parser)
        pb.DesktopUser.add_terminal_type_option(parser)
        bpb.BaseParser.add_offset_option(parser)
        bpb.BaseParser.add_limit_option(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace

        kwargs = dict(start_time=args.start_time,
                      end_time=args.end_time,
                      user_name=args.user_name,
                      computer_name=args.computer_name,
                      terminal_type=args.terminal_type,
                      offset=args.offset,
                      limit=args.limit)
        records = client.desktop_users.list_login_records(**kwargs)
        columns = resource.DesktopLoginRecords.list_column_names
        outputs = [r.get_display_data(columns) for r in records]
        return columns, outputs
