import sys
from pathlib import Path
import re


punct =  "-.,:;?\")" 
chars1 = "\"אבגדהוזחטיכלמנסעפצקרשת"
chars2 = "ךםןףץ'"
chars3 = "כמנפצ"
pb = "ב\'"
pg = "ג\'"
pz = "ז\'"
pp = "פ\'"
p = re.compile(f"^({pb}|{pg}|{pz}|{pp}|[{chars1}])+[{chars2}]?$")



if len(sys.argv) != 4:
    print("Usage:")
    print(f"    python3 {sys.argv[0]} <textfile> <wordfile> <outfile>")
    exit()

inputfile = Path(sys.argv[1])
dictfile = Path(sys.argv[2])
outputfile = Path(sys.argv[3])

class dict:
    def __init__(self, dictfile):
        self.dict = {}
        with open(dictfile, 'r', encoding='utf-8-sig') as fdict:
            for line in fdict.readlines():
                list = line.split(",")
                for i in range(2):
                    # Word has quotation marks
                    word=list[i]
                    if word[0:1] == "\"":
                        # Remove the start and end quotation marks
                        word = word[1:-1]
                        # Find two consecutive quotation marks and remove one of them
                        word = word.replace("\"\"", "\"")
                        list[i] =word
                    list[i] =list[i].strip()
                if list[1] != "":
                    self.dict[list[0]] = (list[1], list[2])
#                    print(f"#{list[0]}# , #{list[1]}#")

    def look(self,key):
        try:
            return self.dict[key]
        except KeyError:
            return ("?", "?")

fout = open(outputfile, "w") 

lad_dict = dict(dictfile)

with open(inputfile, 'r', encoding='utf-8-sig') as fin:
    leftover=""
    count = 0
    for line in fin.readlines():  # Read line by line in txt file
        count = count + 1
        line = line.strip()
        # If line begins with "[" remove the word.
        # This is page number field
        if line == "":
            fout.write(line)
            fout.write("\n")
            continue
        if line[0:1] == "[":
            fout.write(line)
            fout.write("\n")
            continue       
        line = leftover + line
        leftover = ""
        linelist = []
        for word in line.split():  # Read word by word in each line
            try:
                # Replace all  "'ש" replace with "ש"
                word = word.replace("ש\'", "ש")
         
                # If word starts with quotation mark remove it
                if word[0:1] == "\"":
                    word = word[1:]
                    fout.write("\"")
                elif word[0:1] == "(":
                    word = word[1:]
                    fout.write("(")

                # If word ends with hyphen leave the word in leftover
                if word != "-" and (word[-1] == "-" or word[-1] == "⸗" or word[-1] == "־") :
                    leftover = word[0:-1]
                    continue
                # If word ends with one or two punctuation mark(s) remove the punctuation mark(s)
                pm = ""
                for i in range(2):
                    last = word[-1]
                    if last in punct:
                        word = word[0:-1]
                        pm = pm + last    
            
                res = lad_dict.look(word)
                if res[0] == "?":
                    fout.write(word)
                else:
                    if res[1] == "H":
                        fout.write("$")
                    elif res[1] == "T":
                        fout.write("&")
                    fout.write(res[0])
                    if res[1] == "H":
                        fout.write("$")
                    elif res[1] == "T":
                        fout.write("&")
                fout.write(pm)
                fout.write(" ")
                continue
            except IndexError:
                res = lad_dict.look(word)
                if res[0] == "?":
                    fout.write(word)
                else:
                    fout.write(res[0])
                fout.write(pm)
                fout.write(" ")
                continue
        fout.write("\n")

fout.close()      