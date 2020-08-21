""" 
Program to extract final coordinates from all log files in the current directory and create nbo input files with script
"""
import sys
import os
import re
import math

from os import listdir
from os.path import isfile, join

cwd = os.getcwd()
#dest1 = '/users/PAS0925/osu1342/9/electrophilic/successfulfiles'
#dest2 = '/users/PAS0925/osu1342/9/electrophilic/fukui'
onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from cwd

files_list = []
for x in onlyfiles[:]:
	if x[-4:] == '.log':
		files_list.append(x)


def extract_coordinate(file_log):	
	coordinates = []
	file = open(file_log)
	print file_log 
	lines = file.readlines()
	file.close()
	for i, line in enumerate(reversed(lines)):
		if 'Standard orientation:' in line:
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
nbo_files = []
for x in files_list[:]:
	y = extract_coordinate(x)
	data = open(x[:-4]+'-nbo.com', 'w+')
	data.write("%mem=10gb"+'\n')
	data.write("%chk="+x[:-4]+"-nbo.chk"+'\n')
	data.write("%nprocshared=28"+'\n')
	data.write("#m062x/6-31g** pop=nboread"+'\n'+'\n')
	data.write(x[:-4]+'\n'+'\n')
	data.write("0 1"+'\n')
	for line in y:
		out=line+'\n'
		data.write(out)
	del y[:]
	data.write('\n')
	data.write("$nbo bndidx $end"+'\n')
	nbo_files.append(x[:-4]+'-nbo.com')

script_file = []
for x in nbo_files[:]:
	script_name=x[:-4]
	script_file.append(script_name)
#print script_file

for x in script_file[:]:	
	file_script=x
	file2 = open(file_script,'w+')
	file2.close()
	content2=[]
	content2.append('#PBS -S /bin/tcsh'+'\n')
	content2.append('#PBS -N '+file_script+'\n')
	content2.append('#PBS -o '+file_script+'.log'+'\n')
	content2.append('#PBS -A PAA0001'+'\n')
	content2.append('#PBS -l walltime=20:00:00'+'\n')
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


