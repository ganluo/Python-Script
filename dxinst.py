#!/usr/bin/env python
#coding=utf-8
#author: GANLUO

from urllib import urlretrieve
import xml.etree.ElementTree as ET
import subprocess
import getpass
from glob import glob
import os
import webbrowser
import shutil

# download jar file
urls = ['http://app.diexun.com/client/mac/fushi.jar',
    'http://app.diexun.com/client/mac/shoes_sxxl.jar',
    'http://app.diexun.com/client/mac/shoes_sxxl.jar',
    'http://epd.sxxl.com/Public/login/DiexunEPD.jar',
    'http://epd.xiebaowang.com/Public/login/DiexunShoesEPD.jar']

choice = '''\
1. 服装网客户端
2. 鞋业网客户端
3. 箱包网客户端
4. 服装趋势网客户端
5. 鞋业趋势网客户端
6. 不需要下载客户端
请选择需要下载的客户端(输入对应的数字):'''

os.chdir(os.path.dirname(os.path.abspath(__file__)))

while True:
    select = raw_input(choice)
    if select in ['1', '2', '3', '4', '5', '6']:
        index = int(select) - 1
        break
    else:
        print('输入错误，请重新选择')

if 5 != index:
    fname = urls[index].rsplit('/', 1)[1]
    try:
        urlretrieve(urls[index], fname)
    except:
        if os.path.exists(fname):
            os.remove(fname)
    
    

# check if jre exists, if not, get one
jre_url = 'http://app.diexun.com/client/mac/jre.dmg'
java = '/Library/Internet Plug-Ins/JavaAppletPlugin.plugin/Contents/Home/bin/java'
cmd = [java, '-version']
if (not os.path.exists(java)) or (not subprocess.call(cmd)):
    try:
        mountpoint = '/tmp/jre'
        jre = jre_url.rsplit('/', 1)[1]
        pwd = getpass.getpass("请输入当前用户的登录密码:")
    
        urlretrieve(jre_url, jre)
    
        subprocess.check_call(['hdiutil', 'mount', '-mountpoint', mountpoint, jre])
        pkg = glob('{0}/*.pkg'.format(mountpoint))[0]
        p = subprocess.Popen(['sudo', 'installer', '-package', pkg, '-target', 
            '/'], stdin=subprocess.PIPE)
        p.communicate(pwd)
        subprocess.check_call(['hdiutil', 'unmount', mountpoint])
    except:
        if os.path.exists(jre):
            os.remove(jre)
        if os.path.isdir(mountpoint):
            subprocess.call(['umount', mountpoint])
        raise


# modify the configuration of security & privacy
confile = '/private/var/db/SystemPolicy-prefs.plist'
confile_bak = '/private/var/db/SystemPolicy-prefs.plist.bak'
shutil.copy2(confile, confile_bak)

tree = ET.parse(confile)
root = tree.getroot()
string = root.find('./dict/string')
if 'yes' == string.text:
    string.text = 'no'
    tree.write(confile)

# safari cookie setting
url = ('http://wiki.diexun.com/index.php/%E6%89%93%E5%BC%80%E5%AE%A2%E6%88%B7%E'
    '7%AB%AF%E6%98%BE%E7%A4%BA%E6%9C%AA%E7%99%BB%E5%BD%95%E7%8A%B6%E6%80%81')
reminder_file = 'diexun.txt'
reminder = '''\
如果你的缺省浏览器是safari,可能会出现使用客户端登录打开浏览器之后页面显示未登录状态
此时需要调整safari的cookie 设置,如何设置请参考{url}。或者您可以
考虑使用 chrome, firefox 等浏览器来访问我们的网站'''.format(url=url)

with open(reminder_file, 'w') as f:
    f.write(reminder)
subprocess.call(['open', '-e', reminder_file])
webbrowser.open_new_tab(url)
