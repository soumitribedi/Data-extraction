#program to extract homo and lumo energies from all log files in the current directory and write in excel file
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
def homo_lumo_energies(filename):
	content = []
	f = open(filename, 'r')
	t = f.readlines()
	just_file = filename[:-4]
	content.append(str(just_file))
	for i, line in enumerate(reversed(t)):
		if "Population analysis using the SCF density." in line: 
			k1 = i
			break
	index1 = len(t)-(k1-4)
	
	for i in range(index1, len(t)):
		if "Alpha virt. eigenvalues" in t[i]:
			index2 = i
			homo_line = t[index2-1].split()
			lumo_line = t[index2].split()
			homo_e = float(homo_line[-1])
			lumo_e = float(lumo_line[4])
			content.append(homo_e)
			content.append(lumo_e)
			break
	return content

content2 = []
content3 = []
for x in onlyfiles[:]:
        if x[-4:] == '.log':
                filenames.append(x)
		just_file = x[:-4]
                content2 = homo_lumo_energies(x)
		content3.append(content2)
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)
for p, q in enumerate(content3):
	for n in range(0,3):
		sh.write(p, n, q[n])

book.save("homo-lumo.xls")	
