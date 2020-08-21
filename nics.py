#!/share/apps/Python341/bin/python3.4

import commands
import shutil
import re
import sys
import os



# Step 1: Uncomment is asking for the file name from command line
#file = raw_input('Enter log file name: ')

logfile = 'p-F-complex-amide-nbo.log'

# Read the log file
with open(logfile,'r') as f:
	file = f.readlines()

# Dictionary of atoms with atomic number and mass. You can add atoms if you want to. Make sure that the masses are
# right. Log file will have the exact masses.
atoms ={
	8:{'symbol': 'O', 'mass': 16},
	7:{'symbol': 'N', 'mass': 14},
	6:{'symbol': 'C', 'mass': 12},
	1:{'symbol': 'H', 'mass': 1}
}


# Finding the input orientation. This is to get the atom center numbers
for line in file:
	if 'Input orientation' in line:
		start = file.index(line) + 5
		break

# Finding coordinates starting from the 'start' obtained in previous lines
coordinates = []
for l in range(start, len(file)):
	if '-'*30 not in file[l]:
		coordinates.append(file[l])
	else:
		break

# Just printing the coordinates to confirm
for xyz in coordinates:
	print xyz.strip('\n')


# Get the atom center numbers of the ring atoms from the user if they are different across different
# structures. If the atoms numbers are same across all the structures then you can provide a list of
# those numbers here.

num = [1, 2, 3, 4, 5, 6]


# center_num: will have the list of atoms center numver; atomic_num: will have the list of atomic numbers;
center_num = []
atomic_num = []
final_coordinates =''
X_bq = 0.0		# Numerator for the X_COM
Y_bq = 0.0		# Numerator for the Y_COM
Z_bq = 0.0		# Numerator for the Z_COM


total_mass_dr = 0.00	# Denominator for the COM of the ring


# splitting the lines in coordinates to put it in above lists
for line in coordinates:
	tmp = line.split()
	print tmp

	# Adding the elements of the tmp to the list
	center_num = tmp[0]
	atomic_num = int(tmp[1])
	X = float(tmp[3])
	Y = float(tmp[4])
	Z = float(tmp[5])

	final_coordinates += atoms[atomic_num]['symbol'] + "          " + tmp[3] + "         " + tmp[4] + "         " + tmp[5] + "\n"


	# Check if the atom number is in num
	center_num = int(tmp[0])
	if center_num in num:
		X_bq += atoms[atomic_num]['mass'] * X
		Y_bq += atoms[atomic_num]['mass'] * Y
		Z_bq += atoms[atomic_num]['mass'] * Z
		total_mass_dr += atoms[atomic_num]['mass']


# Adding NICS point to the final_coordiantes
nics_x = X_bq/total_mass_dr
nics_y = Y_bq/total_mass_dr
nics_z = Z_bq/total_mass_dr

final_coordinates += "Bq" + "          " + str(nics_x) + "         " + str(nics_y) + "         " + str(nics_z)
for i in range(1,5):
	final_coordinates = final_coordinates + '\n' + "Bq" + "      " + str(nics_x) + "     " + str(nics_y) + "     " + str(nics_z+0.5*i)

# Printing final coordinates
print "============ Final coordiantes for the NICS ======================"
print "%mem=5gb"
print "nprocshared=28"
print ("chk="+logfile[:-4]+"chk")
print ("#m062x/def2tzvp pop=nbo6")
print " "
print "comment"
print " "
print "0 1"
print final_coordinates






