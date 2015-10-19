import crypt
import sys
import base64
import os

passwd = sys.argv[1]

encrypted_passwd = crypt.crypt('passwd', '$6$' + base64.b64encode(os.urandom(6)))
print(encrypted_passwd)
