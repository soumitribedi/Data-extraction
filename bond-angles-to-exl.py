"""

PROGRAM TO CALCULATE BOND ANGLES OF ALL LOG FILES IN THE CURRENT DIRECTORY FROM USER DEFINED ATOM NUMBERS AND WRITE IN AN EXCEL SHEET

"""
import sys
import os
import re
import math
import xlwt

from os import listdir
from os.path import isfile, join

cwd = os.getcwd()   #current working directory

onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from a address leaving out directories
at_no = [[1,6,7],[2,3,7],[5,1,4]]  #   <--------- Provide atom numbers here

#Calculate bond angles from 3 atom numbers
def get_angle(filename,A1,A2,A3):
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
	file = open(filename)
	lines = file.readlines()
	file.close()
	for j in reversed(range(len(lines))):
		if lines[j].strip()=='Standard orientation:':
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
def all_angle(filename):
	content=[]
	content.append(filename)
	for i in range(len(at_no)):
		A1 = at_no[i][0]
		A2 = at_no[i][1]
		A3 = at_no[i][2]
		content.append(get_angle(filename,A1,A2,A3))
	return content
	del content[:]

#p = all_angle("S-SPA-real-sol.log")
#print p
content2 = []
justfile = []
for x in onlyfiles[:]:
	if x[-4:] == '.log':
		justfile.append(x)
		content2.append(all_angle(x))    #Store the angles for all the files in current directory as a 2-D array
#print content2

#-------Writing in an Excel Sheet--------
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)

for i in range(0,len(justfile)):
	ind = (len(at_no))+1
	for b in range(0,ind):
		sh.write(i, b, content2[i][b])

book.save("bond-angles.xls")	
