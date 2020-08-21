"""

PROGRAM TO CALCULATE BOND LENGTHS OF ALL LOG FILES IN THE CURRENT DIRECTORY FROM USER DEFINED ATOM NUMBERS AND WRITE IN AN EXCEL SHEET

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
at_no = [[1,6],[2,3],[5,1]]  #   <--------- Provide atom numbers here

#Calculate bond lengths from 2 atom numbers
def get_length(filename,L1,L2):
	x1 = 0
	x2 = 0
	y1 = 0
	y2 = 0
	z1 = 0
	z2 = 0
	length = 0
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
def all_length(filename):
	content=[]
	content.append(filename)
	for i in range(len(at_no)):
		L1 = at_no[i][0]
		L2 = at_no[i][1]
		content.append(get_length(filename,L1,L2))
	return content
	del content[:]

#p = all_length("S-SPA-real-sol.log")
#print p

content2 = []
justfile = []
for x in onlyfiles[:]:
	if x[-4:] == '.log':
		justfile.append(x)
		content2.append(all_length(x))    #Store the angles for all the files in current directory as a 2-D array
#print content2

#-------Writing in an Excel Sheet--------
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)

for i in range(0,len(justfile)):
	ind = (len(at_no))+1
	for b in range(0,ind):
		sh.write(i, b, content2[i][b])

book.save("bond-lengths.xls")	

