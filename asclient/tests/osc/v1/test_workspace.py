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
import mock

from asclient.common import resource as base_resource
from asclient.osc.v1 import workspace
from asclient.tests import base
from asclient.v1 import resource
from asclient.v1 import workspace_mgr


class TestWorkspaceEnable(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestWorkspaceEnable, self).setUp()
        self.cmd = workspace.EnableWorkspace(self.app, None)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_create")
    def test_enable_lite_ad_workspace(self, mocked_create):
        args = [
            "--domain-type", "LITE_AD",
            "--domain-name", "test.com",
            "--domain-admin-account", "test",
            "--domain-password", "Test!@#$22",
            "--vpc", "vpc-name",
            "--subnet", "subnet-name-01",
            "--subnet", "subnet-name-02",
            "--access-mode", "INTERNET",
        ]
        verify_args = [
            ("domain_type", "LITE_AD"),
            ("domain_name", "test.com"),
            ("domain_admin_account", "test"),
            ("domain_password", "Test!@#$22"),
            ("vpc", "vpc-name"),
            ("subnets", ["subnet-name-01", "subnet-name-02", ]),
            ("access_mode", "INTERNET"),
        ]
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        # mock return values
        _network = base_resource.Resource(None, dict(id="network-id"))
        self.app.client_manager.network.find_network.return_value = _network
        _subnets = [base_resource.Resource(None, dict(id="subnet-id-1")),
                    base_resource.Resource(None, dict(id="subnet-id-2"))]
        self.app.client_manager.network.find_subnet.side_effect = _subnets
        _job = base_resource.DictWithMeta(dict(job_id="job_id"), 'RID')
        mocked_create.return_value = _job

        # take cmd
        result = self.cmd.take_action(parsed_args)

        json = {
            "ad_domains": {
                "domain_type": "LITE_AD",
                "domain_name": "test.com",
                "domain_admin_account": "test",
                "domain_password": "Test!@#$22"
            },
            "vpc_id": "network-id",
            "subnet_ids": [{
                "subnet_id": "subnet-id-1"
            }, {
                "subnet_id": "subnet-id-2"
            }],
            "access_mode": "INTERNET"
        }

        mocked_create.assert_called_once_with(
            "/workspaces", json=json, raw=True
        )
        self.assertEqual("Request Received, job id: %s" % _job["job_id"],
                         result)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_create")
    def test_enable_local_ad_workspace(self, mocked_create):
        args = [
            "--domain-type", "LOCAL_AD",
            "--domain-name", "test.com",
            "--domain-admin-account", "test",
            "--domain-password", "Test!@#$22",
            "--active-domain-ip", "1.1.1.1",
            "--standby-domain-ip", "1.1.1.1",
            "--active-dns-ip", "1.1.1.1",
            "--standby-dns-ip", "1.1.1.1",
            "--vpc", "vpc-name",
            "--subnet", "subnet-name-01",
            "--subnet", "subnet-name-02",
            "--access-mode", "INTERNET",
        ]
        verify_args = [
            ("domain_type", "LOCAL_AD"),
            ("domain_name", "test.com"),
            ("domain_admin_account", "test"),
            ("domain_password", "Test!@#$22"),
            ("active_domain_ip", "1.1.1.1"),
            ("active_dns_ip", "1.1.1.1"),
            ("standby_domain_ip", "1.1.1.1"),
            ("standby_dns_ip", "1.1.1.1"),
            ("vpc", "vpc-name"),
            ("subnets", ["subnet-name-01", "subnet-name-02", ]),
            ("access_mode", "INTERNET"),
        ]
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        # mock return values
        _network = base_resource.Resource(None, dict(id="network-id"))
        self.app.client_manager.network.find_network.return_value = _network
        _subnets = [base_resource.Resource(None, dict(id="subnet-id-1")),
                    base_resource.Resource(None, dict(id="subnet-id-2"))]
        self.app.client_manager.network.find_subnet.side_effect = _subnets
        _job = base_resource.DictWithMeta(dict(job_id="job_id"), 'RID')
        mocked_create.return_value = _job

        # take cmd
        result = self.cmd.take_action(parsed_args)

        json = {
            "ad_domains": {
                "domain_type": "LOCAL_AD",
                "domain_name": "test.com",
                "domain_admin_account": "test",
                "domain_password": "Test!@#$22",
                "active_domain_ip": "1.1.1.1",
                "active_dns_ip": "1.1.1.1",
                "standby_domain_ip": "1.1.1.1",
                "standby_dns_ip": "1.1.1.1",
            },
            "vpc_id": "network-id",
            "subnet_ids": [{
                "subnet_id": "subnet-id-1"
            }, {
                "subnet_id": "subnet-id-2"
            }],
            "access_mode": "INTERNET"
        }

        mocked_create.assert_called_once_with(
            "/workspaces", json=json, raw=True
        )
        self.assertEqual("Request Received, job id: %s" % _job["job_id"],
                         result)


class TestWorkspaceDisable(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestWorkspaceDisable, self).setUp()
        self.cmd = workspace.DisableWorkspace(self.app, None)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_delete")
    def test_disable_workspace(self, mocked):
        parsed_args = self.check_parser(self.cmd, [], ())
        _job = base_resource.DictWithMeta(dict(job_id="job_id"), 'RID')
        mocked.return_value = _job
        result = self.cmd.take_action(parsed_args)
        mocked.assert_called_once_with("/workspaces")
        self.assertEquals("Request Received, job id: " + _job["job_id"],
                          result)


