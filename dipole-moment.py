#program to extract dipole moment from all log files in the current directory and write in excel file
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
content = []
def dipole_moment(filename):
	content = []
	f = open(filename, 'r')
	t = f.readlines()
	just_file = filename[:-4]
	content.append(str(just_file))
	for i, line in enumerate(reversed(t)):
		if "Dipole moment (field-independent basis, Debye):" in line:
			k1 = i
			break
	index1 = len(t)-k1
	line1 = t[index1]
	(a,a,a,a,a,a,a,val) = line1.split()
	content.append(float(val))
	return content

#c = dipole_moment("L66.log")
#print c


content2 = []
content3 = []
for x in onlyfiles[:]:
        if x[-4:] == '.log':
                filenames.append(x)
		just_file = x[:-4]
                content2 = dipole_moment(x)
		content3.append(content2)
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)
for p, q in enumerate(content3):
	for n in range(0,2):
		sh.write(p, n, q[n])

book.save("dipole-moment.xls")	

