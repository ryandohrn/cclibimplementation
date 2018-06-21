import tkinter as tk
from tkinter import *
from tkinter import filedialog
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.cm as cm

structurelist = []
evals = [[],[],[],[],[],[]]
fvals = [[],[],[],[],[],[]]

root = tk.Tk()
root.state('zoomed')
filename = filedialog.askopenfilename()
openfile = open(filename, "r")
root.title(filename)

class Atom(object):
    def __init__(self, centernum, atomicnum, x, y, z):
        self.centernum = centernum
        self.atomicnum = atomicnum
        self.x = x
        self.y = y
        self.z = z

class Molecule(object):
    def __init__(self, natoms):
        self.natoms = natoms
        self.atoms = []
        self.ev = []
        self.f = []
        self.bx = 0.0
        self.by = 0.0
        self.xvar = ""
        self.yvar = ""

    def addatom(self, centernum, atomicnum, x, y, z):
        self.atoms.append(Atom(centernum, atomicnum, x, y, z))
    def addvals(self, evval, fval):
        self.ev.append(evval)
        self.f.append(fval)
    def showmodel(self):
        root2 = tk.Toplevel()
        root2.withdraw()
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.axes.set_aspect('equal')
        i=0
        x = []
        y = []
        z = []
        for atom in self.atoms:
            # ax2.scatter(float(atom.x), float(atom.y), float(atom.z), marker='o')
            # ax2.text(float(atom.x), float(atom.y), float(atom.z), str(i))
            # i+=1
            x.append(float(atom.x))
            y.append(float(atom.y))
            z.append(float(atom.z))
            if atom.atomicnum == 6 or atom.atomicnum=="6": ax2.scatter(float(atom.x), float(atom.y), float(atom.z), marker='o', s=130, facecolor="#329932", label='C')
            if atom.atomicnum == 1 or atom.atomicnum=="1": ax2.scatter(float(atom.x), float(atom.y), float(atom.z), marker='o', s=130, facecolor="#00b3b3", label='H')
            if atom.atomicnum == 7 or atom.atomicnum=="7": ax2.scatter(float(atom.x), float(atom.y), float(atom.z), marker='o', s=130, facecolor="#4d4dff", label='N')
        ax2.plot([x[0], x[1], x[2], x[5], x[4], x[3], x[0]], [y[0], y[1], y[2], y[5], y[4], y[3], y[0]], [z[0], z[1], z[2], z[5], z[4], z[3], z[0]], c='teal')
        ax2.plot([x[2], x[6], x[7], x[8], x[5]], [y[2], y[6], y[7], y[8], y[5]], [z[2], z[6], z[7], z[8], z[5]], color='teal')
        ax2.plot([x[1], x[11]], [y[1], y[11]], [z[1], z[11]], color='teal')
        ax2.plot([x[6], x[14]], [y[6], y[14]], [z[6], z[14]], color='teal')
        ax2.plot([x[7], x[15]], [y[7], y[15]], [z[7], z[15]], color='teal')
        ax2.plot([x[8], x[9]], [y[8], y[9]], [z[8], z[9]], color='teal')
        ax2.plot([x[4], x[13]], [y[4], y[13]], [z[4], z[13]], color='teal')
        ax2.plot([x[3], x[12]], [y[3], y[12]], [z[3], z[12]], color='teal')
        ax2.plot([x[0], x[10]], [y[0], y[10]], [z[0], z[10]], color='teal')
        fig2.show()

