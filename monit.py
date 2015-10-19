#!/usr/bin/env python

from sh import ping, ErrorReturnCode

list = r'server.txt'
info = {}
recipient = '5000@sxxl.com'

def alert(message, recipient):
    import smtplib
    import email.utils
    from email.mime.text import MIMEText

    servername = 'smtp.qq.com'
    username = 'xx@sxxl.com'
    password = ''

    # Create the message
    msg = MIMEText('alert.')
    msg['To'] = email.utils.formataddr(('Recipient', recipient))
    msg['From'] = email.utils.formataddr(('Author', username))
    msg['Subject'] = message

    server = smtplib.SMTP(servername)
    try:
        server.login(username, password)
        server.sendmail(username, [recipient], msg.as_string())
    finally:
        server.quit()


with open(list, 'r') as f:
    for line in f:
        name, ip, _  = line.split(None, 2)
        info[name] = ip

for name, ip in info.iteritems():
    try: ping(ip, c = 3)
    except ErrorReturnCode:
        message = 'server {0}: {1} is down'.format(name, ip)
        alert(message, recipient)
    '''
    else:
        print('server {0} is ok !'.format(name))
    '''

'''
#cat server.txt
call_server     192.168.2.10  ping
record_server   192.168.2.11  80
attend_server   192.168.2.12  4370
Xen_server      192.168.2.14  ping
RTX_server      192.168.2.18  8012
Ipguard_server  192.168.2.19  8237
cloth1_server   192.168.2.31  138,139,445
cloth2_server   192.168.2.32  138,139,445
shoes_server    192.168.2.33  138,139,445
'''
