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

from asclient.common import manager
from asclient.common import utils
from asclient.v1 import resource


class GroupManager(manager.Manager):
    """Auto Scaling Group Manager"""

    resource_class = resource.AutoScalingGroup

    # def create(self, name, as_config_id, desire_instance_number
    #          start_number=None, limit=None):
    #     {
    #         "scaling_group_name": "GroupNameTest",
    #         "scaling_configuration_id": "47683a91-93ee-462a-a7d7-484c006f4440",
    #         "desire_instance_number": 0,
    #         "min_instance_number": 0,
    #         "max_instance_number": 0,
    #         "cool_down_time": 200,
    #         "health_periodic_audit_method": "NOVA_AUDIT",
    #         "health_periodic_audit_time": "5",
    #         "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
    #         "vpc_id": "a8327883-6b07-4497-9c61-68d03ee193a",
    #         "networks": [
    #             {
    #                 "id": "3cd35bca-5a10-416f-8994-f79169559870"
    #             }
    #         ],
    #         "notifications": [
    #             "EMAIL"
    #         ],
    #         "security_groups": [
    #             {
    #                 "id": "23b7b999-0a30-4b48-ae8f-ee201a88a6ab"
    #             }
    #         ]
    #     }
    #
    #     params = utils.remove_empty_from_dict({
    #         "scaling_group_name": name,
    #         "scaling_group_status": status,
    #         "scaling_configuration_id": as_config_id,
    #         "start_number": start_number,
    #         "limit": limit,
    #     })
    #     return self._list("/scaling_group",
    #                       params=params,
    #                       key='scaling_groups')

    def list(self, name=None, status=None, as_config_id=None,
             start_number=None, limit=None):
        params = utils.remove_empty_from_dict({
            "scaling_group_name": name,
            "scaling_group_status": status,
            "scaling_configuration_id": as_config_id,
            "start_number": start_number,
            "limit": limit,
        })
        return self._list("/scaling_group",
                          params=params,
                          key='scaling_groups')
