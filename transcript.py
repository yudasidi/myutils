import sys
from pathlib import Path
import re

comment_markers = "*"
punct =  "-.,:;?\")" 
chars1 = "\"אבגדהוזחטיכלמנסעפצקרשת"
chars2 = "ךםןףץ'"
chars3 = "כמנפצ"
pb = "ב\'"
pg = "ג\'"
pz = "ז\'"
pp = "פ\'"
p = re.compile(f"^({pb}|{pg}|{pz}|{pp}|[{chars1}])+[{chars2}]?$")

class dict:
    def __init__(self, dictfile):
        self.dict = {}
        with open(dictfile, 'r', encoding='utf-8-sig') as fdict:
            for line in fdict.readlines():
                line = line.strip()
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
#                    print(f"#{list[0]}# , #{list[1]}#, #{list[2]}#")

    def look(self,key):
        try:
            return self.dict[key]
        except KeyError:
            return ("?", "?")

##EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE



def handle_word(pm, word):
    word_d = word.replace("ש\'", "X")
    if "ס" in word_d and "ש" in word_d:
        fout.write("@")   
    word_d = word_d.replace("ש", "ס")
    word_d = word_d.replace("X", "ש")
 
    res = lad_dict.look(word_d)    # A ladino word 
    res_h = lad_dict.look(word)     # Unchanged word probably a hebrew word where ש should not be replaced by ס
 
    if res[0] == "?" and res_h[0] == "?":
        if word == word_d:
            fdict.write(word + "\n")
        else:
            fdict.write(word + " " + word_d + "\n")
        fout.write(word)     
    elif res[0] == "?":
        res = res_h     
    if res[0] != "?":
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
##EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE


if len(sys.argv) != 4:
    print("Usage:")
    print(f"    python3 {sys.argv[0]} <textfile> <wordfile> <outfile>")
    exit()

inputfile = Path(sys.argv[1])
dictfile = Path(sys.argv[2])
outputfile = Path(sys.argv[3])

fout = open(outputfile, "w") 
fdict = open("newwords.txt", "w")
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
                # If word starts with quotation mark remove it
                if word[0:1] == "\"":
                    word = word[1:]
                    fout.write("\"")
                elif word[0:1] == "(":
                    word = word[1:]
                    fout.write("(")
 
                # We don't need comment markers in Latin text
                if word[0] in comment_markers:
                    word = word[1:]


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

                handle_word(pm, word)
                continue
            except IndexError:
                handle_word(pm, word)
                continue
        fout.write("\n")
fdict.close()
fout.close()