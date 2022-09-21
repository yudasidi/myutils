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

def intersect(a1,b1, x1, y1, x2, y2):
    if (x1-x2) == 0:
        a2 =(y1-y2)
    else:
        a2 = (y1-y2)/(x1-x2)
    b2 = y2 - a2*x2
    xi = (b1-b2)/(a2-a1)
    yi = a1*xi+b1
    return xi, yi

def single_page(fname):
    # Get the page number
    pageNum = int(re.findall('\_(.*).xml', fname)[-1])

    xmldoc = minidom.parse(fname)
    alto = xmldoc.getElementsByTagName("alto")[0]

    lx = []
    ly = []
    rx = []
    ry = []
#    dist = []
    cnt = 0
    for textblock in alto.getElementsByTagName("TextBlock"):
        try:
            tb_width = int(textblock.attributes['WIDTH'].value)
            tb_height = int(textblock.attributes['HEIGHT'].value)
        except (KeyError):
            tb_width = 0
            tb_height = 0

        print ("TextBlock", tb_width, tb_height)
        if tb_width < 1500:
            print("Deleting a textblock", cnt)
            parent = textblock.parentNode
            parent.removeChild(textblock)
            continue

        # Calculations calculate the vertical boundaries of the column
        for tline in textblock.getElementsByTagName("TextLine"):
            print()
            cnt = cnt + 1 
            bline =  tline.attributes['BASELINE'].value
            spx = bline.split(" ")
            y1 = float(spx[0])
            x1 = float(spx[1])
            y2 = float(spx[-2])
            x2 = float(spx[-1])
            lx.append(x1)
            ly.append(y1)
            rx.append(x2)
            ry.append(y2)
#            dist.append(math.sqrt( (x1-x2)**2 + (y1-y2)**2 ))

    #################################################
    # Take only full lines
    #################################################
    lmed_y = statistics.median(ly)
    rmed_y = statistics.median(ry)

    nlx = []
    nly = []
    nrx = []
    nry = []
    for i in range(len(ly)):
        if abs(lmed_y - ly[i])<50 and abs(rmed_y -ry[i]) < 50:
            nlx.append(lx[i])
            nly.append(ly[i])
            nrx.append(rx[i])
            nry.append(ry[i])
    #################################################
    # Calculate left line and right line formulas 
    #################################################
    xnp = np.array(nlx)
    ynp = np.array(nly)
    la, lb = np.polyfit(xnp, ynp, 1)#
    plt.scatter(ynp, xnp)
    plt.plot(la*xnp+lb, xnp)

    xnp = np.array(nrx)
    ynp = np.array(nry)
    ra, rb = np.polyfit(xnp, ynp, 1)
    plt.scatter(ynp, xnp)
    plt.plot(ra*xnp+rb, xnp)
    plt.show()


    cnt = 0
    for textblock in alto.getElementsByTagName("TextBlock"):
        for tline in textblock.getElementsByTagName("TextLine"):
            cnt = cnt + 1 
            bline =  tline.attributes['BASELINE'].value
            print("line", cnt)
            print ("old", bline)
            spx = bline.split(" ")
            lpx = []
            lpy = []
            
            for i in range(0, len(spx)-2, 2):
                y1= float(spx[i])
                x1= float(spx[i+1])
                y2= float(spx[i+2])
                x2= float(spx[i+3])
                i=i+2
                if y1<x1*la+lb:
                    # First point is at the left side
                    if y2<la*x2+lb:
                        # Second point is also at the left side
                        # Discard this line
                        print("L L")
                        needNextPoint = False
                        continue
                    elif y2 > ra*x2+rb:
                        # Second point is is the right side
                        # Calculate intersection point for the first point
                        print("L R")
                        x , y = intersect(la, lb, x1, y1, x2, y2)
                        print (y, y1)
                        if abs(y-y1)<20 and y1<y:
                            lpx.append(int(x1))
                            lpy.append(int(y1))
                        else:   
                            lpx.append(int(x))
                            lpy.append(int(y))
                        # Calculate intersection point for the second point
                        x , y = intersect(ra, rb, x1, y1, x2, y2)
                        if abs(y-y2)<20 and y2>y:
                            lpx.append(int(x2))
                            lpy.append(int(y2))
                        else:
                            lpx.append(int(x))
                            lpy.append(int(y))
                        needNextPoint = False
                        break
                    else: 
                        # Second point is inside 
                        # Calculate intersection point for the first point
                        print("L I")
                        x , y = intersect(la, lb, x1, y1, x2, y2)
                        if abs(y-y1)<20 and y1<y:
                            lpx.append(int(x1))
                            lpy.append(int(y1))
                        else:
                            lpx.append(int(x))
                            lpy.append(int(y))
                        needNextPoint = True
                        continue
                elif y1<=x1*ra+rb:
                    # First point inside
                    lpx.append(int(x1))
                    lpy.append(int(y1))
                    if y2 > ra*x2+rb:
                        # Second point is at the right side
                        # Calculate intersection point for the second point
                        print("I R")
                        x , y = intersect(ra, rb, x1, y1, x2, y2)
                        if abs(y-y2)<20 and y2>y:
                            lpx.append(int(x2))
                            lpy.append(int(y2))
                        else:
                            lpx.append(int(x))
                            lpy.append(int(y))
                        needNextPoint = False
                        break
                    else:
                        # Second point is inside
                        print("I I")
                        needNextPoint = True
                        continue
                else:
                    # First point is at the right side
                    print("R R")
                    needNextPoint = False
                    break
            if needNextPoint:
                y= float(spx[-2])
                x= float(spx[-1])                
                lpx.append(int(x))
                lpy.append(int(y))

            if len(lpx) == 0:
                # Remove this textline
                print("Removing line", cnt)
                parent = tline.parentNode
                parent.removeChild(tline)
                continue
            # Change the line
            #     Make sure that there are no extra spaces !!!
            newval = ""
            for i in range(len(lpx)):
                newval = newval + str(lpy[i]) + ' ' + str(lpx[i]) + ' '
            print("new", f"@{newval[:-1]}@")  
            tline.attributes['BASELINE'].value = newval[:-1]

    # Write modified XML file
    outfile = updatedir + "/" + os.path.basename(fname)
    print(outfile)
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

