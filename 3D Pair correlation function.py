#!/usr/bin/env python
# coding: utf-8

# In[6]:


import trimesh
import csv
import os
import numpy as np
from numpy import *
import math
import matplotlib.pyplot as plt
from scipy.stats import norm

def pairCorrelationFunction_3D(x, y, z, S, rMax, dr):
    """Compute the three-dimensional pair correlation function for a set of
    spherical particles contained in a cube with side length S.  This simple
    function finds reference particles such that a sphere of radius rMax drawn
    around the particle will fit entirely within the cube, eliminating the need
    to compensate for edge effects.  If no such particles exist, an error is
    returned.  Try a smaller rMax...or write some code to handle edge effects! ;)
    Arguments:
        x               an array of x positions of centers of particles
        y               an array of y positions of centers of particles
        z               an array of z positions of centers of particles
        S               length of each side of the cube in space
        rMax            outer diameter of largest spherical shell
        dr              increment for increasing radius of spherical shell
    Returns a tuple: (g, radii, interior_indices)
        g(r)            a numpy array containing the correlation function g(r)
        radii           a numpy array containing the radii of the
                        spherical shells used to compute g(r)
        reference_indices   indices of reference particles
    """
    from numpy import zeros, sqrt, where, pi, mean, arange, histogram

    # Find particles which are close enough to the cube center that a sphere of radius
    # rMax will not cross any face of the cube
    bools1 = x > rMax
    bools2 = x < (S - rMax)
    bools3 = y > rMax
    bools4 = y < (S - rMax)
    bools5 = z > rMax
    bools6 = z < (S - rMax)
    
    interior_indices, = where(bools1 * bools2 * bools3 * bools4 * bools5 * bools6)
    num_interior_particles = len(interior_indices)

    if num_interior_particles < 1:
        raise  RuntimeError ("No particles found for which a sphere of radius rMax\
                will lie entirely within a cube of side length S.  Decrease rMax\
                or increase the size of the cube.")

    edges = arange(0., rMax + 1.1 * dr, dr)
    num_increments = len(edges) - 1
    g = zeros([num_interior_particles, num_increments])
    radii = zeros(num_increments)
    numberDensity = len(x) / 117.1260*122.6690*22.378
    len_d = 0
    # Compute pairwise correlation for each interior particle
    for p in range(num_interior_particles):
        index = interior_indices[p]
        d = sqrt((x[index] - x)**2 + (y[index] - y)**2 + (z[index] - z)**2)
        len_d = len(d) + len_d
        d[index] = 2 * rMax
        (result, bins) = histogram(d, bins=edges, normed=False)
        g[p,:] = result / numberDensity
    print(len_d)
    # Average g(r) for all interior particles and compute radii
    g_average = zeros(num_increments)
    for i in range(num_increments):
        radii[i] = (edges[i] + edges[i+1]) / 2.
        rOuter = edges[i + 1]
        rInner = edges[i]
        g_average[i] = mean(g[:, i]) / (4.0 / 3.0 * pi * (rOuter**3 - rInner**3) )

    return (g_average, radii, interior_indices)

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
root = 'data' # file containing all objects
x_list = []
y_list = []
z_list = []
object_list_passed = [] # list with objects that passed the filter
object_list_filtered = [] # list with all objects except ones with negative center of mass


for file_name in os.listdir(root):
    count = count + 1
    filter_pass_check = 0
    if file_name.endswith('.obj'): # filter to avoid errors if an non-obj file is found
        full_path_to_file = os.path.join(root, file_name) # finding path to each object
        loaded_object = trimesh.load(full_path_to_file, process = True, validate = True) # loading each object according to it's individual path
        if loaded_object.is_watertight is True and check_center_of_mass(loaded_object) is True and check_inertia_components(loaded_object) is True and check_volume(loaded_object) is True:
            object_list_passed.append(loaded_object.center_mass[0])
            z_list.append(loaded_object.center_mass[0]*0.334)
            x_list.append(loaded_object.center_mass[1]*0.2410)
            y_list.append(loaded_object.center_mass[2]*0.2410)
            filter_pass_check = 1 
        if filter_pass_check == 0:
            object_list_filtered.append(loaded_object) # objects that failed the fitlers 


x_list = np.array(x_list)
y_list = np.array(y_list)
z_list = np.array(z_list)

domain_size = 118


dr = 0.25

rMax = 6


# Compute pair correlation
g_r, r, reference_indices = pairCorrelationFunction_3D(x_list, y_list, z_list, domain_size, rMax, dr)
#print(reference_indices)
#print("length of refenrece_indices:", len(reference_indices))
# Visualize
plt.figure()
plt.plot(r, g_r, color='black')
plt.xlabel('r')
plt.ylabel('g(r)')
plt.xlim( (0, 12))
plt.ylim( (0, 1.05 * g_r.max()))
plt.show()
print(len(x_list))


# In[ ]:




