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
from asclient.v1 import resource


class QuotaManager(manager.Manager):
    """Auto Scaling Quota Manager"""

    resource_class = resource.AutoScalingQuota

    def list(self, as_group_id=None):
        """list quotas

        :param as_group_id: if present, show quotas of the group
        :return:
        """
        url = '/quotas' if as_group_id is None else '/quotas/' + as_group_id
        return self._list(url, key='quotas.resources')
