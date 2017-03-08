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
from asclient.osc.v1 import group
from asclient.tests import base
from asclient.v1 import group_mgr
from asclient.v1 import resource
from keystoneauth1 import exceptions


class AutoScalingGroupV1BaseTestCase(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(AutoScalingGroupV1BaseTestCase, self).__init__(*args, **kwargs)
        self._groups = [
            {
                "networks": [
                    {
                        "id": "f5ebe00f-3ac1-4ec5-9175-090d9d43e4ef"
                    }
                ],
                "detail": None,
                "notifications": [],
                "scaling_group_name": "Woo-Test-1",
                "scaling_group_id": "f5da912c-4525-4edf-b418-cc1c8e077298",
                "scaling_group_status": "PAUSED",
                "scaling_configuration_id":
                    "498c242b-54a4-48ec-afcd-bc21dd612b57",
                "scaling_configuration_name": "as-config-TEO",
                "current_instance_number": 0,
                "desire_instance_number": 1,
                "min_instance_number": 1,
                "max_instance_number": 3,
                "cool_down_time": 900,
                "lb_listener_id": "038a1208f15b47ab8c2f5f4238c9e783",
                "available_zones": [
                    "eu-de-01"
                ],
                "security_groups": [
                    {
                        "id": "d3e2e1ad-b7f2-414c-9b5a-2d485686a96a"
                    }
                ],
                "create_time": "2017-02-20T06:41:25Z",
                "vpc_id": "f496ae99-6e3e-4957-924d-087ca5b0b2f0",
                "health_periodic_audit_method": "ELB_AUDIT",
                "health_periodic_audit_time": 15,
                "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
                "is_scaling": False,
                "delete_publicip": True
            },
            {
                "networks": [
                    {
                        "id": "f5ebe00f-3ac1-4ec5-9175-090d9d43e4ef"
                    }
                ],
                "detail": None,
                "notifications": [],
                "scaling_group_name": "as-group-teo",
                "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
                "scaling_group_status": "INSERVICE",
                "scaling_configuration_id":
                    "498c242b-54a4-48ec-afcd-bc21dd612b57",
                "scaling_configuration_name": "as-config-TEO",
                "current_instance_number": 2,
                "desire_instance_number": 2,
                "min_instance_number": 0,
                "max_instance_number": 4,
                "cool_down_time": 200,
                "lb_listener_id": "038a1208f15b47ab8c2f5f4238c9e783",
                "available_zones": [
                    "eu-de-01"
                ],
                "security_groups": [
                    {
                        "id": "d3e2e1ad-b7f2-414c-9b5a-2d485686a96a"
                    }
                ],
                "create_time": "2016-11-29T12:57:52Z",
                "vpc_id": "f496ae99-6e3e-4957-924d-087ca5b0b2f0",
                "health_periodic_audit_method": "ELB_AUDIT",
                "health_periodic_audit_time": 5,
                "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
                "is_scaling": False,
                "delete_publicip": False
            },
            {
                "networks": [
                    {
                        "id": "668ad9b0-6f3f-46ee-8972-0b2a42909bcc"
                    }
                ],
                "detail": None,
                "notifications": [],
                "scaling_group_name": "as-group-lorc-Romania1",
                "scaling_group_id": "56e25174-c317-4be1-9fbd-17d5aff10ad5",
                "scaling_group_status": "PAUSED",
                "scaling_configuration_id": None,
                "scaling_configuration_name": None,
                "current_instance_number": 0,
                "desire_instance_number": 2,
                "min_instance_number": 1,
                "max_instance_number": 4,
                "cool_down_time": 900,
                "lb_listener_id": None,
                "available_zones": [
                    "eu-de-02"
                ],
                "security_groups": [
                    {
                        "id": "1e225447-928a-431f-855a-0857385788c5"
                    }
                ],
                "create_time": "2016-11-15T13:44:00Z",
                "vpc_id": "facf3196-1862-4b3f-b802-9f46ad8908a3",
                "health_periodic_audit_method": "NOVA_AUDIT",
                "health_periodic_audit_time": 5,
                "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
                "is_scaling": False,
                "delete_publicip": False
            }
        ]


@mock.patch.object(group_mgr.GroupManager, "_list")
class TestListAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestListAutoScalingGroup, self).setUp()
        self.cmd = group.ListAutoScalingGroup(self.app, None)

    def test_list_group(self, mock_list):
        args = [
            "--name", "group-name",
            "--config", "config-1",
            "--status", "INSERVICE",
            "--offset", "10",
            "--limit", "20",
        ]
        verify_args = [
            ("name", "group-name"),
            ("config", "config-1"),
            ("status", "INSERVICE"),
            ("offset", 10),
            ("limit", 20),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_config_find as find_config:
            groups = [resource.AutoScalingGroup(None, c)
                      for c in self._groups]
            mock_list.return_value = br.ListWithMeta(groups, "Request-ID")
            columns, data = self.cmd.take_action(args)

            params = {
                'scaling_group_status': 'INSERVICE',
                'scaling_group_name': 'group-name',
                'scaling_configuration_id': self._config.id,
                'limit': 20,
                'start_number': 10
            }
            mock_list.assert_called_once_with("/scaling_group", params=params,
                                              key="scaling_groups")

            self.assertEquals(resource.AutoScalingGroup.list_column_names,
                              columns)
            expected = [('f5da912c-4525-4edf-b418-cc1c8e077298',
                         'Woo-Test-1',
                         '0/1/1/3',
                         '498c242b-54a4-48ec-afcd-bc21dd612b57',
                         'PAUSED'),
                        ('ac8acbb4-e6ce-4890-a9f2-d8712b3d7385',
                         'as-group-teo',
                         '2/2/0/4',
                         '498c242b-54a4-48ec-afcd-bc21dd612b57',
                         'INSERVICE'),
                        ('56e25174-c317-4be1-9fbd-17d5aff10ad5',
                         'as-group-lorc-Romania1',
                         '0/2/1/4',
                         None,
                         'PAUSED')]
            self.assertEquals(expected, data)


class TestShowAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestShowAutoScalingGroup, self).setUp()
        self.cmd = group.ShowAutoScalingGroup(self.app, None)

    def test_show_group(self):
        args = ["group-name", ]
        verify_args = [
            ("group", "group-name"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find as find:
            columns, data = self.cmd.take_action(args)
            find.assert_called_once_with(args.group)
            self.assertEquals(resource.AutoScalingGroup.show_column_names,
                              columns)
            expected = ('d4e50321-3777-4135-97f8-9f5e9714a4b0',
                        'api_gateway_modify',
                        '3e22f934-800d-4bb4-a588-0b9a76108190',
                        "id='2daf6ba6-fb24-424a-b5b8-c554fab95f15'",
                        "id='23b7b999-0a30-4b48-ae8f-ee201a88a6ab'",
                        '7/8/0/100',
                        '53579851-3841-418d-a97b-9cecdb663a90',
                        'press',
                        900,
                        None,
                        'NOVA_AUDIT',
                        60,
                        'OLD_CONFIG_OLD_INSTANCE',
                        True,
                        False,
                        '',
                        '2015-09-01T08:36:10Z',
                        'INSERVICE')
            self.assertEquals(expected, data)


@mock.patch.object(group_mgr.GroupManager, "_create")
class TestPauseAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestPauseAutoScalingGroup, self).setUp()
        self.cmd = group.PauseAutoScalingGroup(self.app, None)

    def test_pause_group(self, mock_create):
        args = ["group-name-1"]
        verify_args = [
            ("group", "group-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find as find:
            result = self.cmd.take_action(args)
            url = "/scaling_group/%s/action" % self._group.id
            find.assert_called_once_with(args.group)
            mock_create.assert_called_once_with(url,
                                                json=dict(action="pause"),
                                                raw=True)
            self.assertEquals('done', result)


@mock.patch.object(group_mgr.GroupManager, "_create")
class TestResumeAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestResumeAutoScalingGroup, self).setUp()
        self.cmd = group.ResumeAutoScalingGroup(self.app, None)

    def test_resume_group(self, mock_create):
        args = ["group-name-1"]
        verify_args = [
            ("group", "group-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find as find:
            result = self.cmd.take_action(args)
            url = "/scaling_group/%s/action" % self._group.id
            find.assert_called_once_with(args.group)
            mock_create.assert_called_once_with(url,
                                                json=dict(action="resume"),
                                                raw=True)
            self.assertEquals('done', result)


@mock.patch.object(group_mgr.GroupManager, "_delete")
class TestDeleteAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestDeleteAutoScalingGroup, self).setUp()
        self.cmd = group.DeleteAutoScalingGroup(self.app, None)

    def test_delete_group(self, mock_create):
        args = ["group-name-1"]
        verify_args = [
            ("group", "group-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        with self.mocked_group_find as find:
            result = self.cmd.take_action(args)
            find.assert_called_once_with(args.group)
            mock_create.assert_called_once_with(
                "/scaling_group/" + self._group.id
            )
            self.assertEquals('done', result)


class TestCreateAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestCreateAutoScalingGroup, self).setUp()
        self.cmd = group.CreateAutoScalingGroup(self.app, None)

    @mock.patch.object(group_mgr.GroupManager, "_create")
    def test_create_group(self, mock_create):
        args = [
            "new-group-name",
            "--vpc", "vpc-1",
            "--subnet", "subnet-1",
            "--subnet", "subnet-2",
            "--security-group", "sg-1",
            "--security-group", "sg-2",
            "--config", "config-1",
            "--desire-instance", "3",
            "--max-instance", "6",
            "--min-instance", "1",
            "--cool-down", "60",
            "--lb-listener", "lb-listener-1",
            "--health-periodic-audit-method", "ELB_AUDIT",
            "--health-periodic-audit-time", "5",
            "--instance-terminate-policy", "OLD_CONFIG_OLD_INSTANCE",
            "--delete-public-ip",
            "--available-zone", "eu-de-01",
            "--available-zone", "eu-de-02",
        ]

        verify_args = [
            ("name", "new-group-name"),
            ("vpc", "vpc-1"),
            ("subnets", ["subnet-1", "subnet-2"]),
            ("security_groups", ["sg-1", "sg-2"]),
            ("config", "config-1"),
            ("desire_instance", 3),
            ("max_instance", 6),
            ("min_instance", 1),
            ("cool_down", 60),
            ("lb_listener", "lb-listener-1"),
            ("health_periodic_audit_method", "ELB_AUDIT"),
            ("health_periodic_audit_time", 5),
            ("instance_terminate_policy", "OLD_CONFIG_OLD_INSTANCE"),
            ("delete_public_ip", True),
            ("available_zones", ["eu-de-01", "eu-de-02"]),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        network_client = self.app.client_manager.network

        _vpc = br.Resource(None, dict(id="vpc-id-1"))
        network_client.find_router.return_value = _vpc
        _sg_list = [br.Resource(None, dict(id="sg-id-01")),
                    br.Resource(None, dict(id="sg-id-02")), ]
        network_client.find_security_group.side_effect = _sg_list
        _subnets = [
            br.Resource(None, dict(network_id="subnet-id-1")),
            br.Resource(None, dict(network_id="subnet-id-2")),
        ]
        network_client.find_subnet.side_effect = _subnets

        with self.mocked_config_find:
            mock_create.return_value = self._group
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_name': 'new-group-name',
                'vpc_id': 'vpc-id-1',
                'security_groups': [{'id': 'sg-id-01'}, {'id': 'sg-id-02'}],
                'networks': [{'id': 'subnet-id-1'}, {'id': 'subnet-id-2'}],
                'scaling_configuration_id': self._config.id,
                'desire_instance_number': 3,
                'max_instance_number': 6,
                'min_instance_number': 1,
                'instance_terminate_policy': 'OLD_CONFIG_OLD_INSTANCE',
                'health_periodic_audit_method': 'ELB_AUDIT',
                'health_periodic_audit_time': 5,
                'lb_listener_id': 'lb-listener-1',
                'cool_down_time': 60,
                'delete_publicip': True,
                'available_zones': ["eu-de-01", "eu-de-02"],
            }
            mock_create.assert_called_once_with("/scaling_group", json=json)
            self.assertEquals("Group %s created" % self._group.id, result)


class TestEditAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestEditAutoScalingGroup, self).setUp()
        self.cmd = group.EditAutoScalingGroup(self.app, None)

    @mock.patch.object(group_mgr.GroupManager, "_update_all")
    def test_edit_group(self, mock_update):
        args = [
            "new-group-name",
            "--name", "changed-name",
            "--subnet", "subnet-1",
            "--subnet", "subnet-2",
            "--security-group", "sg-1",
            "--security-group", "sg-2",
            "--config", "config-1",
            "--desire-instance", "3",
            "--max-instance", "6",
            "--min-instance", "1",
            "--cool-down", "60",
            "--lb-listener", "lb-listener-1",
            "--health-periodic-audit-method", "ELB_AUDIT",
            "--health-periodic-audit-time", "5",
            "--instance-terminate-policy", "OLD_CONFIG_OLD_INSTANCE",
            "--delete-public-ip",
            "--available-zone", "eu-de-01",
            "--available-zone", "eu-de-02",
        ]

        verify_args = [
            ("group", "new-group-name"),
            ("name", "changed-name"),
            ("subnets", ["subnet-1", "subnet-2"]),
            ("security_groups", ["sg-1", "sg-2"]),
            ("config", "config-1"),
            ("desire_instance", 3),
            ("max_instance", 6),
            ("min_instance", 1),
            ("cool_down", 60),
            ("lb_listener", "lb-listener-1"),
            ("health_periodic_audit_method", "ELB_AUDIT"),
            ("health_periodic_audit_time", 5),
            ("instance_terminate_policy", "OLD_CONFIG_OLD_INSTANCE"),
            ("delete_public_ip", True),
            ("available_zones", ["eu-de-01", "eu-de-02"]),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        network_client = self.app.client_manager.network

        _vpc = br.Resource(None, dict(id="vpc-id-1"))
        network_client.find_router.return_value = _vpc
        _sg_list = [br.Resource(None, dict(id="sg-id-01")),
                    br.Resource(None, dict(id="sg-id-02")), ]
        network_client.find_security_group.side_effect = _sg_list
        _subnets = [
            br.Resource(None, dict(network_id="subnet-id-1")),
            br.Resource(None, dict(network_id="subnet-id-2")),
        ]
        network_client.find_subnet.side_effect = _subnets
        with self.mocked_config_find, self.mocked_group_find:
            mock_update.return_value = self._group
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_name': 'changed-name',
                'security_groups': [{'id': 'sg-id-01'}, {'id': 'sg-id-02'}],
                'networks': [{'id': 'subnet-id-1'}, {'id': 'subnet-id-2'}],
                'scaling_configuration_id': self._config.id,
                'desire_instance_number': 3,
                'max_instance_number': 6,
                'min_instance_number': 1,
                'instance_terminate_policy': 'OLD_CONFIG_OLD_INSTANCE',
                'health_periodic_audit_method': 'ELB_AUDIT',
                'health_periodic_audit_time': 5,
                'lb_listener_id': 'lb-listener-1',
                'cool_down_time': 60,
                'delete_publicip': True,
                'available_zones': ["eu-de-01", "eu-de-02"],
            }
            mock_update.assert_called_once_with(
                "/scaling_group/" + self._group.id, json=json)
            self.assertEquals("Group %s modified" % self._group.id, result)


class TestFindAutoScalingGroup(AutoScalingGroupV1BaseTestCase):
    def setUp(self):
        super(TestFindAutoScalingGroup, self).setUp()

    @mock.patch.object(group_mgr.GroupManager, "_get")
    def test_find_group_with_id(self, mocked):
        groups = self.app.client_manager.auto_scaling.groups
        get_return = self._group
        mocked.return_value = get_return
        find = groups.find("group-id-1")
        mocked.assert_called_once_with("/scaling_group/group-id-1",
                                       key='scaling_group')
        self.assertEquals(get_return, find)

    @mock.patch.object(group_mgr.GroupManager, "_list")
    @mock.patch.object(group_mgr.GroupManager, "_get")
    def test_find_group_with_name(self, mocked_get, mock_list):
        groups = self.app.client_manager.auto_scaling.groups
        mocked_get.side_effect = exceptions.ClientException(0)

        _list = [resource.AutoScalingGroup(None, g) for g in self._groups]
        mock_list.return_value = br.ListWithMeta(_list, None)
        find = groups.find("Woo-Test-1")
        params = dict(scaling_group_name="Woo-Test-1")
        mock_list.assert_called_once_with("/scaling_group",
                                          key="scaling_groups",
                                          params=params)
        self.assertEquals(_list[0], find)

    @mock.patch.object(group_mgr.GroupManager, "_list")
    @mock.patch.object(group_mgr.GroupManager, "_get")
    def test_find_group_with_name_no_match(self, mocked_get, mock_list):
        groups = self.app.client_manager.auto_scaling.groups
        mocked_get.side_effect = exceptions.ClientException(0)
        mock_list.return_value = br.ListWithMeta([], None)
        self.assertRaises(exceptions.NotFound, groups.find, "group-name-1")
