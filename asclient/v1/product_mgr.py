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


class ProductManager(manager.Manager):
    """Product API management"""

    resource_class = resource.Product

    def list(self):
        return self._list("/products", key="products")
