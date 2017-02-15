#   Copyright 2016 Huawei, Inc. All rights reserved.
#
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
from asclient.osc.v1 import policy
from asclient.tests import base
from asclient.v1 import policy_mgr
from asclient.v1 import resource


class TestPolicy(base.WorkspaceV1BaseTestCase):

    instance = {
        "usb_port_redirection": {
            "enable": True,
            "options": {
                "usb_image_enable": False,
                "usb_video_enable": True,
                "usb_printer_enable": False,
                "usb_storage_enable": True,
                "usb_smart_card_enable": False
            }
        },
        "printer_redirection": {
            "enable": True,
            "options": {
                "sync_client_default_printer_enable": False,
                "universal_printer_driver": "Universal Printing PCL 6"
            }
        },
        "file_redirection": {
            "redirection_mode": "READ_AND_WRITE",
            "options": {
                "fixed_drive_enable": True,
                "removable_drive_enable": False,
                "cd_rom_drive_enable": True,
                "network_drive_enable": True
            }
        },
        "clipboard_redirection": "TWO_WAY_ENABLED",
        "hdp_plus": {
            "hdp_plus_enable": False,
            "display_level": "QUALITY_FIRST",
            "options": {
                "bandwidth": 24315,
                "frame_rate": 18,
                "video_frame_rate": 20,
                "smoothing_factor": 58,
                "lossy_compression_quality": 88
            }
        }
    }

    def __init__(self, *args, **kwargs):
        super(TestPolicy, self).__init__(*args, **kwargs)
        self._policy = None

    def setUp(self):
        super(TestPolicy, self).setUp()
        self._policy = resource.Policy(None, self.instance, attached=True)


class TestPolicyShow(TestPolicy):
    def setUp(self):
        super(TestPolicyShow, self).setUp()
        self.cmd = policy.ShowPolicy(self.app, None)

    @mock.patch.object(policy_mgr.PolicyManager, "_get")
    def test_desktop_show_with_computer_name(self, mocked_get):
        self.check_parser(self.cmd, [], ())
        mocked_get.return_value = self._policy
        columns, data = self.cmd.take_action(None)

        expect_data = (
            'Enabled', 'Disabled', 'Enabled', 'Disabled', 'Enabled',
            'Disabled', 'Enabled', 'Disabled', 'Universal Printing PCL 6',
            'READ_AND_WRITE', 'Enabled', 'Disabled', 'Enabled', 'Enabled',
            'TWO_WAY_ENABLED', 'Disabled', 'QUALITY_FIRST', 24315, 18, 20,
            58, 88)
        self.assertEqual(expect_data, data)


