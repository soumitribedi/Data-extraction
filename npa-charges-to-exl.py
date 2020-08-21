#program to extract NPA charges from all log files in the current directory and write in excel file
import sys
import os
import re
import xlrd
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
filenames=[]
content2 = []
at_no=[2,12,13]                          #  <------------- provide atom numbers here
def print_charges(filename):
	content = []
	f = open(filename, 'r')
	t = f.readlines()
	just_file = filename[:-4]
	content2.append(str(just_file))
	for i,line in enumerate(t):
		if "Summary of Natural Population Analysis:" in line:
			index1 = i + 6
			break
	for j in range(index1, len(t)):
		if not " =======================================================================" in t[j]:
			content.append(t[j].split())
		else:
			index2 = j
			break
	for i in range(len(at_no)):
		val = at_no[i]-1
		content2.append(float(content[val][2]))
	return content2


p=[]
content3 = []
for x in onlyfiles[:]:
        if x[-4:] == '.log':
                filenames.append(x)
		just_file = x[:-4]
                p = print_charges(x)

b = 0
ind = len(at_no)+1
for i in range(len(filenames)):
	content3.append(p[b:ind])
	b=ind
	ind = ind + len(at_no) + 1
	
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)
tot = len(filenames)
#print tot
for q, l in enumerate(content3):
	ind2=len(at_no)+1
	for n in range (0,ind2):
		sh.write(q, n, l[n])
book.save("npa-charges.xls")	
