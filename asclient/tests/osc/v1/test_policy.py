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
from keystoneclient import exceptions

from asclient.common import resource as br
from asclient.osc.v1 import policy
from asclient.tests import base
from asclient.v1 import policy_mgr
from asclient.v1 import resource


class AutoScalingPolicyV1BaseTestCase(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(AutoScalingPolicyV1BaseTestCase, self).__init__(*args, **kwargs)
        self._policies = [
            {"scaling_policy_id": "67174f3d-0a7a-4c13-a890-edbe11b45242",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_policy_name": "as-policy-rpdj",
             "scaling_policy_type": "ALARM",
             "alarm_id": "al1480513400538j1dVGjE04", "scheduled_policy": {},
             "cool_down_time": 900,
             "scaling_policy_action": {"operation": "ADD",
                                       "instance_number": 1},
             "policy_status": "INSERVICE",
             "create_time": "2016-11-30T13:43:20Z"},
            {"scaling_policy_id": "81c5051a-cb1d-4993-b036-3d3afc6c9648",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_policy_name": "as-policy-tfum",
             "scaling_policy_type": "SCHEDULED",
             "scheduled_policy": {"launch_time": "2016-12-24T13:44Z"},
             "cool_down_time": 900,
             "scaling_policy_action": {"operation": "ADD",
                                       "instance_number": 4},
             "policy_status": "PAUSED", "create_time": "2016-11-30T13:44:21Z"},
            {"scaling_policy_id": "c8e2c794-f8ef-428a-8efe-3ff1268f6804",
             "scaling_group_id": "ac8acbb4-e6ce-4890-a9f2-d8712b3d7385",
             "scaling_policy_name": "WooTest",
             "scaling_policy_type": "SCHEDULED",
             "scheduled_policy": {"launch_time": "2017-02-19T13:40Z"},
             "cool_down_time": 900,
             "scaling_policy_action": {"operation": "ADD",
                                       "instance_number": 1},
             "policy_status": "INSERVICE",
             "create_time": "2017-02-19T13:38:00Z"}]


@mock.patch.object(policy_mgr.PolicyManager, "_list")
class TestListAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestListAutoScalingPolicy, self).setUp()
        self.cmd = policy.ListAutoScalingPolicy(self.app, None)

    def test_list_policy(self, mock_list):
        args = [
            "--group", "group-name",
            "--name", "policy-name",
            "--type", "ALARM",
            "--offset", "10",
            "--limit", "20",
        ]
        verify_args = [
            ("group", "group-name"),
            ("name", "policy-name"),
            ("type", "ALARM"),
            ("offset", 10),
            ("limit", 20),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find as find_group:
            policies = [resource.AutoScalingPolicy(None, c)
                        for c in self._policies]
            mock_list.return_value = br.ListWithMeta(policies, "Request-ID")
            columns, data = self.cmd.take_action(args)

            url = "/scaling_policy/%s/list" % self._group.id
            params = {
                "scaling_policy_name": "policy-name",
                "scaling_policy_type": "ALARM",
                "start_number": 10,
                "limit": 20,
            }
            mock_list.assert_called_once_with(url, params=params,
                                              key="scaling_policies")

            self.assertEquals(resource.AutoScalingPolicy.list_column_names,
                              columns)
            expected = [('67174f3d-0a7a-4c13-a890-edbe11b45242',
                         'as-policy-rpdj',
                         'ALARM',
                         900,
                         'ADD 1',
                         'INSERVICE'),
                        ('81c5051a-cb1d-4993-b036-3d3afc6c9648',
                         'as-policy-tfum',
                         'SCHEDULED',
                         900,
                         'ADD 4',
                         'PAUSED'),
                        ('c8e2c794-f8ef-428a-8efe-3ff1268f6804',
                         'WooTest',
                         'SCHEDULED',
                         900,
                         'ADD 1',
                         'INSERVICE')]
            self.assertEquals(expected, data)


class TestShowAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestShowAutoScalingPolicy, self).setUp()
        self.cmd = policy.ShowAutoScalingPolicy(self.app, None)

    def test_show_policy(self):
        args = ["policy-name", ]
        verify_args = [
            ("policy", "policy-name"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_policy_find as find:
            columns, data = self.cmd.take_action(args)
            find.assert_called_once_with(args.policy)
            self.assertEquals(resource.AutoScalingPolicy.show_column_names,
                              columns)
            expected = ('e5d27f5c-dd76-4a61-b4bc-a67c5686719a',
                        'fd7d63ce-8f5c-443e-b9a0-bef9386b23b3',
                        'fix-time-1',
                        'SCHEDULED',
                        '',
                        300,
                        "launch_time='2015-07-24T01:21Z'",
                        'REMOVE 1',
                        '2015-07-24T01:09:30Z',
                        'INSERVICE')
            self.assertEquals(expected, data)


@mock.patch.object(policy_mgr.PolicyManager, "_create")
class TestExecuteAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestExecuteAutoScalingPolicy, self).setUp()
        self.cmd = policy.ExecuteAutoScalingPolicy(self.app, None)

    def test_execute_policy(self, mock_create):
        args = ["policy-name-1"]
        verify_args = [
            ("policy", "policy-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_policy_find as find:
            result = self.cmd.take_action(args)
            url = "/scaling_policy/%s/action" % self._policy.id
            find.assert_called_once_with(args.policy)
            mock_create.assert_called_once_with(url,
                                                json=dict(action="execute"),
                                                raw=True)
            self.assertEquals('done', result)


@mock.patch.object(policy_mgr.PolicyManager, "_create")
class TestPauseAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestPauseAutoScalingPolicy, self).setUp()
        self.cmd = policy.PauseAutoScalingPolicy(self.app, None)

    def test_pause_policy(self, mock_create):
        args = ["policy-name-1"]
        verify_args = [
            ("policy", "policy-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_policy_find as find:
            result = self.cmd.take_action(args)
            url = "/scaling_policy/%s/action" % self._policy.id
            find.assert_called_once_with(args.policy)
            mock_create.assert_called_once_with(url,
                                                json=dict(action="pause"),
                                                raw=True)
            self.assertEquals('done', result)


@mock.patch.object(policy_mgr.PolicyManager, "_create")
class TestResumeAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestResumeAutoScalingPolicy, self).setUp()
        self.cmd = policy.ResumeAutoScalingPolicy(self.app, None)

    def test_resume_policy(self, mock_create):
        args = ["policy-name-1"]
        verify_args = [
            ("policy", "policy-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_policy_find as find:
            result = self.cmd.take_action(args)
            url = "/scaling_policy/%s/action" % self._policy.id
            find.assert_called_once_with(args.policy)
            mock_create.assert_called_once_with(url,
                                                json=dict(action="resume"),
                                                raw=True)
            self.assertEquals('done', result)


@mock.patch.object(policy_mgr.PolicyManager, "_delete")
class TestDeleteAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestDeleteAutoScalingPolicy, self).setUp()
        self.cmd = policy.DeleteAutoScalingPolicy(self.app, None)

    def test_delete_policy(self, mock_create):
        args = ["policy-name-1"]
        verify_args = [
            ("policy", "policy-name-1"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        with self.mocked_policy_find as find:
            result = self.cmd.take_action(args)
            find.assert_called_once_with(args.policy)
            mock_create.assert_called_once_with(
                "/scaling_policy/" + self._policy.id)
            self.assertEquals('done', result)


class TestCreateAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestCreateAutoScalingPolicy, self).setUp()
        self.cmd = policy.CreateAutoScalingPolicy(self.app, None)

    @mock.patch.object(policy_mgr.PolicyManager, "_create")
    def test_create_alarm_policy(self, mock_create):
        args = [
            "new-policy-name",
            "--group", "group-1",
            "--type", "ALARM",
            "--cool-down", "300",
            "--alarm-id", "alarm-id",
            "--action", "ADD:1",
        ]
        verify_args = [
            ("name", "new-policy-name"),
            ("group", "group-1"),
            ("type", "ALARM"),
            ("cool_down", 300),
            ("alarm_id", "alarm-id"),
            ("action", {'instance_number': 1, 'operation': 'ADD'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find:
            mock_create.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_id': self._group.id,
                'alarm_id': 'alarm-id',
                'scaling_policy_type': 'ALARM',
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'ADD'
                },
                'scaling_policy_name': 'new-policy-name',
                'cool_down_time': 300
            }
            mock_create.assert_called_once_with("/scaling_policy", json=json)
            self.assertEquals("Policy %s created" % self._policy.id, result)

    @mock.patch.object(policy_mgr.PolicyManager, "_create")
    def test_create_schedule_policy(self, mock_create):
        args = [
            "new-policy-name",
            "--group", "group-1",
            "--type", "SCHEDULED",
            "--launch-time", "2017-02-20T10:00",
            "--cool-down", "300",
            "--action", "ADD:1",
        ]
        verify_args = [
            ("name", "new-policy-name"),
            ("group", "group-1"),
            ("type", "SCHEDULED"),
            ("launch_time", datetime.datetime(2017, 2, 20, hour=10)),
            ("cool_down", 300),
            ("action", {'instance_number': 1, 'operation': 'ADD'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find:
            mock_create.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_id': self._group.id,
                'scheduled_policy': {
                    'launch_time': '2017-02-20T10:00Z'
                },
                'scaling_policy_type': 'SCHEDULED',
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'ADD'
                },
                'scaling_policy_name': 'new-policy-name',
                'cool_down_time': 300
            }
            mock_create.assert_called_once_with("/scaling_policy", json=json)
            self.assertEquals("Policy %s created" % self._policy.id, result)

    @mock.patch.object(policy_mgr.PolicyManager, "_create")
    def test_create_daily_recurrence_policy(self, mock_create):
        args = [
            "new-policy-name",
            "--group", "group-1",
            "--type", "RECURRENCE",
            "--recurrence", "Weekly:1,5,7",
            "--start-time", "2017-02-20T10:00",
            "--end-time", "2017-03-20T10:00",
            "--cool-down", "300",
            "--action", "REMOVE:1",
        ]
        verify_args = [
            ("name", "new-policy-name"),
            ("group", "group-1"),
            ("type", "RECURRENCE"),
            ("recurrence", {"recurrence_type": "Weekly",
                            "recurrence_value": "1,5,7"}),
            ("start_time", datetime.datetime(2017, 2, 20, hour=10)),
            ("end_time", datetime.datetime(2017, 3, 20, hour=10)),
            ("cool_down", 300),
            ("action", {'instance_number': 1, 'operation': 'REMOVE'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find:
            mock_create.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_id': self._group.id,
                'scheduled_policy': {
                    'start_time': '2017-02-20T10:00Z',
                    'end_time': '2017-03-20T10:00Z',
                    'recurrence_type': 'Weekly',
                    'recurrence_value': '1,5,7',
                },
                'scaling_policy_type': 'RECURRENCE',
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'REMOVE'
                },
                'scaling_policy_name': 'new-policy-name',
                'cool_down_time': 300
            }
            mock_create.assert_called_once_with("/scaling_policy", json=json)
            self.assertEquals("Policy %s created" % self._policy.id, result)

    @mock.patch.object(policy_mgr.PolicyManager, "_create")
    def test_create_weekly_recurrence_policy(self, mock_create):
        args = [
            "new-policy-name",
            "--group", "group-1",
            "--type", "RECURRENCE",
            "--recurrence", "Daily:10:00",
            "--start-time", "2017-02-20T10:00",
            "--end-time", "2017-03-20T10:00",
            "--cool-down", "300",
            "--action", "SET:1",
        ]
        verify_args = [
            ("name", "new-policy-name"),
            ("group", "group-1"),
            ("type", "RECURRENCE"),
            ("recurrence", {"recurrence_type": "Daily",
                            "recurrence_value": "10:00"}),
            ("start_time", datetime.datetime(2017, 2, 20, hour=10)),
            ("end_time", datetime.datetime(2017, 3, 20, hour=10)),
            ("cool_down", 300),
            ("action", {'instance_number': 1, 'operation': 'SET'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_group_find:
            mock_create.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'scaling_group_id': self._group.id,
                'scheduled_policy': {
                    'launch_time': '10:00',
                    'start_time': '2017-02-20T10:00Z',
                    'end_time': '2017-03-20T10:00Z',
                    'recurrence_type': 'Daily',
                },
                'scaling_policy_type': 'RECURRENCE',
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'SET'
                },
                'scaling_policy_name': 'new-policy-name',
                'cool_down_time': 300
            }
            mock_create.assert_called_once_with("/scaling_policy", json=json)
            self.assertEquals("Policy %s created" % self._policy.id, result)


class TestEditAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestEditAutoScalingPolicy, self).setUp()
        self.cmd = policy.EditAutoScalingPolicy(self.app, None)

    @mock.patch.object(policy_mgr.PolicyManager, "_update_all")
    def test_edit_alarm_policy(self, mock_update):
        # pb.Policy.add_launch_time_opt(parser)
        # pb.Policy.add_recurrence_opt(parser)
        # pb.Policy.add_start_time_opt(parser)
        # pb.Policy.add_end_time_opt(parser)
        # pb.Policy.add_action_opt(parser)
        args = [
            "new-policy-name",
            "--name", "changed-name",
            "--type", "ALARM",
            "--cool-down", "300",
            "--alarm-id", "alarm-id",
            "--action", "ADD:1",
        ]
        verify_args = [
            ("policy", "new-policy-name"),
            ("name", "changed-name"),
            ("type", "ALARM"),
            ("cool_down", 300),
            ("alarm_id", "alarm-id"),
            ("action", {'instance_number': 1, 'operation': 'ADD'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        with self.mocked_policy_find:
            mock_update.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'alarm_id': 'alarm-id',
                'scaling_policy_type': 'ALARM',
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'ADD'
                },
                'scaling_policy_name': 'changed-name',
                'cool_down_time': 300
            }
            mock_update.assert_called_once_with(
                "/scaling_policy/" + self._policy.id, json=json
            )
            self.assertEquals("done", result)

    @mock.patch.object(policy_mgr.PolicyManager, "_update_all")
    def test_edit_recurrence_policy(self, mock_update):
        args = [
            "new-policy-name",
            "--name", "changed-name",
            "--type", "RECURRENCE",
            "--recurrence", "Daily:10:00",
            "--start-time", "2017-02-20T10:00",
            "--end-time", "2017-03-20T10:00",
            "--cool-down", "300",
            "--action", "ADD:1",
        ]
        verify_args = [
            ("policy", "new-policy-name"),
            ("name", "changed-name"),
            ("type", "RECURRENCE"),
            ("recurrence", {"recurrence_type": "Daily",
                            "recurrence_value": "10:00"}),
            ("start_time", datetime.datetime(2017, 2, 20, hour=10)),
            ("end_time", datetime.datetime(2017, 3, 20, hour=10)),
            ("cool_down", 300),
            ("action", {'instance_number': 1, 'operation': 'ADD'}),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        with self.mocked_policy_find:
            mock_update.return_value = self._policy
            result = self.cmd.take_action(args)
            json = {
                'scaling_policy_type': 'RECURRENCE',
                'scheduled_policy': {
                    'start_time': '2017-02-20T10:00Z',
                    'launch_time': '10:00',
                    'end_time': '2017-03-20T10:00Z',
                    'recurrence_type': 'Daily'
                },
                'scaling_policy_action': {
                    'instance_number': 1,
                    'operation': 'ADD'
                },
                'scaling_policy_name': 'changed-name',
                'cool_down_time': 300
            }
            mock_update.assert_called_once_with(
                "/scaling_policy/" + self._policy.id, json=json
            )
            self.assertEquals("done", result)


class TestFindAutoScalingPolicy(AutoScalingPolicyV1BaseTestCase):
    def setUp(self):
        super(TestFindAutoScalingPolicy, self).setUp()

    @mock.patch.object(policy_mgr.PolicyManager, "_get")
    def test_find_policy_with_id(self, mocked):
        policies = self.app.client_manager.auto_scaling.policies
        get_return = self._policy
        mocked.return_value = get_return
        find = policies.find("policy-id-1")
        mocked.assert_called_once_with("/scaling_policy/policy-id-1",
                                       key='scaling_policy')
        self.assertEquals(get_return, find)

    @mock.patch.object(policy_mgr.PolicyManager, "_get")
    def test_find_policy_with_name_no_match(self, mocked_get):
        policies = self.app.client_manager.auto_scaling.policies
        mocked_get.side_effect = exceptions.ClientException(0)
        self.assertRaises(exceptions.NotFound, policies.find, "policy_name_1")
