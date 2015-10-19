#!/usr/bin/env python
#coding=utf-8

# pip install suds-jurko
from suds.client import Client
from suds import WebFault

class SendMsg : 

    api_code = 'XXXX'
    login_name = 'XXXX'
    login_pwd = 'XXXX'
    dbip = 'XXXX' 
    dbport = 'XX'
    dbname = 'XX' 
    dbport = 'XX'
    dbuser = 'XX'
    dbpwd = 'XXX'

    def send(self, message, phones):
        if 0 == len(message) or 0 == len(phones):
            raise SystemExit('短信内容或发送手机为空！')
        else:
            try:
                url = "https://{ip}:{port}/axis/services/SMsg?wsdl".format(ip=self.dbip, port=self.dbport)
                client = Client(url)
                init = client.service.init(self.dbip,self.dbname, self.dbport, self.dbuser, self.dbpwd)           
                sendSM = client.service.sendSM(self.api_code,self.login_name,self.login_pwd,list(phones),message,0)
                #return ''.join(["init:",init," sendSM:",sendSM])
                return "init:{0} sendSM:{1}".format(init, sendSM)
            except WebFault as e:
                print(e)
                print("failed")
                return "error"


if '__main__' == __name__ :
    from datetime import date

    o_sms = SendMsg()
    today = date.today().strftime('%Y%m%d')
    message = u'{0} 测试--'.format(today)
    #message = 'hello'
    s = o_sms.send(message,['13714875246', '13632847730'])
    #s = o_sms.send(message,'13714875246')
    
    print(s)
