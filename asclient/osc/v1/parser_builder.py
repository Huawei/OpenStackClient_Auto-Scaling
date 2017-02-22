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

    @staticmethod
    def add_group_name_arg(parser):
        parser.add_argument(
            'name',
            metavar='<group-name>',
            help=_("New Auto-Scaling group name")
        )

    @staticmethod
    def add_vpc_opt(parser, required=True):
        parser.add_argument(
            '--vpc',
            metavar='<vpc>',
            required=required,
            help=_("VPC(Router) to assign to the instance (ID or name, "
                   "use openstack router list to get it)")
        )

    @staticmethod
    def add_subnet_opt(parser, required=True):
        parser.add_argument(
            '--subnet',
            metavar='<subnet>',
            default=[],
            action='append',
            required=required,
            dest="subnets",
            help=_("Subnet to assign to the instance (ID or name, "
                   "Repeat option to set multiple subnet, "
                   "max repeat times is 5)")
        )

    @staticmethod
    def add_security_group_opt(parser, required=True):
        parser.add_argument(
            "--security-group",
            metavar="<security-group>",
            default=[],
            required=required,
            dest="security_groups",
            action='append',
            help=_('Security group to assign to the instance (ID or name, '
                   'Repeat option to set multiple security groups)'),
        )

    @staticmethod
    def add_config_id_opt(parser, required=False):
        parser.add_argument(
            '--config',
            required=required,
            metavar='<config>',
            help=_("Auto-Scaling config to assign to the instance "
                   "(ID or name)")
        )

    @staticmethod
    def add_desired_instance_opt(parser, required=False):
        parser.add_argument(
            '--desire-instance',
            required=required,
            metavar='<number>',
            type=int,
            help=_("Auto-Scaling group desired instance number")
        )

    @staticmethod
    def add_max_instance_opt(parser, required=False):
        parser.add_argument(
            '--max-instance',
            required=required,
            metavar='<number>',
            type=int,
            help=_("Auto-Scaling group max instance number")
        )

    @staticmethod
    def add_min_instance_opt(parser, required=False):
        parser.add_argument(
            '--min-instance',
            required=required,
            metavar='<number>',
            type=int,
            help=_("Auto-Scaling group min instance number")
        )

    @staticmethod
    def add_cool_down_opt(parser, required=False):
        parser.add_argument(
            '--cool-down',
            required=required,
            metavar='<seconds>',
            type=int,
            help=_("Auto-Scaling group cool down time (second)")
        )

    @staticmethod
    def add_lb_listener_opt(parser, required=False):
        parser.add_argument(
            '--lb-listener',
            metavar='LB-listener-id',
            required=required,
            help=_("load balance listener id")
        )

    @staticmethod
    def add_health_periodic_audit_method_arg(parser, required=False):
        parser.add_argument(
            '--health-periodic-audit-method',
            required=required,
            metavar='<audit-method>',
            choices=['ELB_AUDIT', 'NOVA_AUDIT'],
            help=_("Auto-Scaling group health periodic audit method, "
                   "NOVA_AUDIT by default, if lb-listen-id present, "
                   "ELB_AUDIT will be used.")
        )

    @staticmethod
    def add_health_periodic_audit_time_arg(parser, required=False):
        parser.add_argument(
            '--health-periodic-audit-time',
            required=required,
            metavar='<minute>',
            choices=[5, 15, 60, 180],
            type=int,
            help=_("Auto-Scaling group health periodic audit time (min), "
                   "5 minutes by default.")
        )

    @staticmethod
    def add_instance_terminate_policy_opt(parser, required=False):
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

    @staticmethod
    def add_del_public_ip_opt(parser, required=False):
        parser.add_argument(
            '--delete-public-ip',
            required=required,
            action="store_true",
            default=False,
            help=_("Delete public-ip when terminate instance "
                   "(False by default)")
        )

    ################
    # List Groups #
    ###############

    @staticmethod
    def add_group_name_opt(parser, help_=None, required=False):
        help_txt = _(help_ if help_ else "Search by group name")
        parser.add_argument(
            '--name',
            required=required,
            metavar='<group-name>',
            help=help_txt,
        )

    @staticmethod
    def add_group_status_opt(parser, required=False):
        parser.add_argument(
            '--status',
            required=required,
            choices=["INSERVICE", "PAUSED", "ERROR"],
            help=_("Search by group status")
        )

    ################
    # Show Group  #
    ###############

    @staticmethod
    def add_group_id_arg(parser):
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_("Group to display (ID or name)")
        )


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
    def add_name_opt(parser, help_, required=True):
        parser.add_argument(
            '--name',
            required=required,
            metavar='<config-name>',
            help=help_,
        )

    @staticmethod
    def add_instance_opt(parser, required=False):
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
    def add_image_opt(parser, help_, required=False):
        parser.add_argument(
            '--image',
            required=required,
            metavar='<image>',
            help=help_,
        )

    @staticmethod
    def add_root_volume_opt(parser, required=False):
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
    def add_data_volume_opt(parser):
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
    def add_authentication_opt(parser):
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
    def add_file_opt(parser):
        parser.add_argument(
            '--file',
            metavar='<dest-filename=source-filename>',
            action='append',
            default=[],
            help=_('File to inject into instance (repeat option to '
                   'set multiple files, max file number is 5)'),
        )

    @staticmethod
    def add_metadata_opt(parser):
        parser.add_argument(
            '--metadata',
            metavar='<key=value>',
            action=parseractions.KeyValueAction,
            help=_('Set a metadata on this server '
                   '(repeat option to set multiple values)'),
        )


