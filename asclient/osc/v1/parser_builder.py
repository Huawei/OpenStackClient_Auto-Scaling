#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from asclient.common import parsetypes
from asclient.common.i18n import _
from osc_lib.cli import parseractions


class Group(object):
    {
        "scaling_group_name": "GroupNameTest",
        "scaling_configuration_id": "47683a91-93ee-462a-a7d7-484c006f4440",
        "desire_instance_number": 0,
        "min_instance_number": 0,
        "max_instance_number": 0,
        "cool_down_time": 200,
        "health_periodic_audit_method": "NOVA_AUDIT",
        "health_periodic_audit_time": "5",
        "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
        "vpc_id": "a8327883-6b07-4497-9c61-68d03ee193a",
        "networks": [
            {
                "id": "3cd35bca-5a10-416f-8994-f79169559870"
            }
        ],
        "notifications": [
            "EMAIL"
        ],
        "security_groups": [
            {
                "id": "23b7b999-0a30-4b48-ae8f-ee201a88a6ab"
            }
        ]
    }

    @staticmethod
    def add_group_name_arg(parser, required=True):
        parser.add_argument(
            '--name',
            required=required,
            metavar='<group-name>',
            help=_("Auto-Scaling group name")
        )

    @staticmethod
    def add_config_id_arg(parser, required=True):
        parser.add_argument(
            '--config',
            required=required,
            metavar='<scaling-config>',
            help=_("Auto-Scaling config id or name")
        )

    @staticmethod
    def add_desired_ins_number_arg(parser, required=True):
        parser.add_argument(
            '--desire-instance-number',
            required=required,
            metavar='<count>',
            type=int,
            help=_("Auto-Scaling group desired instance number")
        )

    @staticmethod
    def add_max_ins_number_arg(parser, required=True):
        parser.add_argument(
            '--max-instance-number',
            required=required,
            metavar='<count>',
            type=int,
            help=_("Auto-Scaling group max instance number")
        )

    @staticmethod
    def add_min_ins_number_arg(parser, required=True):
        parser.add_argument(
            '--min-instance-number',
            required=required,
            metavar='<count>',
            type=int,
            help=_("Auto-Scaling group min instance number")
        )

    @staticmethod
    def add_cool_down_time_arg(parser, required=True):
        parser.add_argument(
            '--cool-down-time',
            required=required,
            metavar='<cool-down-time>',
            type=int,
            help=_("Auto-Scaling group cool down time")
        )

    @staticmethod
    def add_lb_listener_arg(parser, required=True):
        parser.add_argument(
            '--lb-listener',
            metavar='load-balance-listener-id',
            required=required,
            help=_("load balance listener id")
        )

    @staticmethod
    def add_health_periodic_audit_method_arg(parser, required=True):
        parser.add_argument(
            '--health-periodic-audit-method',
            required=required,
            metavar='<audit-method>',
            choices=['ELB_AUDIT', 'NOVA_AUDIT'],
            help=_("Auto-Scaling group health periodic audit method")
        )

    @staticmethod
    def add_health_periodic_audit_time_arg(parser, required=True):
        parser.add_argument(
            '--health-periodic-audit-time',
            required=required,
            metavar='<audit-time>',
            choices=['5', '15', '60', '180'],
            type=int,
            help=_("Auto-Scaling group health periodic audit time(min)")
        )

    @staticmethod
    def add_instance_terminate_policy_arg(parser, required=True):
        parser.add_argument(
            '--instance-terminate-policy',
            required=required,
            choices=[
                'OLD_CONFIG_OLD_INSTANCE',
                'OLD_CONFIG_NEW_INSTANCE',
                'OLD_INSTANCE',
                'NEW_INSTANCE'
            ],
            help=_("Auto-Scaling group instance terminate policy")
        )

        # "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
        # "vpc_id": "a8327883-6b07-4497-9c61-68d03ee193a",
        # "networks": [
        #                 {
        #                     "id": "3cd35bca-5a10-416f-8994-f79169559870"
        #                 }
        #             ],
        # "notifications": [
        #                      "EMAIL"
        #                  ],
        # "security_groups": [
        #     {
        #         "id": "23b7b999-0a30-4b48-ae8f-ee201a88a6ab"
        #     }
        # ]


class Config(object):

    @staticmethod
    def add_config_arg(parser):
        parser.add_argument(
            'config',
            metavar="<config>",
            help=_("Configuration to display (ID or name)"),
        )

    @staticmethod
    def add_name_arg(parser):
        parser.add_argument(
            'name',
            metavar='<config-name>',
            help=_("Name of the AS configuration to be created"),
        )

    @staticmethod
    def add_name_option(parser, help_, required=True):
        parser.add_argument(
            '--name',
            required=required,
            metavar='<config-name>',
            help=help_,
        )

    @staticmethod
    def add_instance_option(parser, required=False):
        parser.add_argument(
            '--instance-id',
            required=required,
            metavar='<instance-id>',
            help=_("template server instance id (Either instance-id or "
                   "flavor + image + disk is required)")
        )

    @staticmethod
    def add_flavor_option(parser, required=False):
        parser.add_argument(
            '--flavor',
            required=required,
            metavar='<flavor>',
            help=_("Flavor to assign to configuration (ID or name)")
        )

    @staticmethod
    def add_image_option(parser, help_, required=False):
        parser.add_argument(
            '--image',
            required=required,
            metavar='<image>',
            help=help_,
        )

    @staticmethod
    def add_root_volume_option(parser, required=False):
        parser.add_argument(
            "--root-volume",
            metavar="<volume-type:volume-size(GB)>",
            required=required,
            type=parsetypes.volume_type,
            help=_("Root Volume, volume type [SSD|SATA|SAS], "
                   "volume size should between [40~32768]"
                   "(example: SSD:80)"),
        )

    @staticmethod
    def add_data_volume_option(parser):
        parser.add_argument(
            "--data-volume",
            metavar="<volume-type:volume-size(GB)>",
            required=False,
            default=[],
            type=parsetypes.volume_type,
            dest="data_volumes",
            action='append',
            help=_("Data Volume, volume type [SSD|SATA|SAS], "
                   "volume size should between [10~32768]"
                   "(example: SSD:80, "
                   "Repeat option to set multiple data volumes.)"),
        )

    @staticmethod
    def add_authentication_option(parser):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--key-name',
            metavar='<key-name>',
            help=_("SSH key name, Not support for Window Server "
                   "(Either key-name or admin-pass is required)")
        )
        group.add_argument(
            '--admin-pass',
            metavar='<admin-pass>',
            help=_("SSH key name "
                   "(Either key-name or admin-pass is required)")
        )

    @staticmethod
    def add_file_option(parser):
        parser.add_argument(
            '--file',
            metavar='<dest-filename=source-filename>',
            action='append',
            default=[],
            help=_('File to inject into instance (repeat option to '
                   'set multiple files, max file number is 5)'),
        )

    @staticmethod
    def add_metadata_option(parser):
        parser.add_argument(
            '--metadata',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=_('Set a metadata on this server '
                   '(repeat option to set multiple values)'),
        )
