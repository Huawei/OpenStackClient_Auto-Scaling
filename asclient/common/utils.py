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
from datetime import datetime


def get_id(obj):
    """Get obj's uuid or object itself if no uuid

    Abstracts the common pattern of allowing both an object or
    an object's ID (UUID) as a parameter when dealing with relationships.
    """
    try:
        return obj.uuid or obj['uuid']
    except AttributeError:
        return obj


def remove_empty_from_dict(original):
    """get a new dict which removes keys with empty values

    :param dict original: original dict, should not be None
    :return: a new dict which removes keys with empty values
    """
    return dict((k, v) for k, v in original.iteritems() if v)


def str_range(start, end):
    """get range with string type

    :param n:
    :return:
    """
    return (str(i) for i in range(start, end))


def format_time(time_in_long, strformat='%Y-%m-%d %H:%M:%S'):
    if time_in_long:
        timestamp = datetime.fromtimestamp(time_in_long)
        return timestamp.strftime(strformat)
    else:
        return ''
