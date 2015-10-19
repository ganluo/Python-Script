#!/usr/bin/env python
#coding=utf-8
#author: ganluo
#用途:此脚本用于从mysql全库备份提取单张表的备份到标准输出中
#用法:./cut_table.py tbname backup_sql_file
#example:
#   ./cut_table.py toa_user  /data/backup/mysql/oa_20150412.sql > toa_user_copy.sql

from __future__ import print_function
import sys
import re

table = sys.argv[1]
sql_file = sys.argv[2]
#target = "{table}.sql".format(table=table)

start_pat = re.compile("Table structure for table `{table}`".format(table=table))
end_pat = re.compile(r"Table structure for table `\S+`")
write = False

with open(sql_file, 'r') as s:
    for line in s:
        if not write and start_pat.search(line):
            #print(line)
            write = True
            print(line, end='')
            continue

        if write:
            if end_pat.search(line):
                break
            else:
                print(line, end='')