class Instance(object):

    @staticmethod
    def add_group_opt(parser):
        parser.add_argument(
            '--group',
            metavar="<group>",
            required=True,
            help=_("Group which the instances belong to (ID or name)"),
        )

    @staticmethod
    def add_lifecycle_status_opt(parser):
        parser.add_argument(
            '--lifecycle-status',
            choices=["INSERVICE", "PENDING", "REMOVING", ],
            help=_("Search by instance lifecycle status"),
        )

    @staticmethod
    def add_health_status_opt(parser):
        parser.add_argument(
            '--health-status',
            choices=["INITIALIZING", "NORMAL", "ERROR", ],
            help=_("Search by instance health status"),
        )

    @staticmethod
    def add_instances_opt(parser, op):
        parser.add_argument(
            '--instance',
            metavar="<instance>",
            required=True,
            default=[],
            dest='instances',
            action="append",
            help=_("Instance to be %s (ID or name), repeat option to set "
                   "multiple instances" % op),
        )

    @staticmethod
    def add_delete_instance_opt(parser):
        parser.add_argument(
            '--delete',
            action="store_true",
            help=_("Delete Instance after remove (Not delete by default)"),
        )


class Log(object):

    @staticmethod
    def add_start_time_option(parser):
        parser.add_argument(
            '--start-time',
            metavar="<yyyy-MM-ddTHH:mm:ss>",
            type=parsetypes.date_type('%Y-%m-%dT%H:%M:%S'),
            help=_("list group activity logs after this time"),
        )

    @staticmethod
    def add_end_time_opt(parser):
        parser.add_argument(
            '--end-time',
            metavar="<yyyy-MM-ddTHH:mm:ss>",
            type=parsetypes.date_type('%Y-%m-%dT%H:%M:%S'),
            help=_("list group activity logs after this time"),
        )


class Policy(object):

    @staticmethod
    def add_policy_id_arg(parser, op):
        parser.add_argument(
            'policy',
            metavar='<policy>',
            help=_("Policy to %s (ID)" % op)
        )

    @staticmethod
    def add_policy_name_arg(parser):
        parser.add_argument(
            'name',
            metavar="<policy-name>",
            help=_("Auto-Scaling policy name"),
        )

    @staticmethod
    def add_group_opt(parser, required=False):
        parser.add_argument(
            '--group',
            metavar="<group>",
            required=required,
            help=_("Group (ID or name) which the policies belong to"),
        )

    @staticmethod
    def add_policy_name_opt(parser, help_=None, required=False):
        help_ = _(help_ if help_ else "search by policy name")
        parser.add_argument(
            '--name',
            metavar="<policy-name>",
            required=required,
            help=help_,
        )

    @staticmethod
    def add_policy_type_opt(parser, help_=None, required=False):
        help_ = _(help_ if help_ else "search by policy type")
        parser.add_argument(
            '--type',
            required=required,
            choices=["ALARM", "SCHEDULED", "RECURRENCE"],
            help=help_,
        )

    @staticmethod
    def add_alarm_id_opt(parser, required=False):
        parser.add_argument(
            '--alarm-id',
            required=required,
            metavar="<alarm-id>",
            help=_("Alarm Id to assign to the policy "
                   "(Only effect when policy-type is ALARM)"),
        )

    @staticmethod
    def add_launch_time_opt(parser, required=False):
        parser.add_argument(
            '--launch-time',
            required=required,
            metavar="<yyyy-MM-ddTHH:mm>",
            type=parsetypes.date_type('%Y-%m-%dT%H:%M'),
            help=_("Schedule launch time"
                   "(Only Effect when policy-type is SCHEDULED)"),
        )

    @staticmethod
    def add_recurrence_opt(parser, required=False):
        parser.add_argument(
            '--recurrence',
            required=required,
            metavar="<type:value>",
            type=parsetypes.recurrence_type,
            help=_("Recurrence type contains ['Daily', 'Weekly', 'Monthly']. "
                   "When type is Daily, value should be HH:ss "
                   "(example: Daily:18:00 means schedule at Everyday's 18:00); "
                   "When type is Weekly, value should be 1-7 (example: "
                   "Weekly:1,3 means schedule at Every Sunday,Wednesday); "
                   "When type is Monthly, value should be 1-31 (example: "
                   "Monthly:1,10,20 means schedule at 1,10,20 of Every Month), "
                   "(Effect only when policy-type is RECURRENCE)"
                   ),
        )

    @staticmethod
    def add_start_time_opt(parser, required=False):
        parser.add_argument(
            '--start-time',
            required=required,
            metavar="<yyyy-MM-ddTHH:mm>",
            type=parsetypes.date_type('%Y-%m-%dT%H:%M'),
            help=_("Recurrence start UTC time "
                   "(Effect only when policy-type is RECURRENCE)"),
        )

    @staticmethod
    def add_end_time_opt(parser, required=False):
        parser.add_argument(
            '--end-time',
            required=required,
            metavar="<yyyy-MM-ddTHH:mm>",
            type=parsetypes.date_type('%Y-%m-%dT%H:%M'),
            help=_("Recurrence end UTC time "
                   "(Effect only when policy-type is RECURRENCE)"),
        )

    @staticmethod
    def add_action_opt(parser, required=False):
        parser.add_argument(
            '--action',
            metavar="<operation:number>",
            required=required,
            type=parsetypes.policy_action_type,
            help=_("Action performed when policy execute, "
                   "operation contains ['ADD', 'REMOVE', 'SET'],"
                   "example: ADD:1 means add 1 instance"),
        )

    @staticmethod
    def add_cool_down_opt(parser, required=False):
        parser.add_argument(
            '--cool-down',
            required=required,
            metavar='<seconds>',
            type=int,
            help=_("Auto-Scaling policy schedule period (second), "
                   "900 seconds by default")
        )
