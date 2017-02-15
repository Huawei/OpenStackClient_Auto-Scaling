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


class DesktopUserManager(manager.Manager):
    """Desktop User API management"""

    resource_class = resource.DesktopUser

    def list(self, name=None, email=None, marker=None, limit=None):
        params = utils.remove_empty_from_dict({
            "user_name": name,
            "user_email": email,
            "marker": marker,
            "limit": limit
        })
        return self._list("/desktop-users", params=params, key="users")

    def list_login_records(self, start_time=None, end_time=None,
                           user_name=None, computer_name=None,
                           terminal_type=None, offset=None, limit=None):
        str_fmt = "%Y-%m-%dT%H:%MZ"
        start_time_str = start_time.strftime(str_fmt) if start_time else None
        end_time_str = end_time.strftime(str_fmt) if end_time else None

        params = utils.remove_empty_from_dict({
            "start_time": start_time_str,
            "end_time": end_time_str,
            "user_name": user_name,
            "computer_name": computer_name,
            "terminal_type": terminal_type,
            "offset": offset,
            "limit": limit,
        })
        return self._list("/desktop-users/login-records",
                          params=params,
                          key="records",
                          resource_class=resource.DesktopLoginRecords)
