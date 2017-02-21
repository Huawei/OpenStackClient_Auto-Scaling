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
import datetime

import mock
from asclient.common import resource as br
from asclient.osc.v1 import log
from asclient.tests import base
from asclient.v1 import log_mgr
from asclient.v1 import resource


@mock.patch.object(log_mgr.LogManager, "_list")
class TestListAutoScalingLog(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(TestListAutoScalingLog, self).__init__(*args, **kwargs)
        self.logs = [{
            "id": "5109f11b-54ea-4ac5-93fa-5e93e8490448",
            "status": "SUCCESS",
            "description": ("{\"reason\":[{\"change_reason\":\"SCHEDULED\",\""
                            "old_value\":2,\"change_time\":\"2017-02-19T"
                            "13:41:04Z\",\"new_value\":3}]}"),
            "instance_value": 2,
            "desire_value": 3,
            "scaling_value": 1,
            "start_time": "2017-02-19T13:52:32Z",
            "end_time": "2017-02-19T14:03:31Z",
            "instance_added_list": "as-config-TEO_XQF2JJSI",
            "instance_deleted_list": None,
            "instance_removed_list": ""
        }, {
            "id": "b292c0bb-2769-449e-aa23-00099d0ce3cc",
            "status": "SUCCESS",
            "description": ("{\"reason\":[{\"change_reason\":\"SCHEDULED"
                            "\",\"old_value\":1,\"change_time\":\"2017-02-19"
                            "T13:40:00Z\",\"new_value\":2}]}"),
            "instance_value": 1,
            "desire_value": 2,
            "scaling_value": 1,
            "start_time": "2017-02-19T13:40:12Z",
            "end_time": "2017-02-19T13:52:21Z",
            "instance_added_list": "as-config-TEO_LV1JS5P3",
            "instance_deleted_list": None,
            "instance_removed_list": ""
        }]

    def setUp(self):
        super(TestListAutoScalingLog, self).setUp()
        self.cmd = log.ListAutoScalingLog(self.app, None)

    def test_list_as_log(self, mocked):
        args = [
            "--group", "group-id",
            "--start-time", "2017-02-20T00:00:00",
            "--end-time", "2017-02-22T00:00:00",
            "--offset", "10",
            "--limit", "20",
        ]
        verify_args = [
            ("group", "group-id"),
            ("start_time", datetime.datetime(2017, 2, 20)),
            ("end_time", datetime.datetime(2017, 2, 22)),
            ("offset", 10),
            ("limit", 20),
        ]
        parsed_args = self.check_parser(
            self.cmd, args, verify_args
        )

        with self.mocked_group_find as mocked_fg:
            logs = [resource.AutoScalingLog(None, log) for log in self.logs]
            mocked.return_value = br.ListWithMeta(logs, "Request-ID")
            columns, data = self.cmd.take_action(parsed_args)
            mocked_fg.assert_called_once_with("group-id")
            url = "/scaling_activity_log/" + self._group.id
            params = {
                "start_time": "2017-02-20T00:00:00Z",
                "end_time": "2017-02-22T00:00:00Z",
                "offset": 10,
                "limit": 20,
            }
            mocked.assert_called_once_with(url, params=params,
                                           key="scaling_activity_log")

            self.assertEquals(resource.AutoScalingLog.list_column_names,
                              columns)

            expected = [(
                '2017-02-19T13:52:32Z',
                '2017-02-19T14:03:31Z',
                '2/3/1',
                "change_reason='SCHEDULED', change_time='2017-02-19T13:41:04Z'"
                ", new_value='3', old_value='2'",
                'SUCCESS'
            ), (
                '2017-02-19T13:40:12Z',
                '2017-02-19T13:52:21Z',
                '1/2/1',
                "change_reason='SCHEDULED', change_time='2017-02-19T13:40:00Z'"
                ", new_value='2', old_value='1'",
                'SUCCESS'
            )]
            self.assertEquals(expected, data)
