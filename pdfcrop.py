#coding=utf-8
# Usage: C:\Python34\python.exe .\pdfcrop.py .\faq.pdf newfaq.pdf -p '0,2-83'

from PyPDF2 import PdfFileWriter, PdfFileReader
import argparse
from itertools import islice
import re

parser = argparse.ArgumentParser()
parser.add_argument('infile',  help='original pdf file')
parser.add_argument('outfile', help='output pdf file')
parser.add_argument('-p', '--pages', dest='pages',
    help='pages need to dump out from the original pdf file, ie: 3-25,78')
args = parser.parse_args()

class ParseError(Exception):
    pass


pages = args.pages.split(',')
range_pat = re.compile(r'^(\d+)(-(\d+))?$', re.VERBOSE)
# group                   1    2 3
scope = []
for i in pages:
    m = range_pat.match(i)
    if not m:
        raise ParseError(i)
    elif m.group(3):
        i = slice(int(m.group(1)), int(m.group(3)))
    else:
        start = int(m.group(1))
        i = slice(start, start+1)
    scope.append(i)

with open(args.infile, 'rb') as s, open(args.outfile, 'wb') as d:
    pdfin = PdfFileReader(s)
    pdfout = PdfFileWriter()

    for i in scope:
        for page in islice(pdfin.pages, i.start, i.stop, i.step):
            pdfout.addPage(page)
    pdfout.write(d)
