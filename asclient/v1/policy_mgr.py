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

from asclient.common import manager
from asclient.common import utils
from asclient.v1 import resource


class PolicyManager(manager.Manager):
    """Policy API management"""

    resource_class = resource.Policy

    def get(self):
        return self._get("/policies", key="policies")

    def edit(self, enable_usb_port_redirection=None,
             enable_usb_image=None, enable_usb_video=None,
             enable_usb_printer=None, enable_usb_storage=None,
             enable_usb_smart_card=None, enable_printer_redirection=None,
             enable_sync_client_default_printer=None,
             universal_printer_driver=None, file_redirection_mode=None,
             enable_fixed_drive=None, enable_removable_drive=None,
             enable_cd_rom_drive=None, enable_network_drive=None,
             clipboard_redirection=None, enable_hdp_plus=None,
             display_level=None, bandwidth=None, frame_rate=None,
             video_frame_rate=None, smoothing_factor=None,
             lossy_compression_quality=None,
             ):
        policies = {}

        if enable_usb_port_redirection is not None:
            usb = dict(enable=enable_usb_port_redirection)
            options = utils.remove_empty_from_dict({
                "usb_image_enable": enable_usb_image,
                "usb_video_enable": enable_usb_video,
                "usb_printer_enable": enable_usb_printer,
                "usb_storage_enable": enable_usb_storage,
                "usb_smart_card_enable": enable_usb_smart_card
            })
            if enable_usb_port_redirection and options:
                usb["options"] = options
            policies["usb_port_redirection"] = usb

        if enable_printer_redirection is not None:
            printer = dict(enable=enable_printer_redirection)
            options = utils.remove_empty_from_dict({
                "sync_client_default_printer_enable":
                    enable_sync_client_default_printer,
                "universal_printer_driver": universal_printer_driver,
            })
            if enable_printer_redirection and options:
                printer["options"] = options
            policies["printer_redirection"] = printer

        if file_redirection_mode:
            file_redirection = dict(redirection_mode=file_redirection_mode)
            options = utils.remove_empty_from_dict({
                "fixed_drive_enable": enable_fixed_drive,
                "removable_drive_enable": enable_removable_drive,
                "cd_rom_drive_enable": enable_cd_rom_drive,
                "network_drive_enable": enable_network_drive,
            })
            if file_redirection_mode != "DISABLED" and options:
                file_redirection["options"] = options
            policies["file_redirection"] = file_redirection

        if clipboard_redirection:
            policies["clipboard_redirection"] = clipboard_redirection

        # HDPPlus和显示级别共同控制的选项。
        # 当开启hdp_plus_enable时，可修改lossy_compression_quality
        # 字段的值；否则可修改options中所有字段的值。
        hdp_plus = utils.remove_empty_from_dict({
            "hdp_plus_enable": enable_hdp_plus,
            "display_level": display_level,
        })

        if enable_hdp_plus is not None:
            if enable_hdp_plus:
                if lossy_compression_quality is not None:
                    hdp_plus["options"] = dict(
                        lossy_compression_quality=lossy_compression_quality)
            else:
                options = utils.remove_empty_from_dict({
                    "bandwidth": bandwidth,
                    "frame_rate": frame_rate,
                    "video_frame_rate": video_frame_rate,
                    "smoothing_factor": smoothing_factor,
                })

                if options:
                    hdp_plus["options"] = options

        if hdp_plus:
            policies["hdp_plus"] = hdp_plus

        return self._update_all("/policies", json=dict(policies=policies))
