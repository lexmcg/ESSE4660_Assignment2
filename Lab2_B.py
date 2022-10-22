import numpy as np
import math

# Creating array with coordinates of nodes A,B,C in triangle
triangle = np.array([[300,600,200], 
                    [700,200,350],  
                    [1000,850,500]]) 

# Computing A and B vectors stemming from node C
A_vec = np.subtract(triangle[0,:],triangle[2,:])
B_vec = np.subtract(triangle[1,:],triangle[2,:])

# Calculating IJK values for vectors A and B
ijk_values = np.zeros([3])
ijk_values[0] = A_vec[1]*B_vec[2] - B_vec[1]*A_vec[2]
ijk_values[1] = A_vec[0]*B_vec[2] - B_vec[0]*A_vec[2]
ijk_values[2] = A_vec[0]*B_vec[1] - B_vec[0]*A_vec[1]

# Magnitude of normal vector
mag_norm = math.sqrt(ijk_values[0]**2 + ijk_values[1]**2 + ijk_values[2]**2)

# Magnitude of p vector
mag_p = math.sqrt(ijk_values[0]**2 + ijk_values[1]**2)

# Calculating slope, converting to degrees
slope = math.asin(mag_p/mag_norm)
slope = math.degrees(slope)

# Calculating aspect, converting to degrees
aspect = math.atan(-(A_vec[0]*B_vec[2] - B_vec[0]*A_vec[2])/(A_vec[1]*B_vec[2] - B_vec[1]*A_vec[2]))
aspect = math.degrees(aspect)

print(slope,aspect)