
import numpy as np
from linecache import getline
import matplotlib.pyplot as plt
import re
import cmaps as nclcmaps
import math
#import arcpy as ap



import warnings
warnings.filterwarnings("ignore")

###################### A1 - Read in and properly display elevation data ##########################

# Reading in ASCII file
file = "ascii_elevationfile.txt"

# Obtaining the header using a loop
header = [getline(file, i) for i in np.arange(1,7)]
# Removing the '\n' at the end of each element
header = [x[:-1] for x in header]

# Creating an array containing all the header information
headerInfo = []
for i in [0,1,2,3,4,5]:
    splitH = re.split(" ", header[i])
    headerInfo.append(float(splitH[-1]))

# Assigning header values to variables
cols, rows, lx, ly, cellSize, nd = headerInfo


# Obtaining the DEM data, skipping the header, any data value less than the no data value (-9999) is changed to NaN
dem_data = np.loadtxt(file, skiprows = 6)
dem_data[dem_data<nd] = np.nan

# Easting and Northing coordinates to correspond to DEM data
# taking the XLL and YLL, and adding a the column or row # times the cell size to obtain the E or N coords
easting = lx + np.arange(cols)*cellSize
northing = ly + np.arange(rows)*cellSize

# Creating figure
fig, ax = plt.subplots(figsize=(12, 6))
cs = ax.pcolormesh(easting,northing,dem_data,cmap=nclcmaps.MPL_viridis_r)
# Colorbar legend
fig.colorbar(cs)
# Giving Title and x, y axes
_ = ax.set_title('DEM Data', fontsize = 16)
_ = ax.set_xlabel('Easting (m)')
_ = ax.set_ylabel('Northing (m)')


# Display the plot
#plt.show()

############################ A2 - Compute the X and Y slopes, gradient and aspect terrain parameters of the DEM #################################

slope_X = np.empty((math.trunc(rows),math.trunc(cols)))
slope_X[:] = np.nan
slope_Y = np.empty((math.trunc(rows),math.trunc(cols)))
slope_Y[:] = np.nan

gradient = np.empty((math.trunc(rows),math.trunc(cols)))
gradient[:] = np.nan

aspect = np.empty((math.trunc(rows),math.trunc(cols)))
aspect[:] = np.nan

for i in np.arange(1,math.trunc(rows-3)):
    for j in np.arange(1,math.trunc(cols-3)):

        # The three right elements are added and subtracted by the three left elements added
        sumZ_X = (dem_data[i+1,j-1]+dem_data[i+1,j]+dem_data[i+1,j+1]) - (dem_data[i-1,j-1]+dem_data[i-1,j]+dem_data[i-1,j+1])
        slope_X[i,j] = (sumZ_X/(cellSize*6)) * 100 #to express in perecentage

        # The three bottom elements are added and subtracted by the three top elements
        sumZ_Y = (dem_data[i-1,j+1]+dem_data[i,j+1]+dem_data[i+1,j+1]) - (dem_data[i-1,j-1]+dem_data[i,j-1]+dem_data[i+1,j-1])
        slope_Y[i,j] = (sumZ_Y/(cellSize*6)) * 100 #to express in percentage

        gradient[i,j] = math.sqrt(slope_X[i,j]**2 + slope_Y[i,j]**2)

        aspect[i,j] = math.atan(slope_Y[i,j]/slope_X[i,j])

############################## A1(3) - Generate Slope and aspect maps ##############################       

# Creating figure
fig, ax = plt.subplots(figsize=(12, 6))
cs = ax.pcolormesh(easting,northing,gradient,cmap=nclcmaps.MPL_viridis_r)
# Colorbar legend
fig.colorbar(cs)
# Giving Title
_ = ax.set_title('Gradient of DEM', fontsize = 16) 
_ = ax.set_xlabel('Easting (m)')
_ = ax.set_ylabel('Northing (m)')

plt.show()

#Output .txt file used to verify slope/gradient/aspect content        
with open('output.txt','w') as f:
    for i in np.arange(0,597):
        for j in np.arange(0,599):
            f.write(str(slope_Y[i,j]) + " ")


