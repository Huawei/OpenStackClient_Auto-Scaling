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
import json

import six
from osc_lib import utils as formatter

from asclient.common import display
from asclient.common import resource


class AutoScalingGroup(resource.Resource, display.Display):
    """AutoScaling group resource instance."""

    formatter = {
        "Security Groups": formatter.format_list_of_dicts,
        "Notifications": formatter.format_list,
        "Networks": formatter.format_list_of_dicts,
        "Available Zones": formatter.format_list,
    }

    show_column_names = [
        "ID",
        "Name",
        "VPC id",
        "Networks",
        "Security Groups",
        "Instance(Current/desire/min/max)",
        "Scaling Configuration Id",
        "Scaling Configuration Name",
        "Cool down time",
        "LB listener id",
        "Health periodic audit method",
        "Health periodic audit time",
        "Instance Terminate Policy",
        "Scaling",
        "Delete Public IP",
        "Available Zones",
        "Create Time",
        "Status",
    ]

    list_column_names = [
        "ID",
        "Name",
        "Instance(Current/desire/min/max)",
        "Config Id",
        "Status"
    ]

    column_2_property = {
        "Instance(Current/desire/min/max)": "instance_number",
        "Delete Public IP": "delete_publicip",
        "Scaling": "is_scaling",
    }

    @property
    def id(self):
        return self.scaling_group_id

    @property
    def name(self):
        return self.scaling_group_name

    @property
    def status(self):
        return self.scaling_group_status

    @property
    def config_id(self):
        return self.scaling_configuration_id

    @property
    def instance_number(self):
        numbers = (self.current_instance_number,
                   self.desire_instance_number,
                   self.min_instance_number,
                   self.max_instance_number,)
        return "%d/%d/%d/%d" % numbers


class AutoScalingConfig(resource.Resource, display.Display):
    """AutoScaling configuration resource instance."""

    show_column_names = [
        "ID",
        "Name",
        "Disk",
        # "Instance ID",
        # "Instance Name",
        "Flavor",
        "Image",
        "Key Name",
        "Public IP",
        # "User Data",
        "Metadata",
        "Create Time",
    ]

    list_column_names = [
        "ID",
        "Name",
        "Image",
        "Create Time",
    ]

    formatter = {
        "Disk": formatter.format_list_of_dicts,
        "Metadata": formatter.format_dict,
    }

    @property
    def id(self):
        return self.scaling_configuration_id

    @property
    def name(self):
        return self.scaling_configuration_name

    @property
    def flavor(self):
        return self.instance_config["flavorRef"]

    @property
    def key_name(self):
        return self.instance_config["key_name"]

    @property
    def metadata(self):
        return self.instance_config["metadata"]

    # @property
    # def instance_id(self):
    #     return self.instance_config["instance_id"]
    #
    # @property
    # def instance_name(self):
    #     return self.instance_config["instance_name"]

    @property
    def public_ip(self):
        return self.instance_config["public_ip"]

    @property
    def disk(self):
        return self.instance_config["disk"]

    @property
    def image(self):
        return self.instance_config["imageRef"]

    # @property
    # def user_data(self):
    #     return self.instance_config["user_data"]


class AutoScalingInstance(resource.Resource, display.Display):
    """AutoScaling instance resource instance"""

    list_column_names = [
        "Instance ID",
        "Instance Name",
        "AS Group Name",
        "AS Config Name",
        "Lifecycle Status",
        "Health Status",
    ]

    column_2_property = {
        "AS Group Name": "scaling_group_name",
        "AS Config Name": "scaling_configuration_name",
        "Lifecycle Status": "life_cycle_state",
    }

    @property
    def id(self):
        return self.instance_id

    @property
    def name(self):
        return self.instance_name


class AutoScalingLog(resource.Resource, display.Display):
    """AutoScaling activity log resource instance"""

    list_column_names = [
        "Scaling Time(Start->End)",
        "Current/Desire/Scaling",
        "Scaling Reason",
        "Modified Instances",
        "Status",
    ]

    column_2_property = {
        "Current/Desire/Scaling": "instance_number",
        "Scaling Time(Start->End)": "scaling_time",
    }

    @property
    def instance_number(self):
        return "%d/%d/%d" % (self.instance_value,
                             self.desire_value,
                             self.scaling_value,)

    @property
    def scaling_time(self):
        return self.start_time + '\n' + self.end_time

    @property
    def modified_instances(self):
        output = ""
        if self.instance_added_list:
            output += "added:"
            output += self.instance_added_list

        if self.instance_removed_list:
            output += "\nremoved:"
            output += self.instance_removed_list

        if self.instance_deleted_list:
            output += "\ndeleted:"
            output += self.instance_deleted_list

        return output

    @property
    def scaling_reason(self):
        desc = json.loads(self.description)
        return '\n\n'.join(formatter.format_dict(i)
                           for i in desc["reason"])


class AutoScalingQuota(resource.Resource, display.Display):
    """AutoScaling Quota resource instance"""

    list_column_names = [
        "type",
        "quota",
        "used",
        "max",
    ]


def format_schedule_policy(schedule):
    ordered = [
        "recurrence_type",
        "recurrence_value",
        "launch_time",
        "start_time",
        "end_time",
    ]
    output = ""
    for s in ordered:
        if s in schedule:
            output = output + s + "='" + six.text_type(schedule[s]) + "', "
    return output[:-2]


class AutoScalingPolicy(resource.Resource, display.Display):
    """AutoScaling policy resource instance"""

    list_column_names = [
        # "Group Id",
        "Policy ID",
        "Policy Name",
        "Policy Type",
        "CoolDown(s)",
        "Trigger Action",
        "Status",
    ]

    show_column_names = [
        "Group Id",
        "Policy ID",
        "Policy Name",
        "Policy Type",
        "Alarm Id",
        "CoolDown(s)",
        "Scheduled Policy",
        "Trigger Action",
        "Create Time",
        "Status",
    ]

    column_2_property = {
        "Policy ID": "scaling_policy_id",
        "Policy Name": "scaling_policy_name",
        "Group Id": "scaling_group_id",
        "Policy Type": "scaling_policy_type",
        "CoolDown(s)": "cool_down_time",
    }

    formatter = {
        "Scheduled Policy": format_schedule_policy,
    }

    @property
    def id(self):
        return self.scaling_policy_id

    @property
    def name(self):
        return self.scaling_policy_name

    @property
    def status(self):
        return self.policy_status

    @property
    def trigger_action(self):
        if self.scaling_policy_action:
            operation = self.scaling_policy_action["operation"]
            instance_number = self.scaling_policy_action["instance_number"]
            return "%s %s" % (operation, instance_number)
        return None