class TestWorkspaceEdit(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestWorkspaceEdit, self).setUp()
        self.cmd = workspace.EditWorkspace(self.app, None)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_update_all")
    def test_edit_lite_ad_workspace(self, mocked):
        args = [
            "--domain-type", "LITE_AD",
            "--domain-password", "p1",
            "--old-domain-password", "p2",
        ]
        verify_args = (
            ("domain_type", "LITE_AD"),
            ("domain_password", "p1"),
            ("old_domain_password", "p2"),
        )
        parsed_args = self.check_parser(self.cmd, args, verify_args)
        mocked.return_value = base_resource.StrWithMeta('', 'Request-ID')
        result = self.cmd.take_action(parsed_args)

        json = {
            "ad_domains": {
                "domain_type": "LITE_AD",
                "old_domain_password": "p2",
                "domain_password": "p1"
            }
        }
        mocked.assert_called_once_with("/workspaces", json=json, raw=True)
        self.assertEquals("done", result)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_update_all")
    def test_edit_local_ad_workspace(self, mocked):
        args = [
            "--domain-type", "LITE_AD",
            "--domain-admin-account", "account",
            "--domain-password", "p1",
        ]
        verify_args = (
            ("domain_type", "LITE_AD"),
            ("domain_password", "p1"),
            ("domain_admin_account", "account"),
        )
        parsed_args = self.check_parser(self.cmd, args, verify_args)
        mocked.return_value = base_resource.StrWithMeta('', 'Request-ID')
        result = self.cmd.take_action(parsed_args)

        json = {
            "ad_domains": {
                "domain_type": "LITE_AD",
                "domain_admin_account": "account",
                "domain_password": "p1"
            }
        }
        mocked.assert_called_once_with("/workspaces", json=json, raw=True)
        self.assertEquals("done", result)


class TestWorkspaceShow(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestWorkspaceShow, self).setUp()
        self.cmd = workspace.ShowWorkspace(self.app, None)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_get")
    def test_show_lite_ad_workspace(self, mocked):
        parsed_args = self.check_parser(self.cmd, [], ())
        return_data = {
            "ad_domains": {
                "domain_type": "LITE_AD",
                "domain_name": "test.com",
                "domain_admin_account": "vdsadmin",
                "active_domain_ip": None,
                "standby_domain_ip": None,
                "active_dns_ip": None,
                "standby_dns_ip": None
            },
            "vpc_id": "dbecb512-34d1-4d7d-90f1-6d3feb76263d",
            "vpc_name": "test",
            "dedicated_access_address": "https://192.168.0.4",
            "internet_access_address": "https://10.154.55.185",
            "status": "SUBSCRIBED",
            "access_mode": "DEDICATED",
            "subnet_ids": [
                {
                    "subnet_id": "a4bde8e5-b8b7-453c-839b-3c5a3a49772f"
                }
            ]
        }
        mocked.return_value = resource.Workspace(None, return_data)
        columns, data = self.cmd.take_action(parsed_args)
        mocked.assert_called_once_with("/workspaces")
        self.assertEquals(resource.Workspace.show_column_names, columns)
        expected = (
            "active_dns_ip='None', active_domain_ip='None', "
            "domain_admin_account='vdsadmin', domain_name='test.com', "
            "domain_type='LITE_AD', standby_dns_ip='None', "
            "standby_domain_ip='None'",
            'dbecb512-34d1-4d7d-90f1-6d3feb76263d',
            'test',
            'https://192.168.0.4',
            'https://10.154.55.185',
            'DEDICATED',
            "subnet_id='a4bde8e5-b8b7-453c-839b-3c5a3a49772f'"
        )
        self.assertEquals(expected, data)

    @mock.patch.object(workspace_mgr.WorkspaceManager, "_get")
    def test_show_lite_ad_workspace(self, mocked):
        parsed_args = self.check_parser(self.cmd, [], ())
        return_data = {
            "ad_domains": {
                "domain_type": "LOCAL_AD",
                "domain_name": "test.com",
                "domain_admin_account": "vdsadmin",
                "active_domain_ip": "172.16.0.4",
                "standby_domain_ip": "172.16.0.5",
                "active_dns_ip": "172.16.0.4",
                "standby_dns_ip": "172.16.0.5"
            },
            "vpc_id": "dbecb512-34d1-4d7d-90f1-6d3feb76263d",
            "vpc_name": "test",
            "dedicated_access_address": "null",
            "internet_access_address": "https://10.154.55.185",
            "status": "SUBSCRIBED",
            "access_mode": "INTERNET",
            "subnet_ids": [
                {
                    "subnet_id": "a4bde8e5-b8b7-453c-839b-3c5a3a49772f"
                }
            ]
        }

        mocked.return_value = resource.Workspace(None, return_data)
        columns, data = self.cmd.take_action(parsed_args)
        mocked.assert_called_once_with("/workspaces")
        self.assertEquals(resource.Workspace.show_column_names, columns)
        expected = (
            "active_dns_ip='172.16.0.4', active_domain_ip='172.16.0.4', "
            "domain_admin_account='vdsadmin', domain_name='test.com', "
            "domain_type='LOCAL_AD', standby_dns_ip='172.16.0.5', "
            "standby_domain_ip='172.16.0.5'",
            'dbecb512-34d1-4d7d-90f1-6d3feb76263d',
            'test',
            'null',
            'https://10.154.55.185',
            'INTERNET',
            "subnet_id='a4bde8e5-b8b7-453c-839b-3c5a3a49772f'"
        )
        self.assertEquals(expected, data)