def readfile():
    countdown = 0
    varcount = 0
    grabxyz = False
    grabes = False
    grabvars = False
    current = Molecule(0)
    for line in openfile:
        line = line.replace(":", "")
        line = line.replace("f=", "")
        newline = []
        splitline = line.split()
        if countdown>0:
            countdown-=1
        elif grabxyz == True:
            if len(splitline)>=1 and splitline[0] == "---------------------------------------------------------------------":
                grabxyz = False
                grabes = True
            else:
                current.addatom(splitline[0], splitline[1], splitline[3], splitline[4], splitline[5])
        elif len(splitline)>=1:
            if splitline[0] == "NAtoms=": current.natoms = splitline[1]
            elif splitline[0] == "Excited" and splitline[1] == "State":
                current.addvals(float(splitline[4]), float(splitline[8]))
                print (line)
            elif splitline[0] == "Standard" and splitline[1] == "orientation":
                countdown = 4
                grabxyz = True
            elif grabes == True and splitline[0] == "SavETr":
                grabes = False
                structurelist.append(current)
                current = Molecule(0)
            elif splitline[0] == "Summary":
                grabxyz = False
                grabes = False
                grabvars = True
                varcount = 2
            elif grabvars == True:
                print(line)
                if splitline[0] == "N":
                    for molecule in structurelist:
                        molecule.xvar = splitline[1]
                        molecule.yvar = splitline[2]
                    varcount = 1
                elif varcount == 1:
                    varcount = 0
                elif varcount == 0:
                    if splitline[0] == "----": grabvars = False
                    else:
                        print(line)
                        print(splitline[0])
                        i = int(splitline[0]) - 1
                        molecule = structurelist[i]
                        molecule.bx = float(splitline[1])
                        molecule.by = float(splitline[2])
    for mol in structurelist:
        for x in range(6):
            evals[x].append(mol.ev[x])
            fvals[x].append(mol.f[x])

def plotstate(es):
    axev.cla()
    axf.cla()
    print ("plotting state " + str(es))
    axev.set_xlabel(str(structurelist[0].xvar))
    axev.set_ylabel(str(structurelist[0].yvar))
    axev.set_zlabel("eV")
    axf.set_xlabel(str(structurelist[0].xvar))
    axf.set_ylabel(str(structurelist[0].yvar))
    axf.set_zlabel("f")
    for molecule in structurelist:
        axev.scatter(molecule.bx, molecule.by, molecule.ev[es-1], picker=5, c='teal')
        axf.scatter(molecule.bx, molecule.by, molecule.f[es-1], picker=5, c='teal')
    c1.draw()
    c2.draw()

fig1 = plt.Figure()
fig2 = plt.Figure()
c1 = FigureCanvasTkAgg(fig1, root)
c1.get_tk_widget().grid(row=0, column=0, rowspan=3, columnspan=3, sticky=N+S+E+W)
c2 = FigureCanvasTkAgg(fig2, root)
c2.get_tk_widget().grid(row=0, column=3, rowspan=3, columnspan=3, sticky=N+S+E+W)
axev = fig1.add_subplot(111, projection = '3d')
axev.axes.set_aspect('equal')
axf = fig2.add_subplot(111, projection = '3d')
axf.axes.set_aspect('equal')
for x in range(0,6):
    root.columnconfigure(x, weight=1)
    root.rowconfigure(x, weight=1)

readfile()
plotstate(1)

b1 = Button(text="View Excited State 1", command=lambda:plotstate(1))
b2 = Button(text="View Excited State 2", command=lambda:plotstate(2))
b3 = Button(text="View Excited State 3", command=lambda:plotstate(3))
b4 = Button(text="View Excited State 4", command=lambda:plotstate(4))
b5 = Button(text="View Excited State 5", command=lambda:plotstate(5))
b6 = Button(text="View Excited State 6", command=lambda:plotstate(6))
b1.grid(row=3, column=0, sticky=S)
b2.grid(row=3, column=1, sticky='s')
b3.grid(row=3, column=2, sticky='s')
b4.grid(row=3, column=3, sticky='s')
b5.grid(row=3, column=4, sticky='s')
b6.grid(row=3, column=5, sticky='s')

plt.show()
plt.draw()

def lookup(bx, by):
    for molecule in structurelist:
        if bx == molecule.bx:
            if by == molecule.by:
                return molecule

def onpick(event):
    ind = event.ind[0]
    x, y, z = event.artist._offsets3d
    print (x[ind], y[ind], z[ind])
    print (str(lookup(x[ind], y[ind]).bx) + ", " + str(lookup(x[ind], y[ind])))
    lookup(x[ind], y[ind]).showmodel()

fig1.canvas.mpl_connect('pick_event', onpick)
root.mainloop()
