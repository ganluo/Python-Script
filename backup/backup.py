#!/usr/bin/env python
#coding=utf-8

# 此脚本用于备份各服务器上的配置文件
#
# 通过将各文件的mtime值和md5值记录存储于json文件中，检查对比文件当前的
# mtime值与已经记录的值，如果不同，进一步对比md5值，如果不同，则备份该文件，
# 然后推送到远端的备份服务器上集中存放

from datetime import datetime
import os
import subprocess
import shutil
import tarfile
import json
import sys
from socket import gethostname
import logging


def get_filelist(dir):
    files = []
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            file = os.path.join(dirpath, filename)
            files.append(file)

    return files

def md5sum(file):
    import hashlib
    m = hashlib.md5()

    with open(file, 'rb') as f:
        m.update(f.read())

    return m.hexdigest()


MAX_SIZE = 10485760
p = os.path.abspath(os.path.dirname(__file__))
update_record = False
now = datetime.today().strftime('%Y%m%d%H%M%S')
configuration = os.path.join(p, 'backup.json')


with open(configuration, 'r') as f:
    config = json.load(f)
    

#record_file = os.path.join(p, 'record.json')
record_file = config['record_file']
log_file = config['log_file']

logger = logging.getLogger('backup')
fh = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(messa'
    'ge)s', '%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)
store_dir = os.path.join(config['tmpdir'], now)

#
if os.path.exists(record_file):
    with open(record_file, 'r') as f:
        try:
            record = json.load(f)
        except ValueError:
            record = {}
else:
    record = {}


os.makedirs(store_dir)
os.chdir(store_dir)

# 将目录拓展成文件列表
files = []
for file in config['files']:
    if os.path.isfile(file):
        files.append(file)
    if os.path.isdir(file):
        files.extend(get_filelist(file))

# 生成更新文件列表
updated = []
for file in files:
    if 'exclude' in config and file.endswith(tuple(config['exclude'])):
        continue
    if os.path.getsize(file) > MAX_SIZE:
        continue
    mtime = os.path.getmtime(file)
    if file not in record:
        update_record = True
        record[file] = {}
        record[file]['mtime'] = mtime
        record[file]['md5'] = md5sum(file)
        updated.append(file)
    elif record[file]['mtime'] != mtime: 
        update_record = True
        record[file]['mtime'] = mtime
        md5 = md5sum(file)
        if record[file]['md5'] != md5:
            record[file]['md5'] = md5
            updated.append(file)

for file in updated:
    dst = file.lstrip('/')
    # 使用相对路径
    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    shutil.copy2(file, dst) 
    logger.info(u'backup {0}'.format(file))
    # 必须显式指定使用 unicode, 否则遇到中文文件名会报UnicodeEncodeError

if 0 != len(os.listdir(store_dir)):
    os.chdir(config['tmpdir'])
    tarname = '{0}.tgz'.format(now)
    t = tarfile.open(tarname, 'w:gz')
    t.add(now)
    t.close()
    
    upload = ['rsync', tarname, '/'.join([config['remote'], 
            config.get('id', gethostname())])]
    subprocess.check_call(upload, env=dict(os.environ,
        RSYNC_PASSWORD=config['rsync_pass']))
    logger.info('sync backup {0} to remote server {1}'.format(
        tarname, config['remote'].split('@')[1]))

    os.remove(tarname)

if update_record:
    with open(record_file, 'w') as f:
        json.dump(record, f)
    #    print("dumped json to file")

shutil.rmtree(store_dir)
