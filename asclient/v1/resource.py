#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from osc_lib import utils as formatter

from asclient.common import display
from asclient.common import resource

LOG = logging.getLogger(__name__)


class Desktop(resource.Resource, display.Display):
    """workspace desktop resource instance"""

    show_column_names = [
        "Desktop Id",
        "Computer Name",
        "User Name",
        "Product Id",
        "Security Groups",
        "Flavor",
        "metadata",
        "addresses",
        "Root Volume",
        "Data Volumes",
        "Created",
        "Login Status",
        "Status"
    ]

    formatter = {
        "Security Groups": formatter.format_list,
        "Flavor": lambda flavor: flavor['id'],
        "metadata": formatter.format_dict,
        "Root Volume": formatter.format_dict,
        "Data Volumes": formatter.format_list_of_dicts,
        "addresses": formatter.format_list_of_dicts,
    }

    list_column_names = [
        "Desktop Id",
        "Computer Name",
        "User Name",
        "Ip Address",
        "Created"
    ]

    list_detail_column_names = [
        "Desktop Id",
        "Computer Name",
        "User Name",
        "Product Id",
        "Login Status",
        "Status"
    ]


class Workspace(resource.Resource, display.Display):
    """workspace desktop user resource instance"""

    show_column_names = [
        "AD Domains",
        "VPC ID",
        "VPC Name",
        "Dedicated access address",
        "Internet access address",
        "access_mode",
        "Subnets",
    ]

    column_2_property = {
        "Subnets": "subnet_ids"
    }

    formatter = {
        "AD Domains": formatter.format_dict,
        "subnet_ids": formatter.format_list_of_dicts,
    }


class Product(resource.Resource, display.Display):
    """workspace product resource instance"""

    list_column_names = [
        "Product ID",
        "Flavor ID",
        "Type",
        "Descriptions"
    ]


def format_bool_enable(enable):
    return "Enabled" if enable else "Disabled"


def format_prop_enable(target):
    return format_bool_enable(target["enable"])


def format_hdp_enable(target):
    return format_bool_enable(target["hdp_plus_enable"])


class Policy(resource.Resource, display.Display):
    """workspace policy resource instance"""

    show_column_names = [
        "USB port redirection",
        "USB image",
        "USB video",
        "USB printer",
        "USB storage",
        "USB smart card",

        "Printer redirection",
        "sync client default printer",
        "universal printer driver",
        #
        "File redirection mode",
        "fixed drive",
        "removable drive",
        "cd rom drive",
        "network drive",

        "clipboard redirection",
        #
        "hdp plus",
        #
        "hdp display level",
        "hdp bandwidth",
        "hdp frame rate",
        "hdp video frame rate",
        "hdp smoothing factor",
        "hdp lossy compression quality",
    ]

    formatter = {
        "USB port redirection": format_prop_enable,
        "Printer redirection": format_prop_enable,
        "hdp plus": format_hdp_enable,
    }

    @property
    def hdp_plus_options(self):
        return self.hdp_plus["options"]

    @property
    def hdp_display_level(self):
        return self.hdp_plus["display_level"]

    @property
    def hdp_bandwidth(self):
        return self.hdp_plus_options["bandwidth"]

    @property
    def hdp_frame_rate(self):
        return self.hdp_plus_options["frame_rate"]

    @property
    def hdp_video_frame_rate(self):
        return self.hdp_plus_options["video_frame_rate"]

    @property
    def hdp_smoothing_factor(self):
        return self.hdp_plus_options["smoothing_factor"]

    @property
    def hdp_lossy_compression_quality(self):
        return self.hdp_plus_options["lossy_compression_quality"]

    @property
    def file_options(self):
        return self.file_redirection["options"]

    @property
    def file_redirection_mode(self):
        return self.file_redirection["redirection_mode"]

    @property
    def fixed_drive(self):
        return format_bool_enable(self.file_options["fixed_drive_enable"])

    @property
    def removable_drive(self):
        return format_bool_enable(self.file_options["removable_drive_enable"])

    @property
    def cd_rom_drive(self):
        return format_bool_enable(self.file_options["cd_rom_drive_enable"])

    @property
    def network_drive(self):
        return format_bool_enable(self.file_options["network_drive_enable"])

    @property
    def universal_printer_driver(self):
        printer_options = self.printer_redirection["options"]
        return printer_options["universal_printer_driver"]

    @property
    def sync_client_default_printer(self):
        printer_options = self.printer_redirection["options"]
        return format_bool_enable(
            printer_options["sync_client_default_printer_enable"]
        )

    @property
    def usb_option(self):
        return self.usb_port_redirection["options"]

    @property
    def usb_image(self):
        return format_bool_enable(self.usb_option["usb_image_enable"])

    @property
    def usb_video(self):
        return format_bool_enable(self.usb_option["usb_video_enable"])

    @property
    def usb_printer(self):
        return format_bool_enable(self.usb_option["usb_printer_enable"])

    @property
    def usb_storage(self):
        return format_bool_enable(self.usb_option["usb_storage_enable"])

    @property
    def usb_smart_card(self):
        return format_bool_enable(self.usb_option["usb_smart_card_enable"])


class DesktopUser(resource.Resource, display.Display):
    """workspace desktop user resource instance"""

    list_column_names = [
        "Name",
        "Email",
        "Domain Name",
        "Domain Type"
    ]

    column_2_property = {
        "Name": "user_name",
        "Email": "user_email",
    }

    @property
    def domain_name(self):
        return self.ad_domains["domain_name"]

    @property
    def domain_type(self):
        return self.ad_domains["domain_type"]


class DesktopLoginRecords(resource.Resource, display.Display):
    """workspace desktop login record resource instance"""

    list_column_names = [
        "Computer Name",
        "User Name",
        "Terminal Name",
        "Terminal Type",
        "Connection start time",
        "Connection end time",
    ]
