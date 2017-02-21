#   Copyright 2016 Huawei, Inc. All rights reserved.
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

import mock
from asclient.common import resource as br
from asclient.osc.v1 import quota
from asclient.tests import base
from asclient.v1 import quota_mgr
from asclient.v1 import resource


@mock.patch.object(quota_mgr.QuotaManager, "_list")
class TestListAutoScalingQuota(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestListAutoScalingQuota, self).__init__(*args, **kwargs)

    def setUp(self):
        super(TestListAutoScalingQuota, self).setUp()
        self.cmd = quota.ListQuota(self.app, None)

    def test_list_all_quota(self, mocked):
        _quotas = [
            {
                "type": "scaling_Policy",
                "used": 2,
                "quota": 50,
                "max": 50
            },
            {
                "type": "scaling_Instance",
                "used": 0,
                "quota": 200,
                "max": 1000
            }
        ]
        quotas = [resource.AutoScalingQuota(None, q) for q in _quotas]
        mocked.return_value = br.ListWithMeta(quotas, "Request-ID")

        args = self.check_parser(self.cmd, [], ())
        columns, data = self.cmd.take_action(args)
        mocked.assert_called_once_with("/quotas", key="quotas.resources")

        self.assertEquals(resource.AutoScalingQuota.list_column_names,
                          columns)
        expected = [('scaling_Policy', 50, 2, 50,),
                    ('scaling_Instance', 200, 0, 1000,), ]
        self.assertEquals(expected, data)

    def test_list_quota_of_group(self, mocked):
        _quotas = [
            {
                "type": "scaling_Policy",
                "used": 2,
                "quota": 50,
                "max": 50
            },
            {
                "type": "scaling_Instance",
                "used": 0,
                "quota": 200,
                "max": 1000
            }
        ]
        quotas = [resource.AutoScalingQuota(None, q) for q in _quotas]
        mocked.return_value = br.ListWithMeta(quotas, "Request-ID")

        args = self.check_parser(
            self.cmd,
            ["--group", "group-name"],
            (("group", "group-name"),)
        )

        with self.mocked_group_find as mocked_gf:
            columns, data = self.cmd.take_action(args)
            mocked_gf.assert_called_once_with("group-name")
            mocked.assert_called_once_with("/quotas/" + self._group.id,
                                           key="quotas.resources")
            self.assertEquals(resource.AutoScalingQuota.list_column_names,
                              columns)
            expected = [('scaling_Policy', 50, 2, 50,),
                        ('scaling_Instance', 200, 0, 1000,), ]
            self.assertEquals(expected, data)
