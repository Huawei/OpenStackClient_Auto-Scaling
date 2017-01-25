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
