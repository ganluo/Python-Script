#coding=utf-8
# 此脚本用于在修改 db 备份脚本后，将原来的备份文件根据日期分目录存放
import glob
import os
import re
import shutil

backup_prefix=r'/data/backup/mysql'
os.chdir(backup_prefix)
files=glob.glob('*201*')
pat=re.compile(r'201\d{5}')

for f in files:
    if os.path.isdir(f):
        continue
    m = pat.search(f)
    if m:
        dir = m.group()
        if not os.path.exists(dir):
            os.mkdir(dir)
        shutil.move(f, dir)
        #print("shutil.move({0}, {1})".format(f, dir))
