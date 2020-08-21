#program to accept all logfiles from dest1 and create cationic and anionic input files for single point along with the script files in dest2
#EXECUTE FROM DEST1
import sys
import os
import re
import os.path
import unicodedata
import subprocess
import shutil

from subprocess import call
from os import listdir
from os.path import isfile, join

#cwd = os.getcwd()
dest1 = '/users/PAS0925/osu1342/9/electrophilic/successfulfiles'
dest2 = '/users/PAS0925/osu1342/9/electrophilic/fukui'
onlyfiles = [f for f in listdir(dest1) if isfile(join(dest1, f))] #will extract only files from dest1
#onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from a address leaving out directories
neut_log_files = []
neut_files_name = []
for n in range(len(onlyfiles)):
	log_name = onlyfiles[n]
	if log_name[-4:] == '.log':
		neut_log_files.append(onlyfiles[n])

print neut_log_files

def extract_coordinate(neut_file_log):	
	coordinates = []
	file = open(neut_file_log)
	print neut_file_log 
	lines = file.readlines()
	file.close()
	for i, line in enumerate(reversed(lines)):
		if 'Input orientation:' in line:
			k = i
			break
	index1 = len(lines)-(k - 4)
	
	for i in range(index1, len(lines)):
		if ' ---------------------------------------------------------------------' in lines[i]:
			index2 = i
			break
	for i in range(index1, index2):
		(a, atno, a, x, y, z) = lines[i].split()
		coord = atno + " " + x + " " + y + " " + z
		coordinates.append(coord)
	return coordinates	

def make_script(file_name):		
	file_script=file_name
	file2 = open(file_script,'w+')
	file2.close()
	content2=[]
	content2.append('#PBS -S /bin/tcsh'+'\n')
	content2.append('#PBS -N '+file_script+'\n')
	content2.append('#PBS -o '+file_script+'.log'+'\n')
	content2.append('#PBS -A PAA0001'+'\n')
	content2.append('#PBS -l walltime=02:00:00'+'\n')
	content2.append('#PBS -l nodes=1:ppn=28'+'\n')
	content2.append('#PBS -l pmem=4GB'+'\n'+'\n')
	content2.append('#set echo'+'\n')
	content2.append('###cd $TMPDIR'+'\n')
	content2.append('cd $PBS_O_WORKDIR'+'\n')
	content2.append('pwd'+'\n')
	content2.append('set INPUT='+file_script+'.com'+'\n')
	content2.append('# PBS_O_WORKDIR refers to the directory from which the job was submitted.'+'\n')
	content2.append('##cp $PBS_O_WORKDIR/$INPUT .'+'\n')
	content2.append('module load gaussian/g09e01'+'\n')
	content2.append('g09< ./$INPUT'+'\n')
	content2.append('###ls -al'+'\n')
	content2.append('###cp *.chk $PBS_O_WORKDIR'+'\n')
	content2.append('###cp *.log $PBS_O_WORKDIR'+'\n'+'\n')
	data2=open(file_script,'w+')
	for line in content2:
		out=line
		data2.write(out)
	data2.close()
	del content2[:]
	shutil.move(file_script, dest2)

content = []
def create_cat(neut_file_log):
	c = []
	name=neut_file_log[:-4]
	content.append('%mem=5gb'+'\n')
	content.append('%chk='+name+'-cat.chk'+'\n')
	content.append('%nprocshared=28'+'\n')
	content.append('#'+'m06/def2tzvp 5D pop=nbo nosymm'+'\n'+'\n')
	content.append(name+'\n'+'\n')
	content.append('1 2'+'\n')
	
	c = extract_coordinate(neut_file_log)
	for i in range(0, len(c)):
		content.append(c[i]+'\n')
	
	content.append('\n'+'\n')
	
	cat_com_name = name+'-cat.com'
	make_script(name+'-cat')
	data = open(cat_com_name, 'w+')
	for line in content:
		out = line
		data.write(out)
	del content[:]
	shutil.move(cat_com_name, dest2)

def create_anion(neut_file_log):
	c = []
	name=neut_file_log[:-4]
	content.append('%mem=5gb'+'\n')
	content.append('%chk='+name+'-anion.chk'+'\n')
	content.append('%nprocshared=28'+'\n')
	content.append('#'+'m06/def2tzvp 5D pop=nbo nosymm'+'\n'+'\n')
	content.append(name+'\n'+'\n')
	content.append('-1 2'+'\n')
	
	c = extract_coordinate(neut_file_log)
	for i in range(0, len(c)):
		content.append(c[i]+'\n')
	c = []
	content.append('\n'+'\n')
	
	anion_com_name = name+'-anion.com'
	make_script(name+'-anion')
	data = open(anion_com_name, 'w+')
	for line in content:
		out = line
		data.write(out)
	del content[:]
	shutil.move(anion_com_name, dest2)

#create_anion('EL-CH2SiiPr3-opt-nbo-3.log')

for x in neut_log_files[:]:
	create_cat(x)
	create_anion(x)


