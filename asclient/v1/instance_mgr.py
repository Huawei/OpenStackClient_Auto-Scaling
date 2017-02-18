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


class InstanceManager(manager.Manager):
    """Auto Scaling Instance Manager"""

    resource_class = resource.AutoScalingInstance

    def list(self, as_group_id, lifecycle_status=None, health_status=None,
             limit=None, offset=None):
        """list auto scaling instances of an auto-scaling group

        :param as_group_id:
        :param lifecycle_status: ["INSERVICE", "PENDING", "REMOVING"]
        :param health_status: ["INITIALIZING", "NORMAL", "ERROR",]
        :param limit:
        :param offset:
        :rtype :class: [resource.AutoScalingInstance]
        :return:
        """
        params = utils.remove_empty_from_dict({
            "life_cycle_status": lifecycle_status,
            "health_status": health_status,
            "limit": limit,
            "start_number": offset,
        })
        url = "/scaling_group_instance/%s/list" % as_group_id
        return self._list(url, params=params, key="scaling_group_instances")

    def remove_instances(self, as_group_id, instance_ids, delete_instance=None):
        """batch remove instances of a group

        Remove instance preconditions:
        1. instance lifecycle status should be INSERVICE
        2. Instance group is not scaling
        3. After remove, total instance number should not less than
        min-instance-number
        :param as_group_id: remove instance belong to the group
        :param instance_ids: instances which should be removed
        :param delete_instance: delete instance after remove, False by default
        :return:
        """
        json = utils.remove_empty_from_dict({
            "action": "REMOVE",
            "instances_id": instance_ids,
            "instance_delete": "yes" if delete_instance else None
        })
        url = "/scaling_group_instance/%s/action" % as_group_id
        return self._create(url, json=json, raw=True)

    def add_instances(self, as_group_id, instance_ids):
        """batch add instances to a group

        Remove instance preconditions:
        1. Instance group's status should be INSERVICE, and is not scaling
        2. After add, total instance number should not be great than
        max-instance-number
        :param as_group_id: remove instance belong to the group
        :param instance_ids: instances which should be removed
        :return:
        """
        json = utils.remove_empty_from_dict({
            "action": "ADD",
            "instances_id": instance_ids,
        })
        url = "/scaling_group_instance/%s/action" % as_group_id
        return self._create(url, json=json, raw=True)