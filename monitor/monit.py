#!/usr/bin/env python

import socket
import sys
import json
import os

p = os.path.join(os.path.dirname(__file__), './')
os.chdir(p)
#sys.path.insert(0, p)

TIMEOUT = 5
confile = 'monit.json'
update = False

def tcp_ping(host, port, timeout=TIMEOUT):
    addr = (str(host), int(port))
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.settimeout(timeout)
    try:
        sc.connect(addr)
    # in python2.6, the exception is socket.error
    except  (socket.error, OSError) as msg:
        #print('Connection to {0}:{1} failed: {2}'.format(addr[0], addr[1], msg))
        return False
        
    sc.shutdown(socket.SHUT_RDWR)
    sc.close()
    return True

def send_sms(message, phones):
    from sendsms import SendMsg

    SendMsg().send(message, phones)

def send_mail(message, mail_addrs):
    from sendmail import send
    
    send(message, mail_addrs)

# parse configuration
with open(confile, 'r') as f:
    config = json.load(f)
    mail_addrs = config['mail_addrs']
    phones = config['phones']

# health check
    for target in config['targets']:
        host = target['host']
        port = target['port']
        timeout = target.get('timeout', TIMEOUT)
        if tcp_ping(host, port, timeout):
            if not target['health']:
                target['health'] = True
                update = True
                message = "FYI! {0}:{1} is OK now".format(host, port)
                send_mail(message,mail_addrs)
                send_sms(message,phones)
        else:
            if target['health']:
                target['health'] = False
                update = True
                message = "Warning! {0}:{1} is closed".format(host, port)
                send_mail(message,mail_addrs)
                send_sms(message,phones)

#from pprint import pprint
#pprint(config)
                
if update:
    with open(confile, 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ': '))
