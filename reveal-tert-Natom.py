import sys
import os
import re
import math

from os import listdir
from os.path import isfile, join

cwd = os.getcwd()   #current working directory

onlyfiles = [f for f in listdir(cwd) if isfile(join(cwd, f))] #will extract only files from a address leaving out directories

files_list = []

for n in range(len(onlyfiles)):
	file_name = onlyfiles[n]
	if file_name[-4:] == '.log':
		files_list.append(onlyfiles[n])

def extract_coordinate(file_log):	
	coordinates = []
	file = open(file_log)
	print file_log 
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

def valencyN(coordinate):
	xcoordinate = []
	ycoordinate = []
	zcoordinate = []
	atom_type = []
	natom = len(coordinate)
	dist = [[0 for i in range(natom)] for j in range(natom)]
	connect = [[0 for i in range(natom)] for j in range(natom)]
	valency3 = []
	valency4 = []
	val = []
	buf = 0
	counter = 0
	for i in range(0,natom):
		at, x, y, z = coordinate[i].split()
		X = float(x)
		Y = float(y)
		Z = float(z)
		xcoordinate.append(X)
		ycoordinate.append(Y)
		zcoordinate.append(Z)
		atom_type.append(at)
	for i in range(0,natom):
		for j in range(0,natom):
			dist_x = xcoordinate[i] - xcoordinate[j]
			dist_y = ycoordinate[i] - ycoordinate[j]
			dist_z = zcoordinate[i] - zcoordinate[j]
			dist[i][j] = math.sqrt(dist_x**2 + dist_y**2 + dist_z**2)
	for i in range(0,natom):
		for j in range(0, natom):
			if atom_type[i] == '7':
				if 0.89 < ("%.2f" % dist[i][j]) < 1.99:
					print 'hi'
					#counter = counter + 1
					#print counter
					#buf = counter

		counter = 0			
		if buf == 3:
			valency3.append(i)
		elif buf == 4:
			valency4.append(i)
	return valency3, valency4

val3, val4 = valencyN(extract_coordinate('G4L0144-2-nbo.log'))
print val3, val4

"""
for x in files_list[:]:
	y = extract_coordinate(x)
	val3, val4 = valencyN(y)
	print x, val3, val4
"""		
