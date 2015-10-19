import fnmatch
import hashlib
import os

def md5sum(file):
    m = hashlib.md5()

    with open(file, 'rb') as f:
        m.update(f.read())

    return m.digest()

def gen_find(top, filepat='*'):
    for path, dirlist, filelist in os.walk(top):
        for file in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, file)