class TestPolicyEdit(TestPolicy):
    def setUp(self):
        super(TestPolicyEdit, self).setUp()
        self.cmd = policy.EditPolicy(self.app, None)

    @mock.patch.object(policy_mgr.PolicyManager, "_update_all")
    def test_enable_redirection_options(self, mocked_put):
        args = [
            "--enable-usb-port-redirection",
            "--enable-usb-image",
            "--enable-usb-video",
            "--enable-usb-printer",
            "--enable-usb-storage",
            "--enable-usb-smart-card",

            "--enable-printer-redirection",
            "--enable-sync-client-default-printer",
            "--universal-printer-driver", "Universal Printing PCL 6",

            "--file-redirection-mode", "READ_AND_WRITE",
            "--enable-fixed-drive",
            "--enable-removable-drive",
            "--enable-cd-rom-drive",
            "--enable-network-drive",
            "--enable-network-drive",

            "--clipboard-redirection", "DISABLED",

            "--enable-hdp-plus",
            "--display-level", "QUALITY_FIRST",
            "--bandwidth", "24315",
            "--frame-rate", "18",
            "--video-frame-rate", "20",
            "--smoothing-factor", "58",
            "--lossy-compression-quality", "88"
        ]
        verify_args = [
            ("enable_usb_port_redirection", True),
            ("enable_usb_image", True),
            ("enable_usb_video", True),
            ("enable_usb_printer", True),
            ("enable_usb_storage", True),
            ("enable_usb_smart_card", True),

            ("enable_printer_redirection", True),
            ("enable_sync_client_default_printer", True),
            ("universal_printer_driver", "Universal Printing PCL 6"),

            ("file_redirection_mode", "READ_AND_WRITE"),
            ("enable_fixed_drive", True),
            ("enable_removable_drive", True),
            ("enable_cd_rom_drive", True),
            ("enable_network_drive", True),

            ("clipboard_redirection", "DISABLED"),

            ("enable_hdp_plus", True),
            ("display_level", "QUALITY_FIRST"),
            ("bandwidth", 24315),
            ("frame_rate", 18),
            ("video_frame_rate", 20),
            ("smoothing_factor", 58),
            ("lossy_compression_quality", 88),
        ]
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        mocked_put.return_value = base_resource.StrWithMeta("", "Request-Id")
        result = self.cmd.take_action(parsed_args)

        json = {
            "policies": {
                "usb_port_redirection": {
                    "enable": True,
                    "options": {
                        "usb_image_enable": True,
                        "usb_video_enable": True,
                        "usb_printer_enable": True,
                        "usb_storage_enable": True,
                        "usb_smart_card_enable": True,
                    }
                },
                "printer_redirection": {
                    "enable": True,
                    "options": {
                        "sync_client_default_printer_enable": True,
                        "universal_printer_driver": "Universal Printing PCL 6"
                    }
                },
                "file_redirection": {
                    "redirection_mode": "READ_AND_WRITE",
                    "options": {
                        "fixed_drive_enable": True,
                        "removable_drive_enable": True,
                        "cd_rom_drive_enable": True,
                        "network_drive_enable": True
                    }
                },
                "clipboard_redirection": "DISABLED",

                "hdp_plus": {
                    "hdp_plus_enable": True,
                    "display_level": "QUALITY_FIRST",
                    "options": {
                        "lossy_compression_quality": 88
                    }
                }
            }
        }
        mocked_put.assert_called_once_with(
            "/policies", json=json
        )
        self.assertEqual('done', result)

    @mock.patch.object(policy_mgr.PolicyManager, "_update_all")
    def test_disable_redirection_options(self, mocked_put):
        args = [
            "--disable-usb-port-redirection",
            "--enable-usb-image",
            "--enable-usb-video",
            "--enable-usb-printer",
            "--enable-usb-storage",
            "--enable-usb-smart-card",

            "--disable-printer-redirection",
            "--enable-sync-client-default-printer",
            "--universal-printer-driver", "Universal Printing PCL 6",

            "--file-redirection-mode", "DISABLED",
            "--enable-fixed-drive",
            "--enable-removable-drive",
            "--enable-cd-rom-drive",
            "--enable-network-drive",
            "--enable-network-drive",

            "--clipboard-redirection", "DISABLED",
        ]
        verify_args = [
            ("enable_usb_port_redirection", False),
            ("enable_usb_image", True),
            ("enable_usb_video", True),
            ("enable_usb_printer", True),
            ("enable_usb_storage", True),
            ("enable_usb_smart_card", True),

            ("enable_printer_redirection", False),
            ("enable_sync_client_default_printer", True),
            ("universal_printer_driver", "Universal Printing PCL 6"),

            ("file_redirection_mode", "DISABLED"),
            ("enable_fixed_drive", True),
            ("enable_removable_drive", True),
            ("enable_cd_rom_drive", True),
            ("enable_network_drive", True),

            ("clipboard_redirection", "DISABLED"),
        ]
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        mocked_put.return_value = base_resource.StrWithMeta("", "Request-Id")
        result = self.cmd.take_action(parsed_args)
        json = {
            "policies": {
                "usb_port_redirection": {
                    "enable": False,
                },
                "printer_redirection": {
                    "enable": False,
                },
                "file_redirection": {
                    "redirection_mode": "DISABLED",
                },
                "clipboard_redirection": "DISABLED",
            }
        }
        mocked_put.assert_called_once_with(
            "/policies", json=json
        )
        self.assertEqual('done', result)

    @mock.patch.object(policy_mgr.PolicyManager, "_update_all")
    def test_hdp_plus_disable(self, mocked_put):
        args = [
            "--disable-hdp-plus",
            "--display-level", "QUALITY_FIRST",
            "--bandwidth", "24315",
            "--frame-rate", "18",
            "--video-frame-rate", "20",
            "--smoothing-factor", "58",
            "--lossy-compression-quality", "88"
        ]
        verify_args = [
            ("enable_hdp_plus", False),
            ("display_level", "QUALITY_FIRST"),
            ("bandwidth", 24315),
            ("frame_rate", 18),
            ("video_frame_rate", 20),
            ("smoothing_factor", 58),
            ("lossy_compression_quality", 88),
        ]
        parsed_args = self.check_parser(self.cmd, args, verify_args)

        mocked_put.return_value = base_resource.StrWithMeta("", "Request-Id")
        result = self.cmd.take_action(parsed_args)
        json = {
            "policies": {
                "hdp_plus": {
                    "hdp_plus_enable": False,
                    "display_level": "QUALITY_FIRST",
                    "options": {
                        "bandwidth": 24315,
                        "frame_rate": 18,
                        "video_frame_rate": 20,
                        "smoothing_factor": 58,
                    }
                }
            }
        }
        mocked_put.assert_called_once_with(
            "/policies", json=json
        )
        self.assertEqual('done', result)
