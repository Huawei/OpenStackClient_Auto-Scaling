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
import six
from asclient.common import resource
from asclient.common import utils


class MyClass(object):
    def __init__(self):
        pass

    def a(self):
        return 1


class MyClass2(object):
    def b(self):
        return 2


class MyClass3(MyClass, MyClass2):
    pass


class SampleResource(resource.Resource):
    pass

if __name__ == "__main__":

    print utils.format_time(float(1485245386329/1000))

    r = SampleResource(None, dict(foo='bar', baz='spam'))
    print zip(*sorted(six.iteritems(dict(foo='bar', baz='spam'))))

    import re
    pattern = re.compile(r'(\d{0,3}\.){1,3}(\d{0,3})$')
    match = pattern.match('1.1.1.')
    print match.group()
