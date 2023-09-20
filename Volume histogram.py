#!/usr/bin/env python
# coding: utf-8

# In[4]:


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
count_passed = 0
root = 'data' # file containing all objects

object_list_passed = [] # list with objects that passed the filter
# objects with negative center of mass are on the edge and cannot be carved properly
object_list_filtered = [] # list with all objects except ones with negative center of mass
Volumes_list = []
total_volume_passed = 0
Volumes_list_passed = []
####################
for file_name in os.listdir(root):
    count = count + 1
    filter_pass_check = 0
    if file_name.endswith('.obj'): # filter to avoid errors if an non-obj file is found
        full_path_to_file = os.path.join(root, file_name) # finding path to each object
        loaded_object = trimesh.load(full_path_to_file, process = True, validate = True) # loading each object according to it's individual path
        if loaded_object.is_watertight is True and check_center_of_mass(loaded_object) is True and check_inertia_components(loaded_object) is True and check_volume(loaded_object) is True:
            object_list_passed.append(loaded_object)
            filter_pass_check = 1 
            #print(loaded_object.metadata["file_name"])
            volume_passed = loaded_object.volume
            total_volume_passed = volume_passed + total_volume_passed
            Volumes_list.append(loaded_object.volume)
            count_passed = count_passed + 1
        if filter_pass_check == 0:
            object_list_filtered.append(loaded_object) # objects that failed the fitlers 

                
bins = [40*x for x in range(0,200)]
mean, std_dev = norm.fit(Volumes_list_passed)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax)
p = norm.pdf(x, mean, std_dev)
plt.plot(x, p, 'k', linewidth=2)
plt.hist(Volumes_list_passed, bins, density = True, alpha=0.6)
mean, std_dev = norm.fit(Volumes_list_passed)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax)
p = norm.pdf(x, mean, std_dev)
plt.plot(x, p, 'k', linewidth=2)
plt.xlabel('Volume')
plt.ylabel('Frequency')
title = "Volumes Histogram. Mean = %.2f" %mean 
plt.title(title)
plt.show()




# In[ ]:





# In[ ]:




