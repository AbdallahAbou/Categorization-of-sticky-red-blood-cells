#!/usr/bin/env python
# coding: utf-8

# In[8]:


import trimesh
import csv
import os
import numpy as np
import math
import matplotlib.pyplot as plt

def generateDataFile(dataList): # Write data to Csv file while checking old data with newly added data
    # initiate data variable
    newObjects = [] # variable to store  IDs of the new added object 
    oldObjects = [] # variable to store IDs of objects already handled

    # open the files to treat them 
    dataFile = open('data.csv', 'a', newline='', encoding='utf-8') # data.csv file to store the information
    idsFileRead = open('ids.txt', 'r') # ids.txt file contains file names of objects that are already treated
    writer = csv.writer(dataFile)
   
    # read the IDs of old objects and store them in oldObjects list
    oldObjects = [el for el in idsFileRead.read().split(",") if el]
    idsFileRead.close()

    # loop through all objects and export the new objects data to the data.csv file 
    for dt in dataList:
        # check if the object obj exists in the oldObjects list
        if dt["objname"] not in oldObjects:
            # append object to data.csv file
            writer.writerow([dt["objname"], dt["x"], dt["y"], dt["z"], dt["alpha1"], dt["alpha2"], dt["alpha3"], dt["a1/a2"],
                             dt["a2/a3"],dt["volume"]])
            # append the object filename to newObjects
            newObjects.append(dt["objname"])
    writer.writerow("##############")
    # close the data.csv file descriptor
    dataFile.close()
    # write new objs ids to ids.txt
    with open('ids.txt', 'w') as f:
        f.write(",".join(oldObjects + newObjects))
    print("Export New objects to data.csv")
    return


def add_to_Csv(object_list_): # Create data array with necessary information and execute the generateDataFile function
    dataToCsv = []
    print("generate dataToCsv array ....")
    for object_ in object_list_:
        object_comp_list_arranged = np.sort(object_.principal_inertia_components)[::-1]
        dataToCsv.append({
            "objname": object_.metadata["file_name"].replace(".obj", ""),
            "x": round(object_.center_mass[2] * 0.2410,3),
            "y": round(object_.center_mass[1] * 0.2410,3),
            "z": round(object_.center_mass[0] * 0.334,3),
            "alpha1": round(object_comp_list_arranged[0]/1000,3),
            "alpha2": round(object_comp_list_arranged[1]/1000,3),
            "alpha3": round(object_comp_list_arranged[2]/1000,3),
            "a1/a2": round(object_comp_list_arranged[0]/object_comp_list_arranged[1],3),
            "a2/a3": round(object_comp_list_arranged[1]/object_comp_list_arranged[2],3),
            "volume": round(object_.volume*0.2410*0.2410*0.334,3),
        }) 
    generateDataFile(dataToCsv)

def check_center_of_mass(loaded_object):
    if (loaded_object.center_mass[0] > 0 ) and (loaded_object.center_mass[1] > 0 ) and (loaded_object.center_mass[2] > 0 ):
            return True
def check_inertia_components(loaded_object):
    positive_inertia_components = []
    positive_inertia_components = [abs(component) for component in loaded_object.principal_inertia_components]
    a = max(positive_inertia_components)
    positive_inertia_components.remove(max(positive_inertia_components))
    b = positive_inertia_components[0]
    c = positive_inertia_components[1]
    if int(b + c) in range(int(a-a*25/100),int(a+a*25/100)) and int(b) in range(int(c/2),int(2*c)):
        return True

def check_volume(loaded_object):
    if loaded_object.volume > 2300 and loaded_object.volume < 5100:
        return True

#####################    
count = 0 # number of objects loaded
count_filtered = 0 # number of objects with at least one negative value of center of mass
count_not_watertight = 0
Distance_to_each = [] # Array to store values of distance of each cell from other cells
root = 'data' # file containing all objects

object_list_passed = [] # list with objects that passed the filter
# objects with negative center of mass are on the edge and cannot be carved properly
object_list_filtered = [] # list with all objects except ones with negative center of mass

volume_passed = 0
total_volume_passed = 0
file_name_list = [] # list with all object file names
Volumes_list = []
####################
for file_name in os.listdir(root):
    count = count + 1
    filter_pass_check = 0
    if file_name.endswith('.obj'): # filter to avoid errors if an non-obj file is found
        full_path_to_file = os.path.join(root, file_name) # finding path to each object
        file_name_list.append(file_name) # storing the file names of loaded objects
        loaded_object = trimesh.load(full_path_to_file, process = True, validate = True) # loading each object according to it's individual path
        if loaded_object.is_watertight is True and check_center_of_mass(loaded_object) is True and check_inertia_components(loaded_object) is True and check_volume(loaded_object) is True:
            object_list_passed.append(loaded_object)
            filter_pass_check = 1 
            #print(loaded_object.metadata["file_name"])
            volume_passed = loaded_object.volume
            total_volume_passed += volume_passed
            Volumes_list.append(loaded_object.volume)
        if filter_pass_check == 0:
            count_filtered = count_filtered + 1
            object_list_filtered.append(loaded_object) # objects that failed the fitlers 
            #print(loaded_object.metadata["file_name"])
            if loaded_object.is_watertight is False:
                #print(loaded_object.metadata["file_name"], " is not water tight")
                count_not_watertight = count_not_watertight + 1  

ratio = count_filtered/count 
ratio_not_watertight = count_not_watertight/count
add_to_Csv(object_list_passed)
add_to_Csv(object_list_filtered)




# In[ ]:





# In[ ]:





# In[ ]:




