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
from asclient.tests import fakes
from asclient.v1 import config_mgr
from asclient.v1 import group_mgr
from asclient.v1 import resource
from osc_lib.tests import utils


class BaseTestCase(utils.TestCommand):
    """Base Test case class for all unit tests."""
    pass


class AutoScalingV1BaseTestCase(BaseTestCase):
    """Base test case class for Workspace V1 management API."""

    def __init__(self, *args, **kwargs):
        super(AutoScalingV1BaseTestCase, self).__init__(*args, **kwargs)
        self.cmd = None
        self.mocked_group_find = None
        self.mocked_config_find = None
        self._group = resource.AutoScalingGroup(None, {
            "networks": [
                {
                    "id": "2daf6ba6-fb24-424a-b5b8-c554fab95f15"
                }
            ],
            "detail": None,
            "scaling_group_name": "api_gateway_modify",
            "scaling_group_id": "d4e50321-3777-4135-97f8-9f5e9714a4b0",
            "scaling_group_status": "INSERVICE",
            "scaling_configuration_id": "53579851-3841-418d-a97b-9cecdb663a90",
            "scaling_configuration_name": "press",
            "current_instance_number": 7,
            "desire_instance_number": 8,
            "min_instance_number": 0,
            "max_instance_number": 100,
            "cool_down_time": 900,
            "lb_listener_id": None,
            "security_groups": [
                {
                    "id": "23b7b999-0a30-4b48-ae8f-ee201a88a6ab"
                }
            ],
            "create_time": "2015-09-01T08:36:10Z",
            "vpc_id": "3e22f934-800d-4bb4-a588-0b9a76108190",
            "health_periodic_audit_method": "NOVA_AUDIT",
            "health_periodic_audit_time": 60,
            "instance_terminate_policy": "OLD_CONFIG_OLD_INSTANCE",
            "is_scaling": True,
            "delete_publicip": False,
            "notifications": [
                "EMAIL"
            ]
        })

        self._config = resource.AutoScalingConfig(None, {
            "tenant": "ce061903a53545dcaddb300093b477d2",
            "scaling_configuration_id": "6afe46f9-7d3d-4046-8748-3b2a1085ad86",
            "scaling_configuration_name": " config_name_1",
            "instance_config": {
                "disk": [
                    {
                        "size": 40,
                        "volume_type": "SATA",
                        "disk_type": "SYS"
                    },
                    {
                        "size": 100,
                        "volume_type": "SATA",
                        "disk_type": "DATA"
                    }
                ],
                "adminPass": "***",
                "personality": None,
                "instance_name": None,
                "instance_id": None,
                "flavorRef": "103",
                "imageRef": "37ca2b35-6fc7-47ab-93c7-900324809c5c",
                "key_name": "keypair01",
                "public_ip": None,
                "user_data": None,
                "metadata": {"prop1": "value1", "prop2": "value2"}
            },
            "create_time": "2015-07-23T01:04:07Z"
        }
                                                 )

    def setUp(self):
        super(AutoScalingV1BaseTestCase, self).setUp()
        fake_as_client = fakes.FakeAutoScalingV1Client()
        self.app.client_manager.auto_scaling = fake_as_client
        self.app.client_manager.network = mock.Mock()
        self.app.client_manager.compute = mock.Mock()
        self.app.client_manager.image = mock.Mock(
            images=mock.Mock()
        )
        self.mocked_group_find = mock.patch.object(
            group_mgr.GroupManager, "find", return_value=self._group
        )
        self.mocked_config_find = mock.patch.object(
            config_mgr.ConfigManager, "find", return_value=self._config
        )
