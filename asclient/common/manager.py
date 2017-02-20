#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack Foundation
# Copyright 2016 Qianbiao NG
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

import six

from asclient.common import resource


class Manager(object):
    """Base Manager for API service.

    Managers interact with a particular type of API (servers, flavors, images,
    etc.) and provide CRUD operations for them.
    """

    resource_class = resource.Resource

    def __init__(self, http_client):
        """initial with open stack http client

        :param http_client: http requester with type of
            asclient.common.httpclient.OpenStackHttpClient
        """
        self.http_client = http_client

    def get_data(self, data, path=None):
        if data and path and path != '':
            nested = path.split('.')
            return self.get_data(data[nested[0]], '.'.join(nested[1:]))
        return data

    def _list(self, url, params={}, resource_class=None, key=None, headers={}):
        """ common list resource function

        :rtype: Resource
        """
        resp, body = self.http_client.get(url, params=params, headers=headers)
        resource_class = (resource_class if resource_class
                          else self.resource_class)
        # get required body part
        data = self.get_data(body, key)
        data = data if data else []
        if all([isinstance(_resource, six.string_types)
                for _resource in data]):
            items = data
        else:
            items = [resource_class(self, _resource, attached=True, resp=resp)
                     for _resource in data if _resource]
        return resource.ListWithMeta(items, resp)

    def _delete(self, url, headers={}):
        resp, body = self.http_client.delete(url, headers=headers)
        return self.mixin_meta(body, resp)

    def _update(self, url, json, key=None, raw=False, headers={}):
        """update part of resource with PATCH method"""
        resp, body = self.http_client.patch(url, json=json, headers=headers)
        # PATCH requests may not return a body
        if body:
            # get required body part
            content = self.get_data(body, key)
            if raw:
                return self.mixin_meta(content, resp)
            else:
                return self.resource_class(self, content, resp=resp)
        else:
            return resource.StrWithMeta(resp.text, resp)

    def _update_all(self, url, json, key=None, raw=False, headers={}):
        """update resource with PUT method"""
        resp, body = self.http_client.put(url, json=json, headers=headers)
        # PATCH requests may not return a body
        if body:
            # get required body part
            content = self.get_data(body, key)
            if raw:
                return self.mixin_meta(content, resp)
            else:
                return self.resource_class(self, content, resp=resp)
        else:
            return resource.StrWithMeta(resp.text, resp)

    def _create(self, url, json=None, key=None, raw=False, headers={}):
        if json:
            resp, body = self.http_client.post(url, json=json, headers=headers)
        else:
            resp, body = self.http_client.post(url, headers=headers)

        # get required body part
        content = self.get_data(body, key)
        if raw or not body:
            return self.mixin_meta(content, resp)
        else:
            return self.resource_class(self, content, resp=resp)

    def _get(self, url, params={}, key=None, raw=False, resource_class=None,
             headers={}):
        resp, body = self.http_client.get(url, params=params, headers=headers)
        # get required body part
        if body:
            content = self.get_data(body, key)
            if raw:
                return self.mixin_meta(content, resp)
            else:
                rc = resource_class if resource_class else self.resource_class
                return self.resource_class(self,
                                           content,
                                           resp=resp,
                                           attached=True)
        else:
            return resource.StrWithMeta(resp.text, resp)

    @staticmethod
    def mixin_meta(item, resp):
        if isinstance(item, six.string_types):
            if six.PY2 and isinstance(item, six.text_type):
                return resource.UnicodeWithMeta(item, resp)
            else:
                return resource.StrWithMeta(item, resp)
        elif isinstance(item, six.binary_type):
            return resource.BytesWithMeta(item, resp)
        elif isinstance(item, list):
            return resource.ListWithMeta(item, resp)
        elif isinstance(item, tuple):
            return resource.TupleWithMeta(item, resp)
        elif item is None:
            return resource.TupleWithMeta((), resp)
        else:
            return resource.DictWithMeta(item, resp)
