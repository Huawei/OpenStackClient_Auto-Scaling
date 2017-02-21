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
from asclient.osc.v1 import instance
from asclient.tests import base
from asclient.v1 import instance_mgr
from asclient.v1 import resource
from osc_lib import utils


class InstanceV1BaseTestCase(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(InstanceV1BaseTestCase, self).__init__(*args, **kwargs)
        self._instances = [
            {"instance_id": "dacd968b-2602-470d-a0e2-92a20c2f2b8b",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_group_name": "as-group-teo",
             "life_cycle_state": "INSERVICE", "health_status": "NORMAL",
             "scaling_configuration_name": "as-config-TEO",
             "scaling_configuration_id": "498c242b-54a4-48ec-afcd",
             "create_time": "2017-02-19T13:52:33Z",
             "instance_name": "as-config-TEO_XQF2JJSI"},
            {"instance_id": "4699d02c-6f4b-47e3-be79-8b92c665310b",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_group_name": "as-group-teo",
             "life_cycle_state": "INSERVICE", "health_status": "NORMAL",
             "scaling_configuration_name": "as-config-TEO",
             "scaling_configuration_id": "498c242b-54a4-48ec-afcd",
             "create_time": "2017-02-19T13:40:12Z",
             "instance_name": "as-config-TEO_LV1JS5P3"},
            {"instance_id": "35d9225d-ca47-4d55-bc5d-3858c34610a5",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_group_name": "as-group-teo",
             "life_cycle_state": "INSERVICE", "health_status": "NORMAL",
             "scaling_configuration_name": "as-config-TEO",
             "scaling_configuration_id": "498c242b-54a4-48ec-afcd",
             "create_time": "2017-02-19T08:24:12Z",
             "instance_name": "as-config-TEO_2MKT59WO"}, ]


@mock.patch.object(instance_mgr.InstanceManager, "_list")
class TestListAutoScalingInstance(InstanceV1BaseTestCase):
    def setUp(self):
        super(TestListAutoScalingInstance, self).setUp()
        self.cmd = instance.ListAutoScalingInstance(self.app, None)

    def test_list_as_log(self, mocked):
        args = [
            "--group", "group-id",
            "--lifecycle-status", "INSERVICE",
            "--health-status", "NORMAL",
            "--offset", "10",
            "--limit", "20",
        ]
        verify_args = [
            ("group", "group-id"),
            ("lifecycle_status", "INSERVICE"),
            ("health_status", "NORMAL"),
            ("offset", 10),
            ("limit", 20),
        ]
        parsed_args = self.check_parser(
            self.cmd, args, verify_args
        )

        with self.mocked_group_find as mocked_fg:
            instances = [resource.AutoScalingInstance(None, i)
                         for i in self._instances]
            mocked.return_value = br.ListWithMeta(instances, "Request-ID")
            columns, data = self.cmd.take_action(parsed_args)
            mocked_fg.assert_called_once_with("group-id")
            url = "/scaling_group_instance/%s/list" % self._group.id
            params = {
                "life_cycle_status": "INSERVICE",
                "health_status": "NORMAL",
                "start_number": 10,
                "limit": 20,
            }
            mocked.assert_called_once_with(url, params=params,
                                           key="scaling_group_instances")

            self.assertEquals(resource.AutoScalingInstance.list_column_names,
                              columns)

            expected = [('dacd968b-2602-470d-a0e2-92a20c2f2b8b',
                         'as-config-TEO_XQF2JJSI',
                         'as-group-teo',
                         'as-config-TEO',
                         'INSERVICE',
                         'NORMAL'),
                        ('4699d02c-6f4b-47e3-be79-8b92c665310b',
                         'as-config-TEO_LV1JS5P3',
                         'as-group-teo',
                         'as-config-TEO',
                         'INSERVICE',
                         'NORMAL'),
                        ('35d9225d-ca47-4d55-bc5d-3858c34610a5',
                         'as-config-TEO_2MKT59WO',
                         'as-group-teo',
                         'as-config-TEO',
                         'INSERVICE',
                         'NORMAL')]
            self.assertEquals(expected, data)


@mock.patch.object(instance_mgr.InstanceManager, "list")
@mock.patch.object(instance_mgr.InstanceManager, "_create")
class TestRemoveAutoScalingInstance(InstanceV1BaseTestCase):
    def setUp(self):
        super(TestRemoveAutoScalingInstance, self).setUp()
        self.cmd = instance.RemoveAutoScalingInstance(self.app, None)

    def test_remove_as_instance(self, mock_create, mock_list):
        args = [
            "--group", "group-id",
            "--instance", "dacd968b-2602-470d-a0e2-92a20c2f2b8b",
            "--instance", "as-config-TEO_2MKT59WO",
            "--delete",
        ]
        verify_args = [
            ("group", "group-id"),
            ("instances", ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                           "as-config-TEO_2MKT59WO", ]),
            ("delete", True),
        ]
        parsed_args = self.check_parser(
            self.cmd, args, verify_args
        )

        with self.mocked_group_find as mocked_fg:
            instances = [resource.AutoScalingInstance(None, i)
                         for i in self._instances]
            mock_list.return_value = br.ListWithMeta(instances, "Request-ID")
            mock_create.return_value = br.StrWithMeta('', 'Request-ID-2')
            result = self.cmd.take_action(parsed_args)
            mocked_fg.assert_called_once_with("group-id")
            mock_list.assert_called_once_with(self._group.id)

            url = "/scaling_group_instance/%s/action" % self._group.id
            json = {
                "action": "REMOVE",
                "instances_id": ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                                 "35d9225d-ca47-4d55-bc5d-3858c34610a5", ],
                "instance_delete": "yes"
            }

            mock_create.assert_called_once_with(url, json=json, raw=True)
            self.assertEquals('done', result)

    def test_soft_remove_as_instance(self, mock_create, mock_list):
        args = [
            "--group", "group-id",
            "--instance", "dacd968b-2602-470d-a0e2-92a20c2f2b8b",
            "--instance", "35d9225d-ca47-4d55-bc5d-3858c34610a5",
        ]
        verify_args = [
            ("group", "group-id"),
            ("instances", ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                           "35d9225d-ca47-4d55-bc5d-3858c34610a5", ]),
        ]
        parsed_args = self.check_parser(
            self.cmd, args, verify_args
        )

        with self.mocked_group_find as mocked_fg:
            instances = [resource.AutoScalingInstance(None, i)
                         for i in self._instances]
            mock_list.return_value = br.ListWithMeta(instances, "Request-ID")
            mock_create.return_value = br.StrWithMeta('', 'Request-ID-2')
            result = self.cmd.take_action(parsed_args)
            mocked_fg.assert_called_once_with("group-id")
            mock_list.assert_called_once_with(self._group.id)

            url = "/scaling_group_instance/%s/action" % self._group.id
            json = {
                "action": "REMOVE",
                "instances_id": ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                                 "35d9225d-ca47-4d55-bc5d-3858c34610a5", ],
            }

            mock_create.assert_called_once_with(url, json=json, raw=True)
            self.assertEquals('done', result)


