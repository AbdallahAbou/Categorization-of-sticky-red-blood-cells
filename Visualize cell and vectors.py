#!/usr/bin/env python
# coding: utf-8

# In[13]:


import trimesh
import csv
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly

def smooth(loaded_object): #refine the object and make the principal inertia components positive value
    loaded_object.remove_unreferenced_vertices
    loaded_object.remove_duplicate_faces
    trimesh.repair.fill_holes(loaded_object)
    trimesh.repair.fix_normals(loaded_object, multibody=True)
    trimesh.repair.fix_winding(loaded_object)
    trimesh.smoothing.filter_humphrey(loaded_object, alpha=0.05, beta=0.2, iterations=10, laplacian_operator=None)
    return(loaded_object)
def visualize_object(loaded_object): #visualise the object
    objected_obj = go.Mesh3d(
        x=loaded_object.vertices.T[0],
        y=loaded_object.vertices.T[1],
        z=loaded_object.vertices.T[2],
        colorbar_title='z',
        colorscale=[[0, 'red'],
                    [0.5, 'mediumturquoise'],
                    [1, 'magenta']],
        # Intensity of each vertex, which will be interpolated and color-coded
        intensity=[0, 0.33, 0.66, 1],
        # i, j and k give the vertices of triangles
        i=loaded_object.faces.T[0],
        j=loaded_object.faces.T[1],
        k=loaded_object.faces.T[2],
        opacity=0.1,
    )
    return objected_obj
def visualize_vector(loaded_object): #visualise each vector as a cone
    positive_inertia_components = []
    positive_inertia_components = [abs(component) for component in loaded_object.principal_inertia_components]
    big_vector = max(positive_inertia_components)
    for i in range(len(loaded_object.principal_inertia_components)):
        if big_vector == loaded_object.principal_inertia_components[i]:
            visualized_vector = go.Cone(name='',
                      x = [loaded_object.center_mass[0]],
                      y= [loaded_object.center_mass[1]],
                      z= [loaded_object.center_mass[2]],
                      u=[loaded_object.principal_inertia_vectors[i,0]],
                      v=[loaded_object.principal_inertia_vectors[i,1]],
                      w=[loaded_object.principal_inertia_vectors[i,2]],
                      sizemode='absolute',
                      sizeref=3.2,
                      autocolorscale=True,
                      colorscale='Blues'
            )
            return visualized_vector

#     vector2 = go.Cone(name='',
#                   x = [object.center_mass[0]],
#                   y= [object.center_mass[1]],
#                   z= [object.center_mass[2]],
#                   u=[object.principal_inertia_vectors[1,0]],
#                   v=[object.principal_inertia_vectors[1,1]],
#                   w=[object.principal_inertia_vectors[1,2]],
#                   sizemode='absolute',
#                   sizeref=3.2,
#                   autocolorscale=True,
#                   colorscale='Blues'
#                   )
#     vector3 = go.Cone(name='',
#                   x = [object.center_mass[0]],
#                   y= [object.center_mass[1]],
#                   z= [object.center_mass[2]],
#                   u=[object.principal_inertia_vectors[2,0]],
#                   v=[object.principal_inertia_vectors[2,1]],
#                   w=[object.principal_inertia_vectors[2,2]],
#                   sizemode='absolute',
#                   sizeref=3.2,
#                   autocolorscale=True,
#                   colorscale='Reds'
#                   )
    

obj = trimesh.load("data/c127.obj", process = True, validate = True)
obj = smooth(obj)
vector1_vis = visualize_vector(obj)
objected_obj1 = visualize_object(obj)
data=[objected_obj1,vector1_vis]
fig = go.Figure(data=data)
fig.update_layout(
scene = dict(
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    zaxis_showgrid=False,
    xaxis_visible=False,
    yaxis_visible=False,
    zaxis_visible=False,),
    margin=dict(r=20, l=10, b=10, t=10))


#plotly.offline.plot(fig, filename="cell2.html")


# In[ ]:




