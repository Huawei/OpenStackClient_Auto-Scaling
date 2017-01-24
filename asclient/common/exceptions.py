#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from keystoneauth1.exceptions import base


def from_http_error(exception):
    """ReBuild exception message from HttpError

    :param keystoneauth1.exceptions.HttpError exception:
    :return:
    """
    clazz = type(exception)
    response = exception.response
    req_id = response.headers.get("x-openstack-request-id")

    kwargs = {
        "http_status": response.status_code,
        "response": response,
        "method": exception.method,
        "url": exception.url,
        "request_id": req_id,
    }
    if "retry-after" in response.headers:
        kwargs["retry_after"] = response.headers["retry-after"]

    content_type = response.headers.get("Content-Type", "")
    if content_type.startswith("application/json"):
        try:
            body = response.json()
        except ValueError:  # pragma: no cover
            pass
        else:
            message = ''
            if isinstance(body, dict):
                if "error_code" in body:
                    message += '[%s] ' % body["error_code"]
                if "error_description" in body:
                    message += body["error_description"]

            if message != '':
                kwargs["message"] = message
    elif content_type.startswith("text/"):
        kwargs["message"] = response.text

    return clazz(**kwargs)


class NotUniqueMatch(base.ClientException):
    message = "Could not locate unique resource"



