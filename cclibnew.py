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
import cclib
from cclib.io import ccread

# filename = 'C:\\Users\\Ryan Dohrn\\Downloads\\two_bonds.out'
root = tk.Tk()
root.state('zoomed')
filename = filedialog.askopenfilename()
data = ccread(filename)
coords = getattr(data, "atomcoords")
gsenergies = getattr(data, "scfenergies")
cmenergies = getattr(data, "etenergies")
molnum = len(coords)
es = int(len(cmenergies)/molnum)
evals = []
molvars = []
xvals = []

def cmconvert(nums):
    newnums = []
    for num in nums:
        y = num * 0.0000045563
        newnums.append(y)
    return newnums
def evconvert(nums):
    newnums = []
    for num in nums:
        y = num * 0.0367493
        newnums.append(y)
    return newnums
energies = cmconvert(cmenergies)
scfvals = evconvert(gsenergies)
for n in range(es):
    evals.append([])
i = 0
for val in energies:
    e = int(i % es)
    evals[e].append(val)
    i+=1
for state in evals:
    for num in range(len(state)):
        state[num] = state[num] + scfvals[num]
for x in range(len(getattr(data, "scfenergies"))):
    xvals.append(x+1)
# for x in range(len(getattr(data, "scannames"))-1):
    # molvars.append([])
if hasattr(data, "scannames"):
    for x in range(len(getattr(data, "scannames"))-1):
        molvars.append([])
    for item in getattr(data, "scanparm"):
        lvars = list(item)
        for x in range(len(molvars)):
            if len(molvars)>0 and len(lvars)>0: molvars[x].append(lvars[x])
else:
    molvars.append([])

if len(molvars)==1: is3d = False
elif len(molvars)==2: is3d = True

fig = plt.Figure()
c = FigureCanvasTkAgg(fig, root)
c.get_tk_widget().grid(row=0, column=0, rowspan=2, columnspan=2, sticky=N+S+E+W)
if is3d:
    ax = fig.add_subplot(111, projection='3d')
    for mol in range(len(evals[0])):
        ax.scatter(molvars[0][mol], molvars[1][mol], evals[0][mol])
        # print(str(mol+1) + ": " + str(molvars[0][mol]) + ", " + str(molvars[1][mol]) + ", " + str(evals[0][mol]))
        # ax.show()
else:
    ax = fig.add_subplot(111)
    mols = []
    ax.plot(xvals, scfvals)
    for gs in range(len(scfvals)):
        ax.scatter(xvals[gs], scfvals[gs])
    for state in range(len(evals)):
        print(evals[state])
        ax.plot(xvals, evals[state])
        for mol in range(len(evals[state])):
            ax.scatter((mol+1), evals[state][mol])
c.draw()
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
