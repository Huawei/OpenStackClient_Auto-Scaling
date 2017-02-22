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
import base64

from keystoneauth1 import exceptions
import six

from asclient.common import exceptions as execs
from asclient.common import manager
from asclient.common import utils
from asclient.common.i18n import _
from asclient.v1 import resource


class ConfigManager(manager.Manager):
    """Auto Scaling Config API Management"""
    resource_class = resource.AutoScalingConfig

    def find(self, id_or_name):
        """find auto scaling instance config by id or name

        exactly match will be performed
        :param id_or_name:
        :return:
        """
        try:
            # try keyword as UUID
            return self.get(id_or_name)
        except exceptions.ClientException as e:
            pass

        results = self.list(name=id_or_name)
        filtered = [result for result in results if result.name == id_or_name]
        matched_number = len(filtered)
        if matched_number > 1:
            raise execs.NotUniqueMatch
        elif matched_number == 1:
            return filtered[0]

        message = _("No Auto Scaling Configuration with ID or name of "
                    "'%s' exists.") % id_or_name
        raise exceptions.NotFound(message)

    def list(self, name=None, image_id=None, offset=None, limit=None):
        """list auto scaling instance configuration

        :param name: configuration name
        :param image_id: configuration image id
        :param offset:
        :param limit:
        :return: [resource.AutoScalingConfig]
        """
        params = utils.remove_empty_from_dict({
            "scaling_configuration_name": name,
            "image_id": image_id,
            "start_number": offset,
            "limit": limit,
        })
        return self._list("/scaling_configuration",
                          key="scaling_configurations",
                          params=params)

    def get(self, config_id):
        """get auto scaling configuration by id

        :param config_id:
        :return:
        """
        return self._get("/scaling_configuration/" + config_id,
                         key="scaling_configuration")

    def delete(self, config_ids):
        """delete auto scaling configuration by id

        :param config_id:
        :return:
        """
        json = {
            "scaling_configuration_id": config_ids
        }
        return self._create("/scaling_configurations", json=json, raw=True)

    def create(self, name, instance_id=None, flavor_id=None, image_id=None,
               disk=None, key_name=None, admin_pwd=None, files=None,
               metadata=None):
        """create a new auto scaling instance configuration

        :param name: Something to name the configuration.
        :param instance_id: Create Instance with the `instance` as template
        :param image_id: The :class:`Image` to boot with.
        :param flavor_id: The :class:`Flavor` to boot onto.
        :param disk: create instance with disk settings, disk is an array like
                    [{"size": 40, "volume_type": "SATA", "disk_type": "SYS"},
                    {"size": 40, "volume_type": "SATA", "disk_type": "DATA"}]
        :param key_name: (optional extension) name of previously created
                      keypair to inject into the instance. Not supported for
                      Window Server. Either key_name or admin_pwd should be set
        :param admin_pwd: (optional extension), admin user login password
        :param files: A dict of files to overwrite on the server upon boot.
                      Keys are file names (i.e. ``/etc/passwd``) and values
                      are the file contents (either as a string or as a
                      file-like object). A maximum of five entries is allowed,
                      and each file must be 10k or less.
        :param metadata: A dict of arbitrary key/value metadata to store for
                instance. Both keys and values must be <=255 characters.
        :return:
        """
        personality = []
        if files:
            for filepath, file_or_string in sorted(files.items(),
                                                   key=lambda x: x[0]):
                if hasattr(file_or_string, 'read'):
                    data = file_or_string.read()
                else:
                    data = file_or_string

                if six.PY3 and isinstance(data, str):
                    data = data.encode('utf-8')
                content = base64.b64encode(data).decode('utf-8')
                personality.append({
                    'path': filepath,
                    'content': content,
                })

        config = utils.remove_empty_from_dict({
            "instance_id": instance_id,
            "flavorRef": flavor_id,
            "imageRef": image_id,
            "disk": disk,
            "key_name": key_name,
            "adminPass": admin_pwd,
            "metadata": metadata,
            "personality": personality,
        })

        json = {
            "scaling_configuration_name": name,
            "instance_config": config
        }
        return self._create("/scaling_configuration", json=json)
