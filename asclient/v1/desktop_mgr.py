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
from keystoneauth1 import exceptions

from asclient.common import exceptions as execs
from asclient.common import manager
from asclient.common import utils
from asclient.common.i18n import _
from asclient.v1 import resource


class DesktopManager(manager.Manager):
    """Desktop API management"""

    resource_class = resource.Desktop

    def find(self, keyword):
        """find desktop by keyword (id only for now)"""
        try:
            # try keyword as UUID
            return self.get(keyword)
        except exceptions.ClientException as e:
            pass

        results = self.list_detail(computer_name=keyword)
        matched_number = len(results)
        if matched_number > 1:
            raise execs.NotUniqueMatch
        elif matched_number == 1:
            return results[0]

        message = _("No Desktop with ID or compute name of "
                    "'%s' exists.") % keyword
        raise exceptions.NotFound(message)

    def create(self, computer_name, user_name, user_email, product_id,
               root_volume, data_volumes=None, image_id=None,
               security_groups=None, nics=None,
               ):
        """create desktop"""
        instance = utils.remove_empty_from_dict({
            "user_name": user_name,
            "user_email": user_email,
            "product_id": product_id,
            "image_id": image_id,
            "computer_name": computer_name,
            "security_groups": security_groups,
            "root_volume": root_volume,
            "data_volumes": data_volumes,
            "nics": nics,
        })
        return self._create("/desktops", json=dict(desktops=[instance]),
                            raw=True)

    def delete(self, desktop_id):
        """delete desktop"""
        return self._delete("/desktops/" + desktop_id)

    def reboot(self, desktop_id, force_reboot):
        """reboot desktop

        :param desktop_id: desktop id
        :param force_reboot: if true, hard reboot else soft reboot
        :return:
        """
        json = {
            "reboot": {
                "type": "HARD" if force_reboot else "SOFT"
            }
        }
        return self._create("/desktops/%s/action" % desktop_id, json=json)

    def start(self, desktop_id):
        """start desktop"""
        json = {
            "os-start": None
        }
        return self._create("/desktops/%s/action" % desktop_id, json=json)

    def stop(self, desktop_id):
        """start desktop"""
        json = {
            "os-stop": None
        }
        return self._create("/desktops/%s/action" % desktop_id, json=json)

    def list(self, ip=None, status=None, user_name=None, computer_name=None,
             marker=None, limit=None):
        params = utils.remove_empty_from_dict({
            "desktop_ip": ip,
            "status": status,
            "user_name": user_name,
            "computer_name": computer_name,
            "limit": limit,
            "marker": marker
        })
        return self._list("/desktops", params=params, key="desktops")

    def get(self, desktop_id):
        """get desktop details"""
        return self._get("/desktops/" + desktop_id, key="desktop")

    def list_detail(self, ip=None, status=None, user_name=None,
                    computer_name=None, marker=None, limit=None):
        """list desktops with detail"""
        params = utils.remove_empty_from_dict({
            "desktop_ip": ip,
            "status": status,
            "user_name": user_name,
            "computer_name": computer_name,
            "limit": limit,
            "marker": marker
        })
        return self._list("/desktops/detail", params=params, key="desktops")

    def edit(self, desktop_id, computer_name):
        """edit desktop meta, only computer name could be edit for now

            note:: restart will be applied after edit
        """
        json = {
            "desktop": {
                "computer_name": computer_name
            }
        }
        return self._update_all("/desktops/%s" % desktop_id, json=json)
