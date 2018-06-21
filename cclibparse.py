import math
import cclib
from cclib.io import ccread
from tkinter import filedialog

def createobj(file):
    return ccread(file)
# filename = 'C:\\Users\\"Ryan Dohrn"\\Downloads\\two_bonds.out'

filename = filedialog.askopenfilename()

gla = [1.407, 1.314, 1.445, 1.436, 1.412, 1.426, 1.377, 1.447, 1.391, 1.403]
glb = [1.367, 1.403, 1.385, 1.420, 1.419, 1.430, 1.446, 1.431, 1.404, 1.466]

class atomref(object):
    def __init__(self, element, i, data):
        self.elem = element
        self.s = 0
        self.i = i
        self.bonds = []
        atomcoords = getattr(data, "atomcoords")
        self.optx = atomcoords[len(atomcoords)-1][i][0]
        self.opty = atomcoords[len(atomcoords)-1][i][1]
        self.optz = atomcoords[len(atomcoords)-1][i][2]
    def setref(self, s):
        self.s = s
    def bond(self, otheratom):
        self.bonds.append(otheratom)
    def distance(self, otheratom):
        x1 = self.optx
        y1 = self.opty
        z1 = self.optz
        x2 = otheratom.optx
        y2 = otheratom.opty
        z2 = otheratom.optz
        x = x2-x1
        y = y2-y1
        z = z2-z1
        xx = x**2
        yy = y**2
        zz = z**2
        d = math.sqrt(xx+yy+zz)
        return d
    def tallycarbons(self):
        c = 0
        for bond in self.bonds:
            if str(bond.elem) == "6":
                c+=1
        return c
    def nonh(self):
        b = 0
        for bond in self.bonds:
            if str(bond.elem) != "1":
                b+=1
        return b

class presort(object):
    def __init__(self, data):
        self.atoms = []
        atomnos = getattr(data, "atomnos")
        for atom in range(len(atomnos)):
            self.atoms.append(atomref(atomnos[atom], atom, data))
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
    x = 0
    sorted.addatom(n)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextnonbridge(n, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextnonbridge(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    next, prevatom = nextc(next, prevatom)
    x+=1
    sorted.addatom(next)
    print(str(x) + ": " + str(sorted.atoms[x].i))

    print("Bonds:")
    sorted.drawbonds()
    y = 0
    for bond in sorted.bonds:
        print("Bond " + str(y) + ": " + str(bond))
        y+=1
    return sorted

def mae(sorted, refbonds):
    mae = 0.0
    for b in range(len(refbonds)):
        bmae = abs(sorted.bonds[b] - refbonds[b])
        # print(str(b) + ": " + str(bmae))
        mae+=bmae
    return mae

data = ccread(filename)
p = presort(data)
s = sortmol(p)
maela = mae(s, gla)
maelb = mae(s, glb)
print("mae for La: " + str(maela))
print("mae for Lb: " + str(maelb))
# for a in p.atoms:
#     print(a.i)
#     print(a.tallycarbons())
#     for bond in a.bonds:
#         print("(" + str(a.i) + ", " + str(bond.i) + ")")
