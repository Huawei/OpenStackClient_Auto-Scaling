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

from keystoneclient import exceptions
from osc_lib import utils

from asclient.common import resource as br
from asclient.osc.v1 import config
from asclient.tests import base
from asclient.v1 import config_mgr
from asclient.v1 import resource


class AutoScalingConfigV1BaseTestCase(base.AutoScalingV1BaseTestCase):
    def __init__(self, *args, **kwargs):
        super(AutoScalingConfigV1BaseTestCase, self).__init__(*args, **kwargs)
        self._configs = [{
            "tenant_id": "ce061903a53545dcaddb300093b477d2",
            "status": "STANDBY",
            "scaling_configuration_id": "6afe46f9-7d3d-4046-8748-3b2a1085ad86",
            "scaling_configuration_name": "config_name_1",
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
                "key_name": "keypair02",
                "public_ip": None,
                "user_data": None,
                "metadate": {}
            },
            "create_time": "2015-07-23T01:04:07Z"
        }, {
            "tenant_id": "ce061903a53545dcaddb300093b477d2",
            "status": "ACTIVE",
            "scaling_configuration_id": "24a8c5f3-c713-4aba-ac29-c17101009e5d",
            "scaling_configuration_name": "config_name_2",
            "instance_config": {
                "disk": [
                    {
                        "size": 40,
                        "volume_type": "SATA",
                        "disk_type": "SYS"
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
                "metadata": {}
            },
            "create_time": "2015-07-22T01:08:41Z"
        }]


@mock.patch.object(utils, "find_resource")
@mock.patch.object(config_mgr.ConfigManager, "_list")
class TestListAutoScalingConfigs(AutoScalingConfigV1BaseTestCase):
    def setUp(self):
        super(TestListAutoScalingConfigs, self).setUp()
        self.cmd = config.ListAutoScalingConfig(self.app, None)

    def test_list_configs(self, mock_list, mock_util):
        args = [
            "--name", "config-name",
            "--image", "image-name",
            "--offset", "10",
            "--limit", "20",
        ]
        verify_args = [
            ("name", "config-name"),
            ("image", "image-name"),
            ("offset", 10),
            ("limit", 20),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        configs = [resource.AutoScalingConfig(None, c) for c in self._configs]
        mock_list.return_value = br.ListWithMeta(configs, "Request-ID")
        mock_util.return_value = br.Resource(None, dict(id="image-id"))
        columns, data = self.cmd.take_action(args)

        mock_util.assert_called_once_with(self.app.client_manager.image.images,
                                          "image-name")

        params = {
            "scaling_configuration_name": "config-name",
            "image_id": "image-id",
            "start_number": 10,
            "limit": 20,
        }
        mock_list.assert_called_once_with("/scaling_configuration",
                                          key="scaling_configurations",
                                          params=params)

        self.assertEquals(resource.AutoScalingConfig.list_column_names,
                          columns)
        expected = [('6afe46f9-7d3d-4046-8748-3b2a1085ad86',
                     'config_name_1',
                     '37ca2b35-6fc7-47ab-93c7-900324809c5c',
                     '2015-07-23T01:04:07Z'),
                    ('24a8c5f3-c713-4aba-ac29-c17101009e5d',
                     'config_name_2',
                     '37ca2b35-6fc7-47ab-93c7-900324809c5c',
                     '2015-07-22T01:08:41Z')]
        self.assertEquals(expected, data)


class TestShowAutoScalingConfig(base.AutoScalingV1BaseTestCase):
    def setUp(self):
        super(TestShowAutoScalingConfig, self).setUp()
        self.cmd = config.ShowAutoScalingConfig(self.app, None)

    def test_show_config(self):
        args = ["config-name", ]
        verify_args = [
            ("config", "config-name"),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        with self.mocked_config_find as find:
            columns, data = self.cmd.take_action(args)
            find.assert_called_once_with(args.config)
            self.assertEquals(resource.AutoScalingConfig.show_column_names,
                              columns)
            expected = ('6afe46f9-7d3d-4046-8748-3b2a1085ad86',
                        ' config_name_1',
                        ("disk_type='SYS', size='40', volume_type='SATA'\n"
                         "disk_type='DATA', size='100', volume_type='SATA'"),
                        '103',
                        '37ca2b35-6fc7-47ab-93c7-900324809c5c',
                        'keypair01',
                        None,
                        "prop1='value1', prop2='value2'",
                        '2015-07-23T01:04:07Z')
            self.assertEquals(expected, data)


@mock.patch.object(config_mgr.ConfigManager, "find")
@mock.patch.object(config_mgr.ConfigManager, "_create")
class TestDeleteAutoScalingConfig(AutoScalingConfigV1BaseTestCase):
    def setUp(self):
        super(TestDeleteAutoScalingConfig, self).setUp()
        self.cmd = config.DeleteAutoScalingConfig(self.app, None)

    def test_delete_config(self, mock_create, mock_find):
        args = ["config-name-1", "config-name-2"]
        verify_args = [
            ("config", ["config-name-1", "config-name-2"]),
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        configs = [resource.AutoScalingConfig(None, c) for c in self._configs]
        mock_find.side_effect = br.ListWithMeta(configs, "request-id")
        result = self.cmd.take_action(args)
        json = {
            "scaling_configuration_id": [c.id for c in configs]
        }
        mock_create.assert_called_once_with("/scaling_configurations",
                                            json=json,
                                            raw=True, )
        self.assertEquals('done', result)


class TestCreateAutoScalingConfig(AutoScalingConfigV1BaseTestCase):
    def setUp(self):
        super(TestCreateAutoScalingConfig, self).setUp()
        self.cmd = config.CreateAutoScalingConfig(self.app, None)

    @mock.patch('asclient.osc.v1.config.io.open')
    @mock.patch.object(config_mgr.ConfigManager, "_create")
    def test_create_from_instance(self, mock_create, mock_io_open):
        args = [
            "new-config-name",
            "--instance-id", "instance-1",
            "--key-name", "keypair1",
            "--file", "/etc/data1=/etc/data1",
            "--file", "/etc/data2=/etc/data2",
            "--metadata", "k1=v1",
            "--metadata", "k2=v2",
        ]
        verify_args = [
            ("name", "new-config-name"),
            ("instance_id", "instance-1"),
            ("key_name", "keypair1"),
            ("metadata", dict(k1='v1', k2='v2')),
            ("file", ['/etc/data1=/etc/data1', '/etc/data2=/etc/data2', ])
        ]
        args = self.check_parser(self.cmd, args, verify_args)
        mock_io_open.side_effect = ["content-1", "content-2"]
        mock_create.return_value = self._config
        result = self.cmd.take_action(args)

        json = {
            "scaling_configuration_name": "new-config-name",
            "instance_config": {
                "instance_id": "instance-1",
                "key_name": "keypair1",
                "metadata": dict(k1='v1', k2='v2'),
                "personality": [
                    {'content': 'Y29udGVudC0x', 'path': '/etc/data1'},
                    {'content': 'Y29udGVudC0y', 'path': '/etc/data2'},
                ],
            }
        }
        mock_create.assert_called_once_with("/scaling_configuration",
                                            json=json)
        self.assertEquals("Configuration %s created" % self._config.id, result)

    @mock.patch.object(utils, "find_resource")
    @mock.patch.object(config_mgr.ConfigManager, "_create")
    def test_create_from_image(self, mock_create, mock_find):
        args = [
            "new-config-name",
            "--flavor", "flavor-1",
            "--image", "image-1",
            "--root-volume", "SSD:40",
            "--data-volume", "SSD:40",
            "--data-volume", "SATA:120",
            "--admin-pass", "admin!@#321",
        ]
        verify_args = [
            ("name", "new-config-name"),
            ("flavor", "flavor-1"),
            ("image", "image-1"),
            ("root_volume", dict(volume_type='SSD', size=40)),
            ("data_volumes", [dict(volume_type='SSD', size=40),
                              dict(volume_type='SATA', size=120)]),
            ("admin_pass", "admin!@#321",),
        ]
        args = self.check_parser(self.cmd, args, verify_args)

        mock_create.return_value = self._config
        mock_find.side_effect = [
            br.Resource(None, dict(id='image-id-1')),
            br.Resource(None, dict(id='flavor-id-1')),
        ]
        result = self.cmd.take_action(args)

        json = {
            "scaling_configuration_name": "new-config-name",
            'instance_config': {
                'imageRef': 'image-id-1',
                'flavorRef': 'flavor-id-1',
                'disk': [
                    {'disk_type': 'SYS', 'volume_type': 'SSD',
                     'size': 40},
                    {'disk_type': 'DATA', 'volume_type': 'SSD',
                     'size': 40},
                    {'disk_type': 'DATA', 'volume_type': 'SATA',
                     'size': 120}
                ],
                'adminPass': 'admin!@#321'
            }
        }
        mock_create.assert_called_once_with("/scaling_configuration",
                                            json=json)
        self.assertEquals("Configuration %s created" % self._config.id, result)


class TestFindAutoScalingConfig(AutoScalingConfigV1BaseTestCase):
    def setUp(self):
        super(TestFindAutoScalingConfig, self).setUp()

    @mock.patch.object(config_mgr.ConfigManager, "_get")
    def test_find_config_with_id(self, mocked):
        configs = self.app.client_manager.auto_scaling.configs
        get_return = self._config
        mocked.return_value = get_return
        find = configs.find("config-id-1")
        mocked.assert_called_once_with("/scaling_configuration/config-id-1",
                                       key='scaling_configuration')
        self.assertEquals(get_return, find)

    @mock.patch.object(config_mgr.ConfigManager, "_list")
    @mock.patch.object(config_mgr.ConfigManager, "_get")
    def test_find_config_with_name(self, mocked_get, mock_list):
        configs = self.app.client_manager.auto_scaling.configs
        mocked_get.side_effect = exceptions.ClientException(0)

        _list = [resource.AutoScalingConfig(None, c) for c in self._configs]
        mock_list.return_value = br.ListWithMeta(_list, None)
        find = configs.find("config_name_1")
        params = dict(scaling_configuration_name="config_name_1")
        mock_list.assert_called_once_with("/scaling_configuration",
                                          key="scaling_configurations",
                                          params=params)
        self.assertEquals(_list[0], find)

    @mock.patch.object(config_mgr.ConfigManager, "_list")
    @mock.patch.object(config_mgr.ConfigManager, "_get")
    def test_find_config_with_name_no_match(self, mocked_get, mock_list):
        configs = self.app.client_manager.auto_scaling.configs
        mocked_get.side_effect = exceptions.ClientException(0)
        mock_list.return_value = br.ListWithMeta([], None)
        self.assertRaises(exceptions.NotFound, configs.find, "config_name_1")