@mock.patch.object(utils, "find_resource")
@mock.patch.object(instance_mgr.InstanceManager, "_create")
class TestAddAutoScalingInstance(InstanceV1BaseTestCase):

    def setUp(self):
        super(TestAddAutoScalingInstance, self).setUp()
        self.cmd = instance.AddAutoScalingInstance(self.app, None)

    def test_add_as_instance(self, mock_create, mock_find_resource):
        args = [
            "--group", "group-id",
            "--instance", "dacd968b-2602-470d-a0e2-92a20c2f2b8b",
            "--instance", "35d9225d-ca47-4d55-bc5d-3858c34610a5",
        ]
        verify_args = [
            ("group", "group-id"),
            ("instances", ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                           "35d9225d-ca47-4d55-bc5d-3858c34610a5", ]),
        ]
        parsed_args = self.check_parser(
            self.cmd, args, verify_args
        )

        with self.mocked_group_find as mocked_fg:
            mock_find_resource.side_effect = [
                br.Resource(None, dict(id=parsed_args.instances[0])),
                br.Resource(None, dict(id=parsed_args.instances[1])),
            ]
            mock_create.return_value = br.StrWithMeta('', 'Request-ID-2')
            result = self.cmd.take_action(parsed_args)
            mocked_fg.assert_called_once_with("group-id")

            url = "/scaling_group_instance/%s/action" % self._group.id
            json = {
                "action": "ADD",
                "instances_id": ["dacd968b-2602-470d-a0e2-92a20c2f2b8b",
                                 "35d9225d-ca47-4d55-bc5d-3858c34610a5", ],
            }
            mock_create.assert_called_once_with(url, json=json, raw=True)
            self.assertEquals('done', result)
