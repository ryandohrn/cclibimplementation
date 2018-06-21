import tkinter as tk
from tkinter import filedialog
import numpy as np
import pickle

root = tk.Tk()
root.withdraw()
filename = filedialog.askopenfilename()

openfile = open(filename, "r")

group = []
lines = []
datalist = []
groups = np.array([])
grabxyz = False
grabes = False
instance = 1
center = 1
countdown = 0
astcount = 0
last = 1
dataset = True

xyz = []
es = []
for line in openfile:
    line = line.replace(":", "")
    line = line.replace("f=", "")
    newline = []
    splitline = line.split()
    if countdown>0:
        countdown-=1
    elif grabxyz == True:
        for word in splitline:
            if word == "---------------------------------------------------------------------":
                grabxyz = False
                grabes = True
                astcount = 0
                break
            else:
                newline.append(word)
        else:
            xyz.append(newline)
    elif len(splitline) >= 1:
        if splitline[0] == "Excited" and splitline[1] == "State":
#            line = line.replace(":", "")
#            line = line.replace("f=", "")
            for word in splitline:
                newline.append(word)
            es.append(newline)
        elif splitline[0] == "Standard" and splitline[1] == "orientation":
            countdown = 4
            grabxyz = True
        elif grabes == True and splitline[0] == "SavETr":
            #if astcount >= 2:
                grabes = False
                tup = [xyz, es]
                datalist.append(tup)
                xyz = []
                es = []
                #else:
                #    astcount += 1
print (datalist)

#picklestring = pickle.dumps(datalist)

outfile = filedialog.asksaveasfile(mode='wb+', defaultextension='.txt')
#outfile.write(str(picklestring))
#print (xyz)
#print (es)
pickle.dump(datalist, outfile)
openfile.close()

data = []
for row in groups:
    if row[1]=="1":
        row[1]="H"
    elif row[1]=="6":
        row[1]="C"
    elif row[1]=="7":
        row[1]="N"
