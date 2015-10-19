#!/usr/bin/env python
#coding=utf-8
# 此脚本用于删除某个目录下的重复文件,将冗余的文件替换为软链接

import os.path
import shell

top = '/tmp/test'
md5_to_file = {}
files = shell.gen_find(top)

for file in files:
    if os.path.islink(file):
        continue
    md5 = shell.md5sum(file)
    if md5 in md5_to_file:
        file_reserv = md5_to_file[md5]
        relpath = os.path.relpath(file_reserv, os.path.dirname(file))
        print('os.remove({0})'.format(file))
        os.remove(file)
        print('os.symlink({0}, {1})'.format(relpath, file))
        os.symlink(relpath, file)
    else:
        md5_to_file[md5] = file


#for file_list in md5_to_file.itervalues():
#    file_reserv = file_list[0]
#    file_to_link = file_list[1:]
#    for file in file_to_link:
#        print('os.remove({0})'.format(file))
#        os.remove(file)
#        relpath = os.path.relpath(file_reserv, os.path.dirname(file))
#        print('os.symlink({0}, {1})'.format(relpath, file))
#        os.symlink(relpath, file)
