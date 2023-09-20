#!/usr/bin/env python
# coding: utf-8

# In[1]:


import trimesh
import csv
import os
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

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

list_a1_a2 = []
list_a2_a3 = []

for obj in object_list_passed:
    obj_comp_list_arranged = np.sort(obj.principal_inertia_components)[::-1]
    list_a1_a2.append(obj_comp_list_arranged[0]/obj_comp_list_arranged[1])
    list_a2_a3.append(obj_comp_list_arranged[1]/obj_comp_list_arranged[2])



# plt.hist(list_a1_a2, bins_tmp, density=True, alpha=0.6)
# plt.xlabel('Alpha1/Alpha2')
# plt.ylabel('Frequency')
# title = "Biggest vector component over second biggest. Mean = %.2f" %mean 

bins_tmp = np.arange(1,2,0.01)
mean, std_dev = norm.fit(list_a2_a3)
plt.hist(list_a2_a3,bins_tmp, density=True, alpha=0.6)
plt.xlabel('Alpha2/Alpha3')
plt.ylabel('Frequency')
title = "Second biggest vector component over smallest. Mean = %.2f" %mean 
plt.title(title)
#xmin, xmax = plt.xlim()
#x = np.linspace(xmin, xmax, 100)
p = norm.pdf(mean, std_dev)
plt.plot(p, 'k', linewidth=2)
plt.show()


# In[ ]:




