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
from osc_lib import utils as formatter

from asclient.common import display
from asclient.common import resource


class AutoScalingGroup(resource.Resource, display.Display):
    """AutoScaling group resource instance."""

    formatter = {
        "Security Groups": formatter.format_list_of_dicts,
        "Notifications": formatter.format_list,
        "Networks": formatter.format_list_of_dicts,
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
        "Notifications",
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
