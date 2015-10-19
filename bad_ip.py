#!/usr/bin/env python
#coding=utf-8

"""读取epdimg0_access.log 文件，找出其IP不在epd.sxxl_access.log中，但是却有下载zip包的访问记录，提取该访问记录中
的IP和下载的压缩包名称"""

import re
from collections import defaultdict

download_log = r'/root/task/epdimg0_access.log'
access_log = r'/root/task/epd.sxxl_access.log'
access_ip = []
ip_zip = defaultdict(list)
get_zip = re.compile(r'GET (/.*\.zip)')

with open(access_log, 'r') as access_f:
    for line in access_f:
        ip = line.split()[0]
        # print(ip)
        access_ip.append(ip)
        

with open(download_log, 'r') as download_f:
    for line in download_f:
        if get_zip.search(line):
            zip_file = get_zip.search(line).group(1)
            ip = line.split()[0]
            ip_zip[ip].append(zip_file)
            
        
suspicious_ip = set(ip_zip.keys()) - set(access_ip)
for ip in suspicious_ip:
    # print(ip)
    result = "{0:s}:\n\t".format(ip) + "\n\t".join(ip_zip[ip])
    print(result)
