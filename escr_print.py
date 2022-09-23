import sys
import os
from pathlib import Path
import glob
import re
import math
import statistics
from xml.dom import minidom

def single_page(fname):
    # Get the page number
    pageNum = int(re.findall('\_(.*).xml', fname)[-1])
    fout.write(f'[{pageNum:03d}]\n')

    xmldoc = minidom.parse(fname)
    alto = xmldoc.getElementsByTagName("alto")[0]


    for textblock in alto.getElementsByTagName("TextBlock"):
        # Calculations calculate the vertical boundaries of the column
        for tline in textblock.getElementsByTagName("String"):
            text = tline.attributes['CONTENT'].value
            fout.write(text+"\n")



if len(sys.argv) != 3:
    print("Usage:")
    print(f"    python3 {sys.argv[0]} <altodir> <outfile>")
    exit()

altofiles = os.path.expandvars(sys.argv[1]) + "/*.xml"
outfile = os.path.expandvars(sys.argv[2])

flist= glob.glob(altofiles)
flist.sort()

fout = open(outfile, "w")

for fname in flist:
    single_page(fname)

