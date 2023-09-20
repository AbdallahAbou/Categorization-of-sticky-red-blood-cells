#!/usr/bin/env python
# coding: utf-8

# In[7]:


from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the 3D TIFF image
img = Image.open('RBC_0.17_FD_2.18mg_20210317_7_8bits.tif')

# Get the number of slices
num_slices = img.n_frames

# Create an empty list to store the intensity values
intensity_values = []

# Loop through each slice
for i in range(25, 67):
    img.seek(i)
    # Convert the slice to grayscale
    gray_img = img.convert('L')
    # Calculate the average pixel value of the grayscale slice
    avg_intensity = np.mean(gray_img)
    # Append the average intensity to the list
    intensity_values.append(avg_intensity)
    
mean_intensities = np.mean(intensity_values) 


intensity_values = []
for i in range(num_slices):
    # Select the slice
    img.seek(i)
    # Convert the slice to grayscale
    gray_img = img.convert('L')
    # Calculate the average pixel value of the grayscale slice
    avg_intensity = np.mean(gray_img)
    # Append the average intensity to the list
    intensity_values.append(avg_intensity)

print(mean_intensities)
# Plot the intensity values using a line graph
plt.plot(intensity_values)
plt.xlabel('Slice Number')
plt.ylabel('Intensity')
plt.show()


# In[ ]:




