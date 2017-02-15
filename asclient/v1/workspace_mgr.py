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


class WorkspaceManager(manager.Manager):
    """Workspace workspace API management"""
    resource_class = resource.Workspace

    def enable(self, domain_type, domain_name, domain_admin_account,
               domain_password, vpc_id, subnet_ids, access_mode,
               active_domain_ip=None, active_dns_ip=None,
               standby_domain_ip=None, standby_dns_ip=None):
        """enable workspace service

        :param domain_type:
        :param domain_name:
        :param domain_admin_account:
        :param domain_password:
        :param vpc_id:
        :param subnet_ids: [subnet-id-1, subnet-id-2]
        :param access_mode:
        :param active_domain_ip:
        :param active_dns_ip:
        :param standby_domain_ip:
        :param standby_dns_ip:
        :return:
        """
        ad = {
            "domain_type": domain_type,
            "domain_name": domain_name,
            "domain_admin_account": domain_admin_account,
            "domain_password": domain_password
        }

        if domain_type == 'LOCAL_AD':
            ad["active_domain_ip"] = active_domain_ip
            ad["active_dns_ip"] = active_dns_ip
            if standby_domain_ip:
                ad["standby_domain_ip"] = standby_domain_ip
            if standby_dns_ip:
                ad["standby_dns_ip"] = standby_dns_ip

        json = {
            "ad_domains": ad,
            "vpc_id": vpc_id,
            "subnet_ids": [dict(subnet_id=sid) for sid in subnet_ids],
            "access_mode": access_mode
        }
        return self._create("/workspaces", json=json, raw=True)

    def edit(self, domain_type, domain_admin_account=None,
             old_domain_password=None, domain_password=None):
        domains = utils.remove_empty_from_dict({
            "domain_type": domain_type,
            "domain_admin_account": domain_admin_account,
            "old_domain_password": old_domain_password,
            "domain_password": domain_password,
        })
        self._update_all("/workspaces",
                         json=dict(ad_domains=domains),
                         raw=True)

    def get(self):
        """get workspace detail"""
        return self._get("/workspaces")

    def disable(self):
        """delete workspace

        this is a asynchronous task
        """
        return self._delete("/workspaces")
