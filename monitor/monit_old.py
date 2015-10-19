#!/usr/bin/env python

from sh import ping, ErrorReturnCode
from threading import Thread

list = r'server.txt'
info = {}
recipient = '5000@sxxl.com'
servername = 'smtp.qq.com'
username = 'liding@sxxl.com'
password = ''

def alert(message, recipient):
    import smtplib
    import email.utils
    from email.mime.text import MIMEText
    
    global servername, username, password
    
    # Create the message
    msg = MIMEText('alert.')
    msg['To'] = email.utils.formataddr(('Recipient', recipient))
    msg['From'] = email.utils.formataddr(('Author', username))
    msg['Subject'] = message
    
    server = smtplib.SMTP(servername)
    try:
        server.login(username, password)
        server.sendmail(username, [recipient], msg.as_string())
    except SMTPException:
       print "Error: unable to send email"
    finally:
        server.quit()

def checker(reminder, target, method='icmp'):
    global info, recipient
    if method == 'icmp':
        try:
            ping(target, c=3)
        except ErrorReturnCode:
            message = 'server {0}: {1} is down'.format(info[target], target)
            reminder(message, recipient)


with open(list, 'r') as f:
    for line in f:
        name, ip, _  = line.split(None, 2) 
        info[ip] = name


for ip in info:
    t = Thread(target=checker, args=(alert, ip, 'icmp'))
    t.start()
