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

import copy

from requests import Response
import six


class RequestIdMixin(object):
    """Wrapper class to expose x-openstack-request-id to the caller."""

    request_id = None

    def mixin_request_id(self, resp):
        """mixin request id from request response

        :param request.Response resp: http response
        """
        if isinstance(resp, Response):
            # Extract 'X-Openstack-Request-Id' from headers if
            # response is a Response object.
            request_id = (resp.headers.get('openstack-request-id') or
                          resp.headers.get('x-openstack-request-id') or
                          resp.headers.get('x-compute-request-id'))
        else:
            # If resp is of type string or None.
            request_id = resp

        self.request_id = request_id


class Resource(RequestIdMixin):
    """Represents an _antiddos of open-stack Resource object

    Resource represents a particular _antiddos of a target resource.
    This is pretty much just a bag for attributes.

    :param manager: ResourceManager object
    :param instance: dictionary representing resource _antiddos
    :param attached: prevent lazy-loading if set to True
    :param resp: Response or list of Response objects
    """

    # original dict type _antiddos

    def __init__(self, manager, instance, attached=False, resp=None):
        """initial resource

        :param manager:
        :param instance:
        :param attached:
        :param resp:
        """
        self.manager = manager
        self._instance = instance
        self._attached = attached
        self._initial_attr()
        self.mixin_request_id(resp)

    def _initial_attr(self):
        for (k, v) in six.iteritems(self._instance):
            setattr(self, k, v)

    @property
    def original(self):
        return self._instance

    def has_attached(self):
        return self._attached

    def set_attached(self, val):
        self._attached = val

    # why we need to override setstate?
    # def __setstate__(self, d):
    #     for k, v in d.items():
    #         setattr(self, k, v)

    def __getattr__(self, k):
        # disallow lazy-loading if already loaded once
        if not self.has_attached():
            self.attach()
        if k not in self.__dict__:
            raise AttributeError(k)
        else:
            return self.__dict__[k]

    def attach(self):
        if not self.has_attached():
            # if we have to bail, we know we tried.
            # so just mark the resource as attached
            self.set_attached(True)

            # try to call resource manager's get
            if hasattr(self.manager, 'get') and self.uuid:
                new = self.manager.get(self.uuid)
                if new:
                    self._instance = new.original
                    self._initial_attr()
                    self.request_id = new.request_id

    def __repr__(self):
        repr_keys = sorted(k for k in self.__dict__.keys() if k[0] != '_' and
                           k not in ('manager', 'request_id'))
        attr_list = ", ".join("%s=%s" % (k, getattr(self, k))
                              for k in repr_keys)
        return "<%s %s>" % (self.__class__.__name__, attr_list)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.original == other.original

    def __ne__(self, other):
        return not self.__eq__(other)


class ListWithMeta(list, RequestIdMixin):
    def __init__(self, values, resp):
        super(ListWithMeta, self).__init__(values)
        self.mixin_request_id(resp)


class DictWithMeta(dict, RequestIdMixin):
    def __init__(self, values, resp):
        super(DictWithMeta, self).__init__(values)
        self.mixin_request_id(resp)


class TupleWithMeta(tuple, RequestIdMixin):
    def __new__(cls, values, resp):
        return super(TupleWithMeta, cls).__new__(cls, values)

    def __init__(self, values, resp):
        self.mixin_request_id(resp)


class StrWithMeta(str, RequestIdMixin):
    def __new__(cls, value, resp):
        return super(StrWithMeta, cls).__new__(cls, value)

    def __init__(self, values, resp):
        self.mixin_request_id(resp)


class BytesWithMeta(six.binary_type, RequestIdMixin):
    def __new__(cls, value, resp):
        return super(BytesWithMeta, cls).__new__(cls, value)

    def __init__(self, values, resp):
        self.mixin_request_id(resp)


if six.PY2:
    class UnicodeWithMeta(six.text_type, RequestIdMixin):
        def __new__(cls, value, resp):
            return super(UnicodeWithMeta, cls).__new__(cls, value)

        def __init__(self, values, resp):
            self.mixin_request_id(resp)
