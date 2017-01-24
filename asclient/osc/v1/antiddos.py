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

from asclient.common import parser as p
from asclient.common import utils
from asclient.common.i18n import _
from asclient.v1.resource import antiddos

LOG = logging.getLogger(__name__)


class AntiDDosParser(object):
    @staticmethod
    def add_floating_ip_arg(parser):
        parser.add_argument(
            'floating_ip',
            metavar='<floating ip>',
            help=_("For floating ip (UUID or IP)")
        )

    @staticmethod
    def add_enable_l7_arg(parser):
        enable_group = parser.add_mutually_exclusive_group()
        enable_group.add_argument(
            '--enable-l7',
            action="store_true",
            dest='enable_l7',
            default=True,
            help=_("enable L7 protection (default)")
        )
        enable_group.add_argument(
            '--disable-l7',
            action="store_false",
            dest='enable_l7',
            help=_("disable L7 protection")
        )

    @staticmethod
    def add_traffic_pos_arg(parser):
        parser.add_argument(
            '--traffic-pos',
            metavar='<traffic-pos>',
            required=True,
            choices=utils.str_range(1, 10),
            help=_("traffic pos, integer between 1-9")
        )

    @staticmethod
    def add_http_request_pos_arg(parser):
        parser.add_argument(
            '--http-request-pos',
            metavar='<http-request-pos>',
            required=True,
            choices=utils.str_range(1, 16),
            help=_("http request pos, integer between 1-15")
        )

    @staticmethod
    def add_cleaning_acess_pos_arg(parser):
        parser.add_argument(
            '--cleaning-access-pos',
            metavar='<cleaning-access-pos>',
            required=True,
            choices=utils.str_range(1, 9),
            help=_("cleaning access pos, integer between 1-8")
        )

    @staticmethod
    def add_app_type_arg(parser):
        parser.add_argument(
            '--app-type',
            metavar='<app-type>',
            required=True,
            choices=('0', '1'),
            help=_("app type, 0 or 1")
        )


