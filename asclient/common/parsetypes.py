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
import argparse
import string
from datetime import datetime

from osc_lib.i18n import _


def date_type(date_format):
    def wrapped(user_input):
        try:
            return datetime.strptime(user_input, date_format)
        except ValueError:
            tpl = _("%s is not a valid date with format %s")
            msg = tpl % (user_input, date_format)
        raise argparse.ArgumentTypeError(msg)

    return wrapped


def int_range_type(from_, to):
    def wrapped(user_input):
        try:
            int_user_input = int(user_input)
        except ValueError:
            msg = _("Not a valid integer value: %s") % user_input
            raise argparse.ArgumentTypeError(msg)

        if int_user_input > to:
            tpl = _("Your input %s is great than max valid value %d")
            msg = tpl % (user_input, to)
            raise argparse.ArgumentTypeError(msg)

        if int_user_input < from_:
            tpl = _("Your input %s is less than min valid value %d")
            msg = tpl % (user_input, from_)
            raise argparse.ArgumentTypeError(msg)

        return int_user_input

    return wrapped


def volume_type(user_input=''):
    try:
        volume = user_input.split(':', 1)
        if len(volume) != 2:
            raise ValueError
        _volume_type = string.upper(volume[0])
        volume_size = int(volume[1])
        if _volume_type not in ['SSD', 'SATA', 'SAS']:
            raise ValueError
        return dict(volume_type=_volume_type, size=volume_size)
    except ValueError:
        msg = _("%s is not a valid volume format") % user_input
        raise argparse.ArgumentTypeError(msg)


# noinspection PyTypeChecker
def subnet_type(user_input=''):
    try:
        kv = {}
        for kv_str in user_input.split(","):
            split = kv_str.split("=", 1)
            kv[split[0]] = split[1]

        subnet = {}
        if "subnet" in kv:
            subnet["subnet_id"] = kv["subnet"]
        else:
            raise ValueError

        if "ip" in kv:
            subnet["ip_address"] = kv["ip"]

        return subnet
    except ValueError as e:
        msg = _("%s is not a valid NIC") % user_input
        raise argparse.ArgumentTypeError(msg)


# noinspection PyTypeChecker
def policy_action_type(user_input=''):
    try:
        split = user_input.split(':', 1)
        if len(split) != 2:
            raise ValueError
        operation = split[0]
        instance_number = int(split[1])
        return dict(operation=operation, instance_number=instance_number)
    except ValueError:
        msg = _("%s is not a valid policy action") % user_input
        raise argparse.ArgumentTypeError(msg)


# noinspection PyTypeChecker
def recurrence_type(user_input=''):
    try:
        split = user_input.split(':', 1)
        if len(split) != 2:
            raise ValueError
        type_ = split[0]
        value = split[1]
        # ok, let server validate the user input
        # if type_ not in ['Daily', 'Weekly', 'Monthly']:
        #     msg = _("Recurrence type must be one of "
        #             "('Daily', 'Weekly', 'Monthly')")
        #     raise argparse.ArgumentTypeError(msg)
        return dict(recurrence_type=type_, recurrence_value=value)
    except ValueError:
        msg = _("%s is not a valid policy action") % user_input
        raise argparse.ArgumentTypeError(msg)
