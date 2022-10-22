import matplotlib.pyplot as plt
from linecache import getline
import numpy as np
import re
import math

import warnings
warnings.filterwarnings("ignore")

# Reading in ASCII file
file = "ascii_elevationfile.txt"

# Obtaining the header using a loop
header = [getline(file, i) for i in np.arange(1,7)]
# Removing the '\n' at the end of each element
header = [x[:-1] for x in header]

headerInfo = []
for i in [0,1,2,3,4,5]:
    splitH = re.split(" ", header[i])
    headerInfo.append(float(splitH[-1]))

# Assigning header values to variables
cols, rows, lx, ly, cellSize, nd = headerInfo

# Obtaining the header using a loop
header = [getline(file, i) for i in np.arange(1,7)]
# Removing the '\n' at the end of each element
header = [x[:-1] for x in header]

# Obtaining the DEM data, skipping the header, any data value less than the no data value (-9999) is changed to NaN
dem_data = np.loadtxt(file, skiprows = 6)
dem_data[dem_data<nd] = np.nan

# Easting and Northing coordinates to correspond to DEM data
# taking the XLL and YLL, and adding a the column or row # times the cell size to obtain the E or N coords
easting = lx + np.arange(cols)*cellSize
northing = ly + np.arange(rows)*cellSize

# Empty arrays, for user input variables
A_coords = [np.nan,np.nan]
B_coords = [np.nan,np.nan]

A_input = input("Enter the coordinates of point A in the format '(COLUMN,ROW)':\n Range of X : 0-601 \n Range of Y : 0-599 \n")
B_input = input("Enter the coordinates of point B in the format '(COLUMN,ROW)':\n Range of X : 0-601 \n Range of Y : 0-599 \n")

A_split, B_split = re.split(r"[,()!]", A_input) , re.split(r"[,()!]", B_input)
A_coords[0], A_coords[1], B_coords[0], B_coords[1] = int(A_split[1]), int(A_split[2]), int(B_split[1]), int(B_split[2])

A_X = lx + A_coords[0]*cellSize
A_Y = ly + A_coords[1]*cellSize
A_Z = dem_data[A_coords[0],A_coords[1]]

B_X = lx + B_coords[0]*cellSize
B_Y = ly + B_coords[1]*cellSize
B_Z = dem_data[B_coords[0],B_coords[1]]


# Computing the azimuth, in radians and degrees
az_Rad =  math.atan2((B_X-A_X),(B_Y-A_Y))
az_Deg = math.degrees(az_Rad)


########################## A2(2) - Distance Intervals ###############################

# Computing the horizontal distance between points A and B on the ground
distance = round(math.sqrt((B_Y-A_Y)**2 + (B_X-A_X)**2),2)

# Modulus operator used to obtain remainder
# If remainder is not zero, then a distance interval array is created to the nearest multiple of 10
# The array is then appended to include the last value which is a interval less than 10
if distance % 10 != 0:
    distanceItv = np.arange(0,int(math.floor(distance/10)))*10 + 10
    distanceItv = np.append(distanceItv, math.floor(distanceItv[-1] + distance % 10))

    #If the remainder is equal to zero, then a distance interval array is created with the multiples of 10
else:
    distanceItv = np.arange(0,distance/10)*10 + 10

# Creating multiple empty arrays, the size of the distance interval array
eastGC = np.zeros(len(distanceItv))
northGC = np.zeros(len(distanceItv))
r = np.zeros(len(distanceItv))
c = np.zeros(len(distanceItv))
elev = np.zeros(len(distanceItv))

for i in range(len(distanceItv)):

    # Computing the Easting and Northing coordinates on the horizontal distance line, at the corresponding distance intervals
    eastGC[i] = A_X + distanceItv[i] * math.sin(az_Rad)
    northGC[i] = A_Y + distanceItv[i] * math.cos(az_Rad)

    row = int(round(-((northGC[i]-ly)/cellSize - (rows + 0.5))))
    column = int(round((eastGC[i]-lx)/cellSize + 0.5))

    r[i], c[i] = row, column
    elev[i] = dem_data[row,column]
    
    
plt.figure
plt.scatter(eastGC,elev)
plt.title('Terrain Profile at 10m Intervals between A and B')
plt.xlabel('Distance Intervals of 10 (m)')
plt.ylabel('Elevation')
plt.show()

print(elev, dem_data[10,10], dem_data[50,50])

    
    
    