class QueryAntiDDosConfig(command.Lister):
    _description = _("Query AntiDDos configurations")

    def get_parser(self, prog_name):
        parser = super(QueryAntiDDosConfig, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        data = client.antiddos.query_config_list()
        columns = antiddos.AntiDDos.list_column_names
        return columns, (r.get_display_data(columns) for r in data)


class OpenAntiDDos(command.Command):
    _description = _("Open AntiDDos for floating IP")

    def get_parser(self, prog_name):
        parser = super(OpenAntiDDos, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        AntiDDosParser.add_enable_l7_arg(parser)
        AntiDDosParser.add_traffic_pos_arg(parser)
        AntiDDosParser.add_http_request_pos_arg(parser)
        AntiDDosParser.add_cleaning_acess_pos_arg(parser)
        AntiDDosParser.add_app_type_arg(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        floating_ip = client.antiddos.find(args.floating_ip)
        task = client.antiddos.open_antiddos(floating_ip.floating_ip_id,
                                             args.enable_l7,
                                             args.traffic_pos,
                                             args.http_request_pos,
                                             args.cleaning_access_pos,
                                             args.app_type)

        return 'Request Received, task id: ' + task['task_id']


class CloseAntiDDos(command.Command):
    _description = _("Close AntiDDos of floating IP")

    def get_parser(self, prog_name):
        parser = super(CloseAntiDDos, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        floating_ip = client.antiddos.find(args.floating_ip)
        task = client.antiddos.close_antiddos(floating_ip.floating_ip_id)
        return 'Request Received, task id: ' + task['task_id']


class ShowAntiDDos(command.ShowOne):
    _description = _("Display AntiDDos settings of floating IP")

    def get_parser(self, prog_name):
        parser = super(ShowAntiDDos, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        _antiddos = client.antiddos.find(args.floating_ip)
        columns = antiddos.AntiDDos.list_column_names
        return columns, _antiddos.get_display_data(columns)


class SetAntiDDos(command.Command):
    _description = _("Set AntiDDos settings of floating IP")

    def get_parser(self, prog_name):
        parser = super(SetAntiDDos, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        AntiDDosParser.add_enable_l7_arg(parser)
        AntiDDosParser.add_traffic_pos_arg(parser)
        AntiDDosParser.add_http_request_pos_arg(parser)
        AntiDDosParser.add_cleaning_acess_pos_arg(parser)
        AntiDDosParser.add_app_type_arg(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        floating_ip = client.antiddos.find(args.floating_ip)
        task = client.antiddos.update_antiddos(floating_ip.floating_ip_id,
                                               args.enable_l7,
                                               args.traffic_pos,
                                               args.http_request_pos,
                                               args.cleaning_access_pos,
                                               args.app_type)
        return 'Request Received, task id: ' + task['task_id']


class ShowAntiDDosTask(command.ShowOne):
    _description = _("Display AntiDDos setting task")

    def get_parser(self, prog_name):
        parser = super(ShowAntiDDosTask, self).get_parser(prog_name)
        parser.add_argument(
            'task_id',
            metavar='<task id>',
            help=_("AntiDDos setting task id")
        )
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        task = client.antiddos.get_task_status(args.task_id)
        columns = antiddos.AntiDDosTask.show_column_names
        return columns, task.get_display_data(columns)


class ListAntiDDosStatus(command.Lister):
    _description = _("List AntiDDos status")

    def get_parser(self, prog_name):
        parser = super(ListAntiDDosStatus, self).get_parser(prog_name)
        parser.add_argument(
            "--status",
            choices=antiddos.AntiDDos.status_list,
            help=_("list AntiDDos with status")
        )
        parser.add_argument(
            "--ip",
            help=_("list AntiDDos with the ip (eg: 110.110.)")
        )
        p.BaseParser.add_limit_option(parser)
        p.BaseParser.add_offset_option(parser)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.antiddos
        data = client.antiddos.list(status=args.status,
                                    ip=args.ip,
                                    limit=args.limit,
                                    offset=args.offset)
        columns = antiddos.AntiDDos.list_column_names
        return columns, (r.get_display_data(columns) for r in data)


class ShowAntiDDosStatus(command.ShowOne):
    _description = _("Display AntiDDos status of floating ip")

    def get_parser(self, prog_name):
        parser = super(ShowAntiDDosStatus, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        return parser

    def take_action(self, args):
        manager = self.app.client_manager.antiddos.antiddos
        floating_ip = manager.find(args.floating_ip)
        antiddos_status = manager.get_antiddos_status(floating_ip.floating_ip_id)
        return zip(*sorted(six.iteritems(antiddos_status)))


class ListAntiDDosDailyReport(command.Lister):
    _description = _("List AntiDDos report(every 5min) of past 24h")

    def get_parser(self, prog_name):
        parser = super(ListAntiDDosDailyReport, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        return parser

    def take_action(self, args):
        manager = self.app.client_manager.antiddos.antiddos
        floating_ip = manager.find(args.floating_ip)
        reports = manager.get_antiddos_daily_report(floating_ip.floating_ip_id)
        columns = antiddos.AntiDDosDailyReport.list_column_names
        return columns, (r.get_display_data(columns) for r in reports)


class ListAntiDDosLogs(command.Lister):
    _description = _("List AntiDDos logs(every 5min) of past 24h")

    def get_parser(self, prog_name):
        parser = super(ListAntiDDosLogs, self).get_parser(prog_name)
        AntiDDosParser.add_floating_ip_arg(parser)
        p.BaseParser.add_limit_option(parser)
        p.BaseParser.add_offset_option(parser)
        p.BaseParser.add_sortdir_option(parser)
        return parser

    def take_action(self, args):
        # TODO(Woo) no data in test env, need to test later
        manager = self.app.client_manager.antiddos.antiddos
        floating_ip = manager.find(args.floating_ip)
        logs = manager.get_antiddos_daily_logs(floating_ip.floating_ip_id)
        columns = antiddos.AntiDDosLog.list_column_names
        return columns, (r.get_display_data(columns) for r in logs)


class ListAntiDDosWeeklyReport(command.Lister):
    _description = _("List AntiDDos weekly report")

    def get_parser(self, prog_name):
        # TODO (woo)
        parser = super(ListAntiDDosWeeklyReport, self).get_parser(prog_name)
        parser.add_argument(
            '--start-date',
            metavar='<start-date>',
            required=True,
            help=_("start date, start ")
        )
        return parser

    def take_action(self, args):
        manager = self.app.client_manager.antiddos.antiddos
        floating_ip = manager.find(args.floating_ip)
        reports = manager.get_antiddos_weekly_report(floating_ip.floating_ip_id)
        columns = antiddos.AntiDDosWeeklyReport.list_column_names
        return columns, (r.get_display_data(columns) for r in reports)
