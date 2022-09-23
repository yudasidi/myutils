#
#   This utility will read an XML file and write it without any modifications.
#   The created file is epected to be different than the original file.
#   This creted file can then be used for comparing with updated XML files
#
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