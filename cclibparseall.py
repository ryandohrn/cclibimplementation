import math
import cclib
from cclib.io import ccread
from tkinter import filedialog

def createobj(file):
    return ccread(file)

ggs = [1.372, 1.376, 1.363, 1.441, 1.405, 1.384, 1.411, 1.404, 1.400, 1.385]
gla = [1.407, 1.314, 1.445, 1.436, 1.412, 1.426, 1.377, 1.447, 1.391, 1.403]
glb = [1.367, 1.403, 1.385, 1.420, 1.419, 1.430, 1.446, 1.431, 1.404, 1.466]

class atomref(object):
    def __init__(self, element, i, data, mol):
        self.elem = element
        self.i = i
        self.bonds = []
        atomcoords = getattr(data, "atomcoords")
        self.optx = atomcoords[mol][i][0]
        self.opty = atomcoords[mol][i][1]
        self.optz = atomcoords[mol][i][2]
    def bond(self, otheratom):
        self.bonds.append(otheratom)
    def distance(self, otheratom):
        x = (otheratom.optx-self.optx)**2
        y = (otheratom.opty-self.opty)**2
        z = (otheratom.optz-self.optz)**2
        d = math.sqrt(x+y+z)
        return d
    def nonh(self):
        b = 0
        for bond in self.bonds:
            if str(bond.elem) != "1":
                b+=1
        return b

class presort(object):
    def __init__(self, data, mol):
        self.atoms = []
        atomnos = getattr(data, "atomnos")
        for atom in range(len(atomnos)):
            self.atoms.append(atomref(atomnos[atom], atom, data, mol))
        for atom in self.atoms:
            for a2 in self.atoms:
                if atom.distance(a2) <= 1.8 and a2.i != atom.i:
                    atom.bond(a2)
class sort(object):
    def __init__(self):
        self.atoms = []
        self.bonds = []
    def addatom(self, atom):
        self.atoms.append(atom)
    def bond(self, a1, a2):
        bondlength = a1.distance(a2)
        self.bonds.append(bondlength)
    def drawbonds(self):
        if len(self.atoms)==9:
            self.bond(self.atoms[8], self.atoms[0])
            self.bond(self.atoms[0], self.atoms[1])
            self.bond(self.atoms[1], self.atoms[2])
            self.bond(self.atoms[2], self.atoms[3])
            self.bond(self.atoms[3], self.atoms[4])
            self.bond(self.atoms[4], self.atoms[5])
            self.bond(self.atoms[5], self.atoms[6])
            self.bond(self.atoms[6], self.atoms[7])
            self.bond(self.atoms[7], self.atoms[8])
            self.bond(self.atoms[8], self.atoms[3])

def nextc(atom, prevatom):
    for bondedatom in atom.bonds:
        if str(bondedatom.elem) == "6" and bondedatom.i != prevatom:
            prevatom = atom.i
            return bondedatom, prevatom
def nextnonbridge(atom, prevatom):
    for bondedatom in atom.bonds:
        if str(bondedatom.elem) == "6" and bondedatom.i != prevatom and bondedatom.nonh() == 2:
            prevatom = atom.i
            return bondedatom, prevatom
def sortmol(presort):
    sorted = sort()
    for atom in presort.atoms:
        if str(atom.elem) == "7":
            n = atom
    prevatom = n.i
    sorted.addatom(n)
    next, prevatom = nextnonbridge(n, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextnonbridge(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    next, prevatom = nextc(next, prevatom)
    sorted.addatom(next)
    sorted.drawbonds()
    return sorted

def sortmols(data):
    mols = []
    size = len(getattr(data, "atomcoords"))
    for mol in range(size):
        p = presort(data, mol)
        s = sortmol(p)
        mols.append(s)
    return mols

def mae(sorted, refbonds):
    mae = 0.0
    for b in range(len(refbonds)):
        bmae = abs(sorted.bonds[b] - refbonds[b])
        mae+=bmae
    return mae

def ccpmae():
    filename = filedialog.askopenfilename()
    data = ccread(filename)
    all = sortmols(data)
    x = 0
    for s in all:
        print(str(x) + ": \n\tLa: " + str(mae(s, gla)) + "\n\tLb: " + str(mae(s, glb)))
        x+=1

def ccmae():
    filename = filedialog.askopenfilename()
    data = ccread(filename)
    all = sortmols(data)
    la = []
    lb = []
    for s in all:
        la.append(mae(s, gla))
        lb.append(mae(s, glb))
    return la, lb

filename = filedialog.askopenfilename()

data = ccread(filename)
all = sortmols(data)
x = 0
for s in all:
    print(str(x) + ": \n\tLa: " + str(mae(s, gla)) + "\n\tLb: " + str(mae(s, glb)) + "\n\tgs: " + str(mae(s, ggs)))
    x+=1
