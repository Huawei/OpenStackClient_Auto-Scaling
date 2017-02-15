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
import os

from asclient.common.i18n import _


class BaseParser(object):
    @staticmethod
    def register_service_option(parser, service_type):
        service_env = service_type.upper().replace('-', '_')
        parser.add_argument(
            '--os-{service_type}-api-version'.format(
                service_type=service_type),
            metavar='<%s-api-version>' % service_type,
            default=os.environ.get(
                'OS_{service_type}_API_VERSION'.format(
                    service_type=service_env), None),
            help=(_('Which version of the service API to use for'
                    ' the {service_type} service').format(
                service_type=service_type)))
        parser.add_argument(
            '--os-{service_type}-endpoint-override'.format(
                service_type=service_type),
            metavar='<%s-endpoint-override>' % service_type,
            default=os.environ.get(
                'OS_{service_type}_ENDPOINT_OVERRIDE'.format(
                    service_type=service_env), None),
            help=(_('Endpoint to use for the {service_type} service'
                    ' instead of the endpoint in the catalog').format(
                service_type=service_type)))

    @staticmethod
    def add_limit_option(parser):
        parser.add_argument(
            "--limit",
            metavar="<count>",
            type=int,
            help=_("return result limit")
        )

    @staticmethod
    def add_offset_option(parser):
        parser.add_argument(
            "--offset",
            metavar="<count>",
            type=int,
            help=_("return result offset")
        )
