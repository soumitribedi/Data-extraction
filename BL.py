"""""""""""""""""""""""""""""""""

PROGRAM TO CALCULATE BOND LENGTHS
OF ALL LOG FILES IN A DIRECTORY
FROM USER DEFINED ATOM NUMBERS
AND WRITE IN AN EXCEL SHEET

"""""""""""""""""""""""""""""""""
import sys
import glob
import os
import re
import math

#Calculate bond lengths from 2 atom numbers
def get_length(address,filename,L1,L2):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    z1 = 0
    z2 = 0
    length = 0
    start = 0
    end = 0
    file = open(os.path.join(address,filename),'r')
    lines = file.readlines()
    file.close()
    for j in reversed(range(len(lines))):
        if lines[j].strip()=='Input orientation:' or lines[j].strip()=='Standard orientation:':
	    start=j+1
	    break

    for j in range(start+4,len(lines)):
	if lines[j].strip()=='---------------------------------------------------------------------':
	    end=j+1
	    break

    NA = end-start-5
    for i in range(start+4,end-1):
    	j=i-start-3
	(no,type,o,x,y,z) = lines[i].split()
    	if j == L1:
            x1=float(x)
            y1=float(y)
            z1=float(z)
        if j == L2:
            x2=float(x)
            y2=float(y)
            z2=float(z)
    a1=(y1-y2)*(y1-y2)
    b1=(x1-x2)*(x1-x2)
    c1=(z1-z2)*(z1-z2)
    length = math.sqrt(a1+b1+c1)
    return length

#calculate bond lengths for all the atom numbers provided in variable 'at_no' in groups of two
def length_all_atom(address,filename,at_no):
    content=[]
    #content.append(filename)
    for i in range(len(at_no)):
	L1 = at_no[i][0]
	L2 = at_no[i][1]
	content.append(get_length(address,filename,L1,L2))
    return content
    del content[:]


def BL_list(address,file_list,atom_list):
    content2 = []
    
    for x in file_list[:]:
        content2.append(length_all_atom(address,x,atom_list))
    return content2

