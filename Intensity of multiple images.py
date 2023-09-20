#!/usr/bin/env python
# coding: utf-8

# In[9]:


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# List of TIFF image filenames
filenames = ['RBC_0.17_FD_2.18mg_20210317_7_8bits.tif']

# Create an empty list to store intensity values for each image
intensity_values_list = []

# Iterate over each filename
for filename in filenames:
    # Load the 3D image
    with Image.open(filename) as img:
        # Convert the image to a NumPy array
        img_array = np.array(img)

        # Get the number of slices in the image
        num_slices = img.n_frames

        # Create an empty list to store intensity values for this image
        intensity_values = []

        # Iterate over each slice in the 3D image
        for i in range(num_slices):
            # Get the i-th slice
            img.seek(i)

            # Calculate the average pixel value of the grayscale slice
            gray_img = img.convert('L')
            
            average_intensity = np.mean(gray_img)
            
            # Store the intensity value in the list for this image
            intensity_values.append(average_intensity)
            
        # Store the intensity values list for this image in the overall list
        mean_intensities = np.mean(intensity_values)
        print(filename)
        print(mean_intensities)
        intensity_values_list.append(intensity_values)
# Create a graph of the intensity values for each image
for i, intensity_values in enumerate(intensity_values_list):
    plt.plot(intensity_values, label=f'Image {i+7}')
    

plt.title('Label: XXIV - RBC = 0.17 and [FD] = 2.18 mg/ml - Intensity over Z-axis')
plt.xlabel('Slice')
plt.ylabel('Intensity')
plt.legend()
plt.xlim(right=100)
plt.show()


# In[ ]:




