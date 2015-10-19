#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function
import sys
import re
from os.path import basename, join
from os import walk

top_dir = sys.argv[1]
ip_pat = re.compile(r'192\.168\.3\.(61|10)')
fname_pat = re.compile(r'[a-zA-Z_]{1,15}\.(php|conf|config)')
dirname_pat = re.compile('\d+')
#suffix = ('.php', '.conf', '.config')

def check_file(file):
    with open(file, 'r') as f:
        for line in f:
            if ip_pat.search(line):
                print(file)
                break


for root, dirs, files in walk(top_dir):
    for file in files:
        if fname_pat.match(file):
            check_file(join(root,file))
    for dir in dirs:
        if dirname_pat.search(dir):
            dirs.remove(dir)
