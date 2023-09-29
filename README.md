# Categorization-of-sticky-red-blood-cells
Red blood cell aggregation happens in the human body because blood is a very complex fluid composed of many different particles that push the red blood cells around and makes them stick to each other. 
This may be an indicator of disease as well as a factor, it can lead to health issues within the heart and in worst cases it can even lead to heart attacks. 
In this study we investigate the exact moment cells in the human body reach aggregation and which forces (pumping of heart) would be needed to break them up again and for flow to continue, 

Steps:
- Studying percolation of red bloods cells in different concentrations of Dextran and virus-FD (Simulating the effects of in vivo).
- Capture images of samples using laser scanning confocal microscopy (3D images).
- Import images into python and plot graphs of intensity over Z-Axis. 
- Select high quality images and analyze said images.
- Using leverage machine learning algorithms to segment cells into individual objects (ilastik software / Fiji's Trainable Weka Segmentation plugin ),
- Importing objects into python and extract information namely Moment of inertia vectors, Center of mass, Volume ect. Calculating Eigenvectors and running all of this through filter to classify the cells according to their shape.
- Add all of this to a large data base and access it each time making the program must more efficient and faster, 
- Calculate the pair correlation function g(r) of the whole sample and extract results.

Download dataset of RBC objects and put in directory

Manually create ids.txt file 
