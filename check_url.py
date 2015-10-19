#!/usr/bin/env python
#coding=utf-8

import sys
import re
from subprocess import call

check_http = "/usr/lib/zabbix/externalscripts/check_http"
ip = sys.argv[1]
url = sys.argv[2]
reg = sys.argv[3]
pat = re.compile(r'http://(.*\.com)(/.*)?$')
#group                    1
vhost = pat.search(url).group(1)

cmd = [check_http, '--timeout=15', '-f', 'follow', '-H', vhost, '-I', ip, '-u',
    url, '-r', reg]
call(cmd, stdout=sys.stdout)
