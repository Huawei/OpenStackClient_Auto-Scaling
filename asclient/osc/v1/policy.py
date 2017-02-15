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
from asclient.osc.v1 import parser_builder as pb
from asclient.v1 import resource

LOG = logging.getLogger(__name__)


class ShowPolicy(command.ShowOne):
    _description = _("show policy")

    def get_parser(self, prog_name):
        parser = super(ShowPolicy, self).get_parser(prog_name)
        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        policy = client.policies.get()
        columns = resource.Policy.show_column_names
        formatter = resource.Policy.formatter
        outputs = policy.get_display_data(columns, formatter=formatter)
        return columns, outputs


class EditPolicy(command.Command):
    _description = _("edit policy")

    def get_parser(self, prog_name):
        parser = super(EditPolicy, self).get_parser(prog_name)
        # usb related
        pb.Policy.add_switch_arg(parser, 'usb-port-redirection')
        pb.Policy.add_switch_arg(parser, 'usb-image')
        pb.Policy.add_switch_arg(parser, 'usb-video')
        pb.Policy.add_switch_arg(parser, 'usb-printer')
        pb.Policy.add_switch_arg(parser, 'usb-storage')
        pb.Policy.add_switch_arg(parser, 'usb-smart-card')

        # printer related
        pb.Policy.add_switch_arg(parser, 'printer-redirection')
        pb.Policy.add_switch_arg(parser, 'sync-client-default-printer')
        pb.Policy.add_printer_driver_arg(parser)

        # file redirection related
        pb.Policy.add_file_redirection_mode_arg(parser)
        pb.Policy.add_switch_arg(parser, 'fixed-drive')
        pb.Policy.add_switch_arg(parser, 'removable-drive')
        pb.Policy.add_switch_arg(parser, 'cd-rom-drive')
        pb.Policy.add_switch_arg(parser, 'network-drive')

        # clipboard redirection
        pb.Policy.add_clipboard_redirection_arg(parser)

        # hdp plus
        pb.Policy.add_switch_arg(parser, 'hdp-plus')
        pb.Policy.add_display_level_arg(parser)
        pb.Policy.add_bandwidth_arg(parser)
        pb.Policy.add_frame_rate_arg(parser)
        pb.Policy.add_video_frame_rate_arg(parser)
        pb.Policy.add_smoothing_factor_arg(parser)
        pb.Policy.add_lossy_compression_quality_arg(parser)

        return parser

    def take_action(self, args):
        client = self.app.client_manager.workspace
        client.policies.edit(args.enable_usb_port_redirection,
                             args.enable_usb_image, args.enable_usb_video,
                             args.enable_usb_printer, args.enable_usb_storage,
                             args.enable_usb_smart_card,
                             args.enable_printer_redirection,
                             args.enable_sync_client_default_printer,
                             args.universal_printer_driver,
                             args.file_redirection_mode,
                             args.enable_fixed_drive,
                             args.enable_removable_drive,
                             args.enable_cd_rom_drive,
                             args.enable_network_drive,
                             args.clipboard_redirection, args.enable_hdp_plus,
                             args.display_level, args.bandwidth,
                             args.frame_rate, args.video_frame_rate,
                             args.smoothing_factor,
                             args.lossy_compression_quality)
        return 'done'
