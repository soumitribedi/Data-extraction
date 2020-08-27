"""""""""""""""""""""""""""""""""

PROGRAM TO CALCULATE BOND ANGLES
OF ALL LOG FILES IN A DIRECTORY
FROM USER DEFINED ATOM NUMBERS
AND WRITE IN AN EXCEL SHEET

"""""""""""""""""""""""""""""""""
import sys
import os
import re
import math

#Calculate bond angles from 3 atom numbers
def get_angle(address,filename,A1,A2,A3):
    x1 = 0
    x2 = 0
    x3 = 0
    y1 = 0
    y2 = 0
    y3 = 0
    z1 = 0
    z2 = 0
    z3 = 0
    angle = 0
    start = 0
    end = 0
    file = open(os.path.join(address,filename),'r')
    lines = file.readlines()
    file.close()
    for j in reversed(range(len(lines))):
	if lines[j].strip()=='Standard orientation:' or lines[j].strip()=='Input orientation:':
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
	if j == A1:
	    x1=float(x)
            y1=float(y)
            z1=float(z)
        if j == A2:
            x2=float(x)
            y2=float(y)
            z2=float(z)
        if j == A3:
            x3=float(x)
            y3=float(y)
            z3=float(z)
    a1=(y1-y2)*(y1-y2)+(x1-x2)*(x1-x2)+(z1-z2)*(z1-z2)
    b1=(z3-z2)*(z3-z2)+(x3-x2)*(x3-x2)+(y3-y2)*(y3-y2)
    c1=math.sqrt(a1)
    d1=math.sqrt(b1)
    e1=(x1-x2)*(x3-x2)+(y1-y2)*(y3-y2)+(z1-z2)*(z3-z2)
    angle= math.degrees(math.acos((e1)/((c1)*(d1))))
    return angle

#calculate bond angles for all the atom numbers provided in variable 'at_no' in groups of three
def angle_all_atom(address,filename,at_no):
    content=[]
    #content.append(filename)
    for i in range(len(at_no)):
        A1 = at_no[i][0]
        A2 = at_no[i][1]
	A3 = at_no[i][2]
	content.append(get_angle(address,filename,A1,A2,A3))
    return content
    del content[:]

def Angle_list(address,file_list,atom_list):
    content2 = []
    
    for x in file_list[:]:
        content2.append(angle_all_atom(address,x,atom_list))
    return content2
