import os
from pprint import pprint

top = 'local'
files = []

for dirpath, dirnames, filenames in os.walk(top):
    for filename in filenames:
        #print(dirpath)
        file = os.path.join(dirpath, filename)
        #print(file)
        files.append(file)

#pprint(files)
