
#
# Version History:
#
# Version 1.0: Initial Release
#
# Version 1.1: 27 Sept 2012.
#  Change: This version won't delete (pop) data unless it is going to enter 
#      in a new piece of data.
#This code is working as of October 4th and properly graphs as many node connections as necesarry

import sys
import getopt
import array
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Default inputs: column number (0=1st column, <0 value is key for doesn't exist.
time_col  = -1 
buffL    = 400 # buffer length, ie, how much data to plot. 
plotSkip  = 1 # How many lines to read before replotting the data.
startSkip  = 5  # How many rows at start of text file to remove before plotting data.
file_method = "stdin"
fin     = sys.stdin
num_nodes = 6 # the number of nodes used
num_pairs = 15 #the number of pairs that we are observing initialized here but filled later
cnt = 0
col_list = [] #list of column in data sheet, column value corresponds to pair value
plot_list = [] #list of plots varying by pair
value_to_add_list = [] #list of values to add to the buffer sorted by the pair value
rad = 0.0 #used to convert from degrees to radians 
mag_vector = []
gyro_vector = [] #the elements of these vectors are the x,y,z components of the vectors,respectively
accel_vector = []
test_pts = [] #this list stores a pt_transform array for each of the nodes that when multiplied by the distance gives us potential points

vector_fill = ['x','y','z']
for i in range(3):
  mag_vector.append(vector_fill[i])
  gyro_vector.append(vector_fill[i])
  accel_vector.append(vector_fill[i])

# Accept command line inputs for 
myopts, args = getopt.getopt(sys.argv[1:],"i:s:k:p:t:")
for o, a in myopts:
  if o == "-k":
    file_method = "file"
    fname = a
    fin = open(a,'r')
  elif o == "-s":
    startSkip = int(a)
  elif o == "-p":
    plotSkip = int(a)
  elif o == "-t":
    num_pairs = int(a) #the number of pairs that are being plotted
  else:
    sys.stderr.write("Usage: %s -v Value_Column_Index -t Time_Column_Index -i filename.txt" % sys.argv[0])


pair_index = np.zeros((num_pairs,2), dtype = int) #this index tracks the pairs of nodes for observing
col_index = np.zeros((num_nodes,num_nodes), dtype = int) #this index allows the user to enter two robots and the script can now find the proper data
pt_transform = np.zeros((360,2), dtype = float) # this array stores cos values in (:,0) sin values in (:,1) from 0:2pi and using dist_index we can find relative x and y values

for i in range(num_nodes):
  col_index[i,i]=num_pairs+1

for j in range(num_nodes):
  for k in range(j):
    col_index[j,k] = cnt
    col_index[k,j] = cnt
    cnt +=1

# this determines and stores the relevant data column
# for i in range(num_pairs):
#   pair_index[i,0], pair_index[i,1] = map(int,raw_input("Enter the two distinct node numbers you would like to graph separate by a space:   ").split())
#   value_col = col_index[pair_index[i,0],pair_index[i,1]]
#   col_list.append(value_col)
for i in range(num_pairs):
  col_list.append(i)
# print(value_col)
print(col_list)
# print(col_index)

#the purpose of this matrix is to store the distance between the nodes  for later analysis this matrix is structured similar to col_index
dist_index = np.zeros((num_nodes,num_nodes), dtype = float)

# this matrix stores the points that have been determined as accurate from the test_pts matrix
pt_coords = np.zeros((num_nodes,2), dtype = float)

# Transformation Matricies: sin and cos iterated 0:2pi so that the dist_index can be used as the hypotenuse to find relative x and y coords
for i in range(0,360,1):
  rad = np.radians(i)
  pt_transform[i,0] = round(np.cos(rad),8)
  pt_transform[i,1] = round(np.sin(rad),8)

  
# Init the figure.
plt.ion()
plt.figure(1)
plt.cla()
value_buffer = np.zeros((buffL, num_pairs))
time_buffer = deque(range(-1*buffL,0))
color = ['b','g','r','c','m','y','k','cyan','maroon','navy','violet','hotpink','lime','gold']


#TEMPORARY, NOT NEEDED HERE; LEAVE IN WHILE LOOP
line = fin.readline()
while line[-1] != '\n':  # If line is incomplete, add to it.
  line += fin.readline()

    
# Get the integers from the line string
#COMPLETED OCT 11 this component fills the dist_index cataloging the distance between the nodes
data = line.split(',') 
for i in range(num_pairs):
  # You can plot the raw data or a function of the data. Define here.
  value_to_add = float(data[col_list[i]])
  if np.abs(value_to_add)>100:
    value_to_add= np.NaN
  value_buffer[:-1,i] = value_buffer[1:,i]
  value_buffer[-1,i] = value_to_add
  

  for k in range(i):
    dist_index[i,k] = value_to_add
    dist_index[k,i] = value_to_add
  # print(value_to_add)
  # dist_index[pair_index[i,0]-1,pair_index[i,1]-1]=value_to_add
  # dist_index[pair_index[i,1]-1,pair_index[i,0]-1]= value_to_add
 
# print(dist_index)


# This fills the test_pts matrix using pt_transform and dist_index
# for i in range(max):



plt.scatter(pt_transform[:,0],pt_transform[:,1])
plt.show()

# # Plot base node at origin of scatter plot and s NOT COMPLETE
# plt.plot(5,1,'o')
# print(value_buffer[0,0])
# for i in range(num_pairs):
#   linePlot, = plt.plot(value_buffer[:,i],time_buffer, '*',label='Line '+ str(pair_index[i,0]) + " " + str(pair_index[i,1]) ,color= color[i])
#   plot_list.append(linePlot) 
# plt.ylabel('Distance Separating Nodes (m)')
# plt.xlabel('Measurement Time Ago (sec)')
# plt.legend()

# Run forever, adding lines as they are available.
#COMMENTED OUT FOR TESTING DO NOT DELETE
# counter = 0
# while 1:

#   line = fin.readline()
#   if (not line) & (file_method == "file"):
#     break
#   if (not line) & (file_method == "stdin"):
#     continue
#   while line[-1] != '\n':  # If line is incomplete, add to it.
#     line += fin.readline()

    
#   # Get the integers from the line string
#   data = line.split(',') 
#   for i in range(num_pairs):
#     # You can plot the raw data or a function of the data. Define here.
#     value_to_add = float(data[col_list[i]])
#     if np.abs(value_to_add)>100:
#       value_to_add= np.NaN
#     value_buffer[:-1,i] = value_buffer[1:,i]
#     value_buffer[-1,i] = value_to_add

#     # print(value_to_add)
#     # sys.stderr.write("Buffer Value: %f\n" % value_to_add) #having this uncommented will print out every graphed data point
#   # print(value_buffer)
#   #so long as the last column is the time column this if statement will never be entered
#   if time_col >= 0:
#     time_buffer.popleft()
#     time_buffer.append(float(data[time_col]))
#     sys.stderr.write(" Time: %f\n" % float(data[time_col]))

#   plt.draw() #the draw is outside the below for loop that way the informatoin updates once and each line does not move separately
#   plt.pause(0.02)#having th epause inside the for loops was causing it to jitter unnecesarily.

#   for i in range(num_pairs):
#     counter += 1
#     if np.mod(counter, plotSkip) == 0:
#       plot_list[i].set_xdata(value_buffer[:,i])
#       # print(value_buffer)
#       # relTime = np.array(time_buffer) - max(time_buffer)
#       # plot_list[i].set_xdata(relTime)
#       # mintime = min(relTime)
#       plt.axis([-8, 8, -8, 8 ])

      
#       