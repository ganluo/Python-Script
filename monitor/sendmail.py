#!/usr/bin/env python
#coding=utf-8

#author: ganluo
#purpose: 调用该脚本发邮件
#usage: notify.py message  recipient1 [ recipient2 ...]

from __future__ import print_function

servername = 'smtp.qq.com'
username = 'it@example.com'
password = 'XXXX'

def send(message, recipient):
    import smtplib
    import email.utils
    from email.mime.text import MIMEText

    global servername, username, password

    # Create the message
    msg = MIMEText(' 如题 ...', 'plain', 'utf-8')
    msg['To'] = ", ".join(recipient)
    msg['From'] = username
    msg['Subject'] = message

    server = smtplib.SMTP(servername)
    try:
        server.login(username, password)
        server.sendmail(username, recipient, msg.as_string())
    finally:
        server.quit()

if '__main__' == __name__ :
    import sys
    notify(sys.argv[1], * sys.argv[2:])
