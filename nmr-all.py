"""
This program operates on all log files in the current directory.
It extracts the NMR and writes to an excel sheet
"""
import sys
import os
import re
import xlrd
import math
import os.path
import unicodedata
import subprocess
import shutil
import xlwt

from subprocess import call
from os import listdir
from os.path import isfile, join

cwd = os.getcwd()   #current working directory

onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from a address leaving out directories

files_list = []

for n in range(len(onlyfiles)):
	file_name = onlyfiles[n]
	if file_name[-4:] == '.log':
		files_list.append(onlyfiles[n])         #files_list contains all log files in the cwd

NMR=[]
C=196.7364
H=31.8627
N=-161.7867

# Comment out the atom you don't need
relevant_C=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
#relevant_H=[8]
#relevant_N=[1]
relevant_O=[15,16]

###         Function to get the isotropic value of a particular list of atoms
def get_nmr(filename,relevant_C,relevant_O):
	file = open(filename)
	lines = file.readlines()
	file.close()
	NMR.append(str(filename[:7]))
	for i, line in enumerate(lines):
		if 'Eigenvalues:' in line:
			(no,type,x,x,val,x,x,x) = lines[i-4].split()
			if (int(no) in relevant_C) or (int(no) in relevant_O):
				NMR.append(float(val))

	return NMR

p=[]
content3 = []
just_file = []
for x in files_list[:]:
	just_file.append(x[:-4])
        p = get_nmr(x,relevant_C,relevant_O)

b = 0
ind = 16+1                                #<-------- the 16 indicates the number of values. In this case it was 14 carbon and 2 Oxygen
for i in range(len(files_list)):
	content3.append(p[b:ind])
	b=ind
	ind = ind + 16 + 1                  #<-------- the 16 indicates the number of values. In this case it was 14 carbon and 2 Oxygen

book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)
tot = len(files_list)
#print tot
for q, l in enumerate(content3):
	ind2=16+1              #<-------- the 16 indicates the number of values. In this case it was 14 carbon and 2 Oxygen        
	for n in range (0,ind2):
		sh.write(q, n, l[n])
book.save("nmr-all.xls")	

