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
from asclient.common import exceptions

from keystoneauth1 import adapter
from keystoneauth1.exceptions import HttpError


class OpenStackHttpClient(adapter.LegacyJsonAdapter):
    """Common OpenStack API HTTP Client with response data type of JSON."""

    def __init__(self, session, endpoint=None, **kwargs):
        """Initialize a new client to access open-stack API.

        :param keystoneauth1.session.Session session:
            The session to be used for making the HTTP API calls.
        :param string endpoint:
            An optional URL to be used as the base for API requests on this API
        :param kwargs:
            Keyword arguments passed to keystoneauth1.adapter.Adapters
        """

        # follow default key arguments, setup endpoint_override directly
        # override endpoint if user specified an endpoint
        if endpoint:
            kwargs['endpoint_override'] = endpoint

        # if session.auth:
        #     kwargs['auth'] = session.auth

        super(OpenStackHttpClient, self).__init__(session, **kwargs)

    def request(self, *args, **kwargs):
        """Override request method to handle http exceptions

        HuaWei Service return not standard error structure
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return super(OpenStackHttpClient, self).request(*args, **kwargs)
        except HttpError as http:
            raise exceptions.from_http_error(http)
