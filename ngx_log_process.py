#!/usr/bin/env python
#coding=utf-8
# author: ganluo
#regex debug https://www.debuggex.com/

import re
import fileinput


pat = re.compile((r''
    '(?P<ipaddress>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    ' - - '
    '\[(?P<datetime>\d{2}/[a-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} (?:\+|\-)\d{4})\] '
    '["](?P<method>GET|POST) '
    '(?P<url>.+)(?:http/1\.1") '
    '(?P<statuscode>\d{3}) '
    '(?P<bytessent>\d+) '
    '(["](?P<referer>-|\S+)["]) '
    '(["](?P<agent>.+)["])'), re.I)
bad_url = set()

for line in fileinput.input():
    m = pat.match(line)
    if m and '404' == m.group('statuscode'):
        method, url = m.group('method'), m.group('url')
        if (method, url) not in bad_url:
            bad_url.add((method, url))
            print('{0} {1}'.format(method, url))
