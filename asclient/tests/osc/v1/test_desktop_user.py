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
import datetime

import mock
from asclient.osc.v1 import desktop_user
from asclient.tests import base
from asclient.v1 import desktop_user_mgr
from asclient.v1 import resource


class TestDesktopUserList(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestDesktopUserList, self).setUp()
        self.cmd = desktop_user.ListDesktopUser(self.app, None)

    @mock.patch.object(desktop_user_mgr.DesktopUserManager, "_list")
    def test_desktop_user_list(self, mocked_list):
        users = [
            {
                "user_name": "a01",
                "user_email": "nuzngyng@test.com",
                "ad_domains": {
                    "domain_name": "abc.com",
                    "domain_type": "LITE_AD"
                }
            },
            {
                "user_name": "a02",
                "user_email": "nuzogyag@test.com",
                "ad_domains": {
                    "domain_name": "abc.com",
                    "domain_type": "LITE_AD"
                }
            }
        ]

        args = [
            "--user-name", "user-name",
            "--user-email", "test@test.com",
            "--marker", "user-id-1",
            "--limit", "10",
        ]

        verify_args = (
            ("user_name", "user-name"),
            ("user_email", "test@test.com"),
            ("marker", "user-id-1"),
            ("limit", 10),
        )
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        mocked_list.return_value = [resource.DesktopUser(None, u)
                                    for u in users]
        columns, data = self.cmd.take_action(parsed_args)

        params = {
            'marker': 'user-id-1',
            'user_name': 'user-name',
            'limit': 10,
            'user_email': 'test@test.com'
        }
        mocked_list.assert_called_once_with("/desktop-users", key='users',
                                            params=params, )
        self.assertEquals(resource.DesktopUser.list_column_names, columns)
        expected = [
            ("a01", "nuzngyng@test.com", "abc.com", "LITE_AD"),
            ("a02", "nuzogyag@test.com", "abc.com", "LITE_AD"),
        ]
        self.assertEquals(expected, data)


class TestLoginRecordList(base.WorkspaceV1BaseTestCase):
    def setUp(self):
        super(TestLoginRecordList, self).setUp()
        self.cmd = desktop_user.ListLoginRecords(self.app, None)

    @mock.patch.object(desktop_user_mgr.DesktopUserManager, "_list")
    def test_login_record_list(self, mocked_list):
        records = [
            {
                "computer_name": "a0504@abc.com",
                "user_name": "a05@abc.com",
                "terminal_mac": "28-6e-d4-f8-cb-1b",
                "terminal_name": "TEST01D02",
                "terminal_ip": "10.75.229.214",
                "client_version": "1.6.00004",
                "terminal_type": "Windows 10 ",
                "agent_version": "1.6.00005.0",
                "desktop_ip": "172.16.0.20",
                "connection_start_time": "2016-12-09T07:28:07.000Z",
                "connection_setup_time": "2016-12-09T07:28:17.000Z",
                "connection_end_time": "2016-12-09T08:29:37.000Z",
                "is_reconnect": False,
                "connection_failure_reason": None
            },
            {
                "computer_name": "a0505@abc.com",
                "user_name": "a05@abc.com",
                "terminal_mac": "28-6e-d4-f8-cb-1b",
                "terminal_name": "TEST01D02",
                "terminal_ip": "10.75.229.214",
                "client_version": "1.6.00004",
                "terminal_type": "Windows 10 ",
                "agent_version": "1.6.00005.0",
                "desktop_ip": None,
                "connection_start_time": "2016-12-09T06:56:21.000Z",
                "connection_setup_time": None,
                "connection_end_time": None,
                "is_reconnect": False,
                "connection_failure_reason":
                    "400200:The desktop is being prepared."
            }
        ]

        args = [
            "--start-time", "2017-02-14 18:00",
            "--end-time", "2017-02-14 19:00",
            "--user-name", "user-name",
            "--computer-name", "computer-name",
            "--terminal-type", "Windows 7",
            "--offset", "10",
            "--limit", "10",
        ]

        verify_args = (
            ("start_time", datetime.datetime(2017, 2, 14, hour=18, minute=0)),
            ("end_time", datetime.datetime(2017, 2, 14, hour=19, minute=0)),
            ("user_name", "user-name"),
            ("computer_name", "computer-name"),
            ("terminal_type", "Windows 7"),
            ("offset", 10),
            ("limit", 10),
        )
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        mocked_list.return_value = [resource.DesktopLoginRecords(None, r)
                                    for r in records]
        columns, data = self.cmd.take_action(parsed_args)

        params = {
            "start_time": "2017-02-14T18:00Z",
            "end_time": "2017-02-14T19:00Z",
            "user_name": "user-name",
            "computer_name": "computer-name",
            "terminal_type": "Windows 7",
            "offset": 10,
            "limit": 10,
        }
        mocked_list.assert_called_once_with(
            "/desktop-users/login-records", key='records', params=params,
            resource_class=resource.DesktopLoginRecords
        )
        self.assertEquals(resource.DesktopLoginRecords.list_column_names,
                          columns)
        expected = [
            ("a0504@abc.com", "a05@abc.com", "TEST01D02", "Windows 10 ",
             "2016-12-09T07:28:07.000Z", "2016-12-09T08:29:37.000Z",),
            ("a0505@abc.com", "a05@abc.com", "TEST01D02", "Windows 10 ",
             "2016-12-09T06:56:21.000Z", None,),
        ]
        self.assertEquals(expected, data)
