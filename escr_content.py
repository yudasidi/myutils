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
 
    xmldoc = minidom.parse(fname)
    alto = xmldoc.getElementsByTagName("alto")[0]


    for textblock in alto.getElementsByTagName("TextBlock"):
        # Calculations calculate the vertical boundaries of the column
        for tline in textblock.getElementsByTagName("String"):
            text = tline.attributes['CONTENT'].value
 
            text = text.replace("ב\"", "ב\'")   
            text = text.replace("ג\"", "ג\'")
            text = text.replace("ז\"", "ז\'")
            text = text.replace("ש\"", "ש\'")

            tline.attributes['CONTENT'].value = text
    # Write modified XML file
    outfile = updatedir + "/" + os.path.basename(fname)
    with open(outfile, "w") as fsxml:
        fsxml.write(xmldoc.toxml())
        fsxml.close()


if len(sys.argv) != 3:
    print("Usage:")
    print(f"    python3 {sys.argv[0]} <altodir> <updatedir>")
    exit()

altofiles = os.path.expandvars(sys.argv[1]) + "/*.xml"
updatedir = os.path.expandvars(sys.argv[2])

flist= glob.glob(altofiles)
flist.sort()

for fname in flist:
    single_page(fname)
