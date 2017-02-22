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
from asclient.common import manager
from asclient.common import utils
from asclient.v1 import resource


class LogManager(manager.Manager):
    """Auto Scaling Log Manager"""

    resource_class = resource.AutoScalingLog

    def list(self, as_group_id, start_time=None, end_time=None, limit=None,
             offset=None):
        """list auto scaling group activity logs

        :param as_group_id:
        :param start_time: datetime
        :param end_time: datetime
        :param limit:
        :param offset:
        :return:
        """
        str_fmt = "%Y-%m-%dT%H:%M:%SZ"
        start_time_str = start_time.strftime(str_fmt) if start_time else None
        end_time_str = end_time.strftime(str_fmt) if end_time else None
        params = utils.remove_empty_from_dict({
            "start_time": start_time_str,
            "end_time": end_time_str,
            "limit": limit,
            "offset": offset,
        })
        url = "/scaling_activity_log/" + as_group_id
        return self._list(url, params=params, key="scaling_activity_log")
