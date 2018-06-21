# -*- coding: utf-8 -*-

import re
import sys
import glob
import os

root_numberRegex = re.compile(r'''
    root=           #beginning of root number appearance
    (\d*)           #GROUP 1: root number
    ''', re.VERBOSE)

#All the regular expressions needed to get indole bond lengths from Gaussian optimization calculation (using Justin's numbering convetion)
r45regex = re.compile(r"!\s*R8\s*R\(4,5\)\s*(\d+\.\d+)")
r56regex = re.compile(r"!\s*R10\s*R\(5,6\)\s*(\d+\.\d+)")
r16regex = re.compile(r"!\s*R2\s*R\(1,6\)\s*(\d+\.\d+)")
r12regex = re.compile(r"!\s*R1\s*R\(1,2\)\s*(\d+\.\d+)")
r23regex = re.compile(r"!\s*R4\s*R\(2,3\)\s*(\d+\.\d+)")
r34regex = re.compile(r"!\s*R6\s*R\(3,4\)\s*(\d+\.\d+)")
r17regex = re.compile(r"!\s*R3\s*R\(1,7\)\s*(\d+\.\d+)")
r78regex = re.compile(r"!\s*R13\s*R\(7.8\)\s*(\d+\.\d+)")
r816regex = re.compile(r"!\s*R16\s*R\(8,16\)\s*(\d+\.\d+)")
r216regex = re.compile(r"!\s*R5\s*R\(2,16\)\s*(\d+\.\d+)")

#Defining the built in structures for this script, particularly the reference structures from the 2011 Guissani paper
keys = ['r45', 'r56', 'r16', 'r12', 'r23', 'r34', 'r17', 'r78', 'r816', 'r216']
guissaniGS = [ 1.411,  1.384,  1.405, 1.404, 1.400, 1.385, 1.441,  1.363,  1.376, 1.372]
guissaniLa = [ 1.377,  1.426, 1.412, 1.403, 1.391,  1.447,  1.436,  1.445,  1.314, 1.407]
guissaniLb = [ 1.446, 1.430, 1.419, 1.466, 1.404, 1.431, 1.420, 1.385, 1.403, 1.367]
justinGS = [ 1.405, 1.383, 1.401, 1.419, 1.394, 1.384, 1.433, 1.365, 1.379, 1.376]
justinroot1 = [1.406, 1.42, 1.398, 1.446, 1.412, 1.406, 1.431, 1.356, 1.408, 1.34]
justinroot2 = [1.373, 1.409, 1.431, 1.416, 1.372, 1.452, 1.389, 1.423, 1.341, 1.391]
zero = [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.]

#Now officially make the molecular structures, stored as python dictionaries using the bond labels as keys
guissaniGS = dict(zip(keys,guissaniGS))
guissaniLa = dict(zip(keys,guissaniLa))
guissaniLb = dict(zip(keys,guissaniLb))
zero = dict(zip(keys,zero)) 
justinGS = dict(zip(keys,justinGS))
justinroot1 = dict(zip(keys,justinroot1))
justinroot2 = dict(zip(keys, justinroot2))

# simple function to compare one molecule to another and calculate sum of the absolute errors
def compare(mol1, mol2):
    mae = 0.0
    for (key1, val1), (key2, val2) in zip(mol1.items(), mol2.items()):
        mae += abs(val1-val2)
    #print "comparison made! mae = %f" % mae
    return mae



#the parameter line is the first that begins with " #", so it searches for that line
def find_parameters(file_handle):
    file_handle.seek(0)
    for l in file_handle:
        if l.startswith(" #"):
            return l.rstrip()

#**********************************BEGIN CODE******************************
folder_location = os.getcwd()

#gets filepaths for everything in the specified folder ending with .out
search_str_out = folder_location + "/" + "*.out"
file_paths = glob.glob(search_str_out)
file_paths = sorted(file_paths)
print(file_paths)

#loop through the files again to get all the relevant results
for file_name in file_paths:
    #open file to use in python
    current_file = open(file_name)
    #reads the file as a list of its lines of text
    content = current_file.read()

    #get the route lrameters.*?D1",content,re.DOTALL)ine; skip to next file if there is no route line
    parameters=str(find_parameters(current_file))
    if parameters=="None":   #skip over any output files that don't have a route line
        continue

    #get the method and basis set of the calculation
    #(using sneaky string slicing)
    slash_pos = parameters.find("/")
    space_pos = parameters.find(" ",slash_pos)
    close_paren_pos = parameters.find(")")
    if "geom=connectivity" in parameters:
        basis = parameters[slash_pos+1:space_pos]
    else:
        basis = parameters[slash_pos+1:]

    method = parameters[close_paren_pos+2:slash_pos]

    root_number = root_numberRegex.search(parameters)
    #if root_number!=None:
    #    root_number = root_number.group(1)
    #else:
    #    root_number = "0"
    root_number = root_number.group(1) if root_number != None else "0" 
    #Now look for the optimized geometry in the Gaussian output (at end of file)
    opt_param = re.findall("  Optimized Parameters.*?D1",content,re.DOTALL)
    if opt_param==[]:    #skip over any output files that don't have an optimized geometry
        continue
    else:
        opt_param = re.findall("  Optimized Parameters.*?D1",content,re.DOTALL)[0]

    #defines the molecule bond lengths from all the relevant regular expression matches, converts string to float, and then forms dictionary
    molecule = [r45regex.search(opt_param).group(1),
                r56regex.search(opt_param).group(1),
                r16regex.search(opt_param).group(1),
                r12regex.search(opt_param).group(1),
                r23regex.search(opt_param).group(1),
                r34regex.search(opt_param).group(1),
                r17regex.search(opt_param).group(1),
                r78regex.search(opt_param).group(1),
                r816regex.search(opt_param).group(1),
                r216regex.search(opt_param).group(1),
                ]
    molecule = [float(x) for x in molecule]
    molecule = dict(zip(keys,molecule))

    #Now look for the last dipole moment in the file (that of the optimum geometry and the state specified by root=)
    # if there is no excited state dipole printed (if it wasn't requested) then use NONE
    #dipole = "NONE"
    #if parameters.find("density") > 0:
    dipole = re.findall("Dipole moment.*?Quadrupole moment", content, re.DOTALL)[-1]  #get the last match in the file for optimized geometry
    dipoleregex = re.compile(r"Tot=\s*(\d+\.\d+)")
    dipole = dipoleregex.search(dipole).group(1)
    
    #Compare the optmized structure to the reference structures
    maeLa = compare(molecule, guissaniLa)
    maeLb = compare(molecule, guissaniLb)
    winner = "La" if maeLa < maeLb else "Lb"
    print("indole %s/%s with root=%s, opt structure closest to %s (maeLa=%f, maeLb=%f) dipole=%s" % (method, basis, root_number, winner, maeLa, maeLb, dipole))
    current_file.close()


#compare(guissaniGS, justinGS)
#compare(guissaniLa, justinroot1)
#compare(guissaniLa, justinroot2)
#compare(guissaniLb, justinroot1)
#mae = compare(guissaniLb, guissaniLa)
#print mae
