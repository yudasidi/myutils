import sys
import os
from pathlib import Path
import glob
import re
import math
import statistics
from xml.dom import minidom
import numpy as np
import matplotlib.pyplot as plt

def single_page(fname):
    # Get the page number
    pageNum = int(re.findall('\_(.*).xml', fname)[-1])

    xmldoc = minidom.parse(fname)
      
    # Write modified XML file
    with open(os.path.basename(fname), "w") as fsxml:
        fsxml.write(xmldoc.toxml())
        fsxml.close()


if len(sys.argv) != 3:
    print("Usage:")
    print(f"    python3 {sys.argv[0]} <altodir> <outfile>")
    exit()

altodir = sys.argv[1]+"/*.xml"
outputfile = Path(sys.argv[2])

flist= glob.glob(altodir)
flist.sort()
fout = open(outputfile, "w")
for fname in flist:
    single_page(fname)
fout.close() 
