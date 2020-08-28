import ast
import BL
import Angles
import Dihedral
import Dipole_moment
import write_to_csv
from os import listdir
from os.path import isfile, join

inp = open("input.dat","r")
lines = inp.readlines()
file_list=[]
BL_List = []
Ang_List = []
Dih_List = []
master_list = []

for i,line in enumerate(lines):
    variable, value = line.split('=')
    variable = variable.strip() 

    ##   Reading the location of all log files   ##

    if variable == 'address':
        address = value.rstrip() 
        print ("Accessing all log files from : "+address)

        ##   Store name of all logfiles in a list   ##

        onlyfiles = [f for f in listdir(address) if isfile(join(address, f))]
        for x in onlyfiles[:]:
            if x[-4:] == '.log':
                file_list.append(x)
                master_list.append([x])

    ##    Calculating bond length   ##

    elif variable == 'B_Len':
        if value.rstrip() == 'True':
            print ("Calculating Bond Lengths .....")
        else:
            print ("Bond Lengths not needed!")

    elif variable == 'Blen_atom_list':
        val1 = value.rstrip()
        at_list = ast.literal_eval(val1)
        BL_List = BL.BL_list(address,file_list,at_list)
        print ("Writing bond lengths to CSV file .....")
        i = 0
        for row in master_list:
            row.extend(BL_List[i])
            i = i + 1

    ##    Calculating bond angle   ##

    elif variable == 'B_Ang':
        if value.rstrip() == 'True':
            print ("Calculating Bond Angles .....")
        else:
            print ("Bond Angles not needed!")

    elif variable == 'Ang_atom_list':
        val1 = value.rstrip()
        at_list = ast.literal_eval(val1)
        Ang_List = Angles.Angle_list(address,file_list,at_list)
        print ("Writing bond angles to CSV file .....")
        i = 0
        for row in master_list:
            row.extend(Ang_List[i])
            i = i + 1

    ##    Calculating dihedral angle   ##

    elif variable == 'Dih_Ang':
        if value.rstrip() == 'True':
            print ("Calculating Dihedral Angles .....")
        else:
            print ("Dihedral Angles not needed!")

    elif variable == 'Dih_atom_list':
        val1 = value.rstrip()
        at_list = ast.literal_eval(val1)
        Dih_List = Dihedral.Dihedral_list(address,file_list,at_list)
        print ("Writing dihedral angles to CSV file .....")
        i = 0
        for row in master_list:
            row.extend(Dih_List[i])
            i = i + 1

    ##    Calculating Dipole Moment   ##

    elif variable == 'Dipole_moment':
        if value.rstrip() == 'True':
            print ("Extracting Dipole Moment .....")
            DM_List = Dipole_moment.DM_list(address,file_list)
            print ("Writing Dipole moment to CSV file .....")
            i = 0
            for row in master_list:
                row.extend(DM_List[i])
                i = i + 1
        else:
            print ("Dipole moment not needed!")

inp.close()

write_to_csv.write_csv(master_list,"CheML_params_all.csv",address)
