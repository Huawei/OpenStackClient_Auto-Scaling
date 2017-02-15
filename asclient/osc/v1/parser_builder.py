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
from asclient.common.i18n import _


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
    def add_name_arg(parser, required=True):
        parser.add_argument(
            '--name',
            required=required,
            metavar='<config-name>',
            help=_("Auto-Scaling configuration name")
        )

    @staticmethod
    def add_instance_arg(parser, required=False):
        parser.add_argument(
            '--instance',
            required=required,
            metavar='<instance-id>',
            help=_("cloud server instance id")
        )

    @staticmethod
    def add_flavor_arg(parser, required=False):
        parser.add_argument(
            '--flavor',
            required=required,
            metavar='<flavor>',
            help=_("Create with this flavor (name or ID)")
        )

    @staticmethod
    def add_image_arg(parser, required=False):
        parser.add_argument(
            '--image',
            required=required,
            metavar='<image>',
            help=_("Create from this image (name or ID)")
        )

    @staticmethod
    def add_root_volume_arg(parser, required=True):
        group = parser.add_argument_group('Root disk volume')
        group.add_argument(
            '--root-volume-type',
            required=required,
            metavar='<volume-type>',
            choices=['SSD', 'SATA', 'SAS'],
            help=_("system disk volume type [SSD|SATA|SAS]")
        )
        group.add_argument(
            '--root-volume-size',
            required=required,
            metavar='<size>',
            type=int,
            help=_("system disk volume size in GB")
        )

    @staticmethod
    def add_data_volume_arg(parser, required=False):
        group = parser.add_argument_group('Data disk volume')
        group.add_argument(
            '--data-volume-type',
            required=required,
            metavar='<volume-type>',
            choices=['SSD', 'SATA', 'SAS'],
            help=_("data disk volume type [SSD|SATA|SAS]")
        )
        group.add_argument(
            '--data-volume-size',
            required=required,
            metavar='<size>',
            type=int,
            help=_("data disk volume size in GB")
        )

    @staticmethod
    def add_key_name_arg(parser, required=False):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--key-name',
            required=required,
            metavar='<key-name>',
            help=_("SSH key name (Could not used for Window Server),"
                   " Required if admin-pass is missing")
        )
        group.add_argument(
            '--admin-pass',
            required=required,
            metavar='<admin-pass>',
            help=_("SSH key name (Could not used for Window Server),"
                   " Required if admin-pass is missing")
        )