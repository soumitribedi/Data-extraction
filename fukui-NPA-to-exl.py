#program to calculate fukui functions for particular atoms from all log files in current directory
#All neutral, cationic and anionic log files should be present in the same directory
#Cationic log files should be named "neutral_log_file_name-cat.log" similarly anionic should be "neutral_log_file_name-anion.log"
import sys,os
import xlwt

from os import listdir
from os.path import isfile, join

cwd = os.getcwd()   #current working directory

onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from a address leaving out directories
filenames=[]
content2 = []
all_log_files = []

#storing only log files in an array
for n in range(len(onlyfiles)):
	log_name = onlyfiles[n]
	if log_name[-4:] == '.log':
		all_log_files.append(onlyfiles[n])

#function to extract the NPA charges from a given log file
def print_charges(filename):
	content = []
	f = open(filename, 'r')
	t = f.readlines()
	just_file = filename[:-4]
	#content.append(str(just_file))
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
	return content


neut_files = []
cat_files = []
anion_files = []

#Storing the neutral, cationic and anionic files separately
for x in all_log_files[:]:
	justfile = x.split('.')[0]
	if justfile[-4:] == '-cat':
		cat_files.append(x)
	elif justfile[-6:] == '-anion':
		anion_files.append(x)
	else:
		neut_files.append(x)

f_plus = []
f_minus = []

at_no = [2,3,4,5,6]     #THIS STRORES THE ATOM NUMBERS WE WANT TO CALCULATE FUKUI FUNCTIONS FOR   <---- Provide atom numbers here


#function to calculate fukui functions of given atom numbers and return as an array
def calc_fukui(neut, at_no):
	F_func = []
	name = neut.split('.')[0]
	F_func.append(str(name))
	catfile = name+'-cat.log'
	anfile = name+'-anion.log'
	npa_n = print_charges(neut)
	npa_cat = print_charges(catfile)
	npa_an = print_charges(anfile)
	for i in range(len(npa_n)):
		f_plus.append(["{0:.4f}".format(float(npa_an[i][2])-float(npa_n[i][2]))])
		f_minus.append(["{0:.4f}".format(float(npa_n[i][2])-float(npa_cat[i][2]))])
	
	for i in range(len(at_no)):
		val = at_no[i]-1
		F_func.append(int(npa_n[val][1]))
		F_func.append(f_plus[val])
		F_func.append(f_minus[val])
		val = 0
	del f_plus[:]
	del f_minus[:]
	return F_func

#-------Writing in an Excel Sheet--------
book = xlwt.Workbook()
sh = book.add_sheet('Sheet1', cell_overwrite_ok=True)

for i in range(0,len(neut_files)):
	fukui_func = calc_fukui(neut_files[i],at_no)
	ind = (len(at_no)*3)+1
	for b in range(0,ind):
		sh.write(i, b, fukui_func[b])
	del fukui_func[:]

book.save("fukui-from-npa.xls")	
