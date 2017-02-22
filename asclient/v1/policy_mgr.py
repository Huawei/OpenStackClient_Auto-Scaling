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

from asclient.common.i18n import _
from asclient.common import manager
from asclient.common import utils
from asclient.common.i18n import _
from asclient.v1 import resource


class PolicyManager(manager.Manager):
    """Auto Scaling Policy Manager"""

    resource_class = resource.AutoScalingPolicy

    def find(self, id_or_name):
        """find auto scaling policy by id or name

        exactly match will be performed
        :param id_or_name:
        :rtype: resource.AutoScalingPolicy
        :return: AutoScalingPolicy which id or name matches id_or_name
        """
        try:
            return self.get(id_or_name)
        except exceptions.ClientException:
            pass

        # TODO(Woo) list need as group id now.
        # results = self.list(name=id_or_name)
        # matched_number = len(results)
        # if matched_number > 1:
        #     raise execs.NotUniqueMatch
        # elif matched_number == 1:
        #     return results[0]

        message = _("No Auto Scaling Group with ID or name of "
                    "'%s' exists.") % id_or_name
        raise exceptions.NotFound(message)

    def list(self, as_group_id, name=None, type_=None, limit=None, offset=None):
        """list policy for auto scaling group

        :param as_group_id:
        :param name:
        :param type_:
        :param limit:
        :param offset:
        :return:
        :rtype: [resource.AutoScalingPolicy]
        """
        params = utils.remove_empty_from_dict({
            "scaling_policy_name": name,
            "scaling_policy_type": type_,
            "start_number": offset,
            "limit": limit,
        })

        url = "/scaling_policy/%s/list" % as_group_id
        return self._list(url, params=params, key="scaling_policies")

    def get(self, as_policy_id):
        """get auto scaling policy detail

        :param as_policy_id:
        :return:
        :rtype: resource.AutoScalingPolicy
        """
        url = "/scaling_policy/" + as_policy_id
        return self._get(url, key="scaling_policy")

    def create(self, as_group_id, name, type_, cool_down=None, alarm_id=None,
               launch_time=None, start_time=None, end_time=None,
               recurrence_type=None, recurrence_value=None, operation=None,
               instance_number=None):
        """create a new policy

        :param as_group_id:
        :param name: policy name
        :param type_: policy type, ["ALARM", "SCHEDULED", "RECURRENCE"]
        :param cool_down: Auto-Scaling policy schedule period (second),
                        900 seconds by default
        :param alarm_id: Alarm Id to assign to the policy (Only effect when
                        policy-type is ALARM)
        :param launch_time: Schedule launch time(Only Effect when policy-type
                            is SCHEDULED)
        :param start_time: Recurrence start UTC time (Effect only when policy-
                        type is RECURRENCE)
        :param end_time: Recurrence end UTC time (Effect only when policy-type
                        is RECURRENCE)
        :param recurrence_type: Recurrence type contains ['Daily', 'Weekly',
                        'Monthly'] (Effect only when policy-type is RECURRENCE)
        :param recurrence_value: When type is Daily, value should be HH:ss
                        (example: Daily:18:00 means schedule at Everyday's
                        18:00); When type is Weekly, value should be 1-7
                        (example: Weekly:1,3 means schedule at Every
                        Sunday,Wednesday); When type is Monthly, value should
                        be 1-31 (example: Monthly:1,10,20 means schedule at
                        1,10,20 of Every Month)
        :param operation: Action performed when policy execute, operation
                        contains ['ADD', 'REMOVE', 'SET']
        :param instance_number: Instance numbers to operate
        :return:
        """

        str_fmt = "%Y-%m-%dT%H:%MZ"
        start_time_str = start_time.strftime(str_fmt) if start_time else None
        end_time_str = end_time.strftime(str_fmt) if end_time else None
        launch_time = launch_time.strftime(str_fmt) if launch_time else None

        if recurrence_type == 'Daily':
            launch_time = recurrence_value
            recurrence_value = None

        json = utils.remove_empty_from_dict({
            "scaling_policy_name": name,
            "scaling_policy_action": utils.remove_empty_from_dict({
                "operation": operation,
                "instance_number": instance_number
            }),
            "cool_down_time": cool_down,
            "alarm_id": alarm_id,
            "scheduled_policy": utils.remove_empty_from_dict({
                "launch_time": launch_time,
                "recurrence_type": recurrence_type,
                "recurrence_value": recurrence_value,
                "start_time": start_time_str,
                "end_time": end_time_str
            }),
            "scaling_policy_type": type_,
            "scaling_group_id": as_group_id
        })
        return self._create("/scaling_policy", json=json)

    def edit(self, as_policy_id, name=None, type_=None, cool_down=None,
             alarm_id=None, launch_time=None, start_time=None, end_time=None,
             recurrence_type=None, recurrence_value=None, operation=None,
             instance_number=None):
        """Edit a policy

        :param as_policy_id: the policy to edit
        :param name: policy name
        :param type_: policy type, ["ALARM", "SCHEDULED", "RECURRENCE"]
        :param cool_down: Auto-Scaling policy schedule period (second),
                        900 seconds by default
        :param alarm_id: Alarm Id to assign to the policy (Only effect when
                        policy-type is ALARM)
        :param launch_time: Schedule launch time(Only Effect when policy-type
                            is SCHEDULED)
        :param start_time: Recurrence start UTC time (Effect only when policy-
                        type is RECURRENCE)
        :param end_time: Recurrence end UTC time (Effect only when policy-type
                        is RECURRENCE)
        :param recurrence_type: Recurrence type contains ['Daily', 'Weekly',
                        'Monthly'] (Effect only when policy-type is RECURRENCE)
        :param recurrence_value: When type is Daily, value should be HH:ss
                        (example: Daily:18:00 means schedule at Everyday's
                        18:00); When type is Weekly, value should be 1-7
                        (example: Weekly:1,3 means schedule at Every
                        Sunday,Wednesday); When type is Monthly, value should
                        be 1-31 (example: Monthly:1,10,20 means schedule at
                        1,10,20 of Every Month)
        :param operation: Action performed when policy execute, operation
                        contains ['ADD', 'REMOVE', 'SET']
        :param instance_number: Instance numbers to operate
        :return:
        """

        str_fmt = "%Y-%m-%dT%H:%MZ"
        start_time_str = start_time.strftime(str_fmt) if start_time else None
        end_time_str = end_time.strftime(str_fmt) if end_time else None
        launch_time = launch_time.strftime(str_fmt) if launch_time else None

        if recurrence_type == 'Daily':
            launch_time = recurrence_value
            recurrence_value = None

        json = utils.remove_empty_from_dict({
            "scaling_policy_name": name,
            "scaling_policy_action": utils.remove_empty_from_dict({
                "operation": operation,
                "instance_number": instance_number
            }),
            "cool_down_time": cool_down,
            "alarm_id": alarm_id,
            "scheduled_policy": utils.remove_empty_from_dict({
                "launch_time": launch_time,
                "recurrence_type": recurrence_type,
                "recurrence_value": recurrence_value,
                "start_time": start_time_str,
                "end_time": end_time_str
            }),
            "scaling_policy_type": type_,
        })
        return self._update_all("/scaling_policy/" + as_policy_id, json=json)

    def pause(self, as_policy_id):
        """pause auto scaling policy

        :param as_policy_id:
        :return:
        """
        url = "/scaling_policy/%s/action" % as_policy_id
        return self._create(url, json=dict(action="pause"), raw=True)

    def resume(self, as_policy_id):
        """resume auto scaling policy

        :param as_policy_id:
        :return:
        """
        url = "/scaling_policy/%s/action" % as_policy_id
        return self._create(url, json=dict(action="resume"), raw=True)

    def execute(self, as_policy_id):
        """resume auto scaling policy

        :param as_policy_id:
        :return:
        """
        url = "/scaling_policy/%s/action" % as_policy_id
        return self._create(url, json=dict(action="execute"), raw=True)

    def delete(self, as_policy_id):
        """delete auto scaling policy

        :param as_policy_id:
        :return:
        """
        url = "/scaling_policy/" + as_policy_id
        return self._delete(url)
