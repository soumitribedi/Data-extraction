import csv
import os

def write_csv(file_list,property_list,csv_name,address):
    new_list=file_list
    with open(os.path.join(address,csv_name),"w") as f:
        writer = csv.writer(f)
        for row in property_list:
            writer.writerow(row)
    return
