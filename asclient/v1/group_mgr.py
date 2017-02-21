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
from keystoneauth1 import exceptions

from asclient.common import exceptions as execs
from asclient.common import manager
from asclient.common import utils
from asclient.common.i18n import _
from asclient.v1 import resource


class GroupManager(manager.Manager):
    """Auto Scaling Group Manager"""

    resource_class = resource.AutoScalingGroup

    def create(self, name, vpc_id, subnets, security_groups,
               as_config_id=None, desire_instance_number=None,
               max_instance_number=None, min_instance_number=None,
               cool_down_time=None, lb_listener_id=None,
               health_periodic_audit_time=None,
               health_periodic_audit_method=None,
               instance_terminate_policy=None, delete_public_ip=None,
               notifications=None, availability_zones=None):
        """create new auto scaling group"""
        json = utils.remove_empty_from_dict({
            "scaling_group_name": name,
            "vpc_id": vpc_id,
            "networks": [dict(id=subnet) for subnet in subnets],
            "security_groups": [dict(id=sg) for sg in security_groups],
            "scaling_configuration_id": as_config_id,
            "lb_listener_id": lb_listener_id,
            "desire_instance_number": desire_instance_number,
            "min_instance_number": min_instance_number,
            "max_instance_number": max_instance_number,
            "cool_down_time": cool_down_time,
            "health_periodic_audit_method": health_periodic_audit_method,
            "health_periodic_audit_time": health_periodic_audit_time,
            "instance_terminate_policy": instance_terminate_policy,
            "notifications": notifications,
            "delete_publicip": delete_public_ip,
            "availability_zones": availability_zones,
        })
        return self._create("/scaling_group", json=json)

    def edit(self, as_group_id, name=None, subnets=None, security_groups=None,
             as_config_id=None, desire_instance_number=None,
             max_instance_number=None, min_instance_number=None,
             cool_down_time=None, lb_listener_id=None,
             health_periodic_audit_time=None,
             health_periodic_audit_method=None,
             instance_terminate_policy=None, delete_public_ip=None,
             notifications=None, availability_zones=None):
        """create new auto scaling group"""
        json = utils.remove_empty_from_dict({
            "scaling_group_name": name,
            "networks": [dict(id=subnet) for subnet in subnets],
            "security_groups": [dict(id=sg) for sg in security_groups],
            "scaling_configuration_id": as_config_id,
            "lb_listener_id": lb_listener_id,
            "desire_instance_number": desire_instance_number,
            "min_instance_number": min_instance_number,
            "max_instance_number": max_instance_number,
            "cool_down_time": cool_down_time,
            "health_periodic_audit_method": health_periodic_audit_method,
            "health_periodic_audit_time": health_periodic_audit_time,
            "instance_terminate_policy": instance_terminate_policy,
            "notifications": notifications,
            "delete_publicip": delete_public_ip,
            "availability_zones": availability_zones,
        })
        return self._update_all("/scaling_group/" + as_group_id, json=json)

    def find(self, id_or_name):
        """find auto scaling group by id or name

        exactly match will be performed
        :param id_or_name:
        :rtype: resource.AutoScalingGroup
        :return: AutoScalingGroup with id or name matches id_or_name
        """
        try:
            return self.get(id_or_name)
        except exceptions.ClientException as e:
            pass

        results = self.list(name=id_or_name)
        results = [result for result in results
                   if result.name == id_or_name]
        matched_number = len(results)
        if matched_number > 1:
            raise execs.NotUniqueMatch
        elif matched_number == 1:
            return results[0]

        message = _("No Auto Scaling Group with ID or name of "
                    "'%s' exists.") % id_or_name
        raise exceptions.NotFound(message)

    def list(self, name=None, status=None, as_config_id=None,
             limit=None, offset=None):
        """list auto scaling groups

        :param name: group name
        :param status: one of ["INSERVICE", "PAUSED", "ERROR"]
        :param as_config_id: auto scaling configuration id
        :param limit:
        :param offset:
        :rtype: list of resource.AutoScalingGroup
        :return:
        """
        params = utils.remove_empty_from_dict({
            "scaling_group_name": name,
            "scaling_group_status": status,
            "scaling_configuration_id": as_config_id,
            "start_number": offset,
            "limit": limit,
        })
        return self._list("/scaling_group",
                          params=params,
                          key='scaling_groups')

    def get(self, group_id):
        """get auto scaling group

        :param group_id:
        :return:
        :rtype: resource.AutoScalingGroup
        """
        return self._get("/scaling_group/" + group_id, key="scaling_group")

    def resume(self, group_id):
        """resume auto scaling group

        :param group_id:
        :return:
        """
        return self._create("/scaling_group/%s/action" % group_id,
                            json=dict(action="resume"),
                            raw=True)

    def pause(self, group_id):
        """pause auto scaling group

        :param group_id:
        :return:
        """
        return self._create("/scaling_group/%s/action" % group_id,
                            json=dict(action="pause"),
                            raw=True)

    def delete(self, group_id):
        """delete auto scaling group

        :param group_id:
        :return:
        """
        return self._delete("/scaling_group/" + group_id, raw=True)
