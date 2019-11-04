
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
num_pairs = 2 #the number of pairs that we are observing 
cnt = 0
col_list = [] #list of column in data sheet, column value corresponds to pair value
plot_list = [] #list of plots varying by pair
value_to_add_list = [] #list of values to add to the buffer sorted by the pair value

mag_vector = []
gyro_vector = [] #the elements of these vectors are the x,y,z components of the vectors,respectively
accel_vector = []

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


for i in range(num_nodes):
  col_index[i,i]=num_nodes+1

for j in range(1,num_nodes):
  for k in range(j):
    col_index[j,k] = cnt
    col_index[k,j] = cnt
    cnt +=1

# this determines and stores the relevant data column
for i in range(num_pairs):
  pair_index[i,0], pair_index[i,1] = map(int,raw_input("Enter the two distinct node numbers you would like to graph separate by a space:   ").split())
  value_col = col_index[pair_index[i,0],pair_index[i,1]]
  col_list.append(value_col)
# print col_index
# print (value_col)
  
# Init the figure.
plt.ion()
plt.figure(1)
plt.cla()
value_buffer = np.zeros((buffL, num_pairs))
time_buffer = deque(range(-1*buffL,0))
color = ['b','g','r','c','m','y','k','cyan','maroon','navy','violet','hotpink','lime','gold']

# Plotting the distance between nodes on a line chart COMPLETE AND FUNCTIONAL, COMMENTED OUT TO WORK ON SCATTER PLOT METHOD
for i in range(num_pairs):
  linePlot, = plt.plot(time_buffer, value_buffer[:,i],label='Line '+ str(pair_index[i,0]) + " " + str(pair_index[i,1]) ,color= color[i])
  plot_list.append(linePlot) 
plt.ylabel('Distance Separating Nodes (m)')
plt.xlabel('Measurement Time Ago (sec)')
plt.legend()


# Run forever, adding lines as they are available.
counter = 0
while 1:

  line = fin.readline()
  if (not line) & (file_method == "file"):
    break
  if (not line) & (file_method == "stdin"):
    continue
  while line[-1] != '\n':  # If line is incomplete, add to it.
    line += fin.readline()

    
  # Get the integers from the line string
  data = line.split(',') 
  for i in range(num_pairs):
    # You can plot the raw data or a function of the data. Define here.
    value_to_add = float(data[col_list[i]])
    if np.abs(value_to_add)>100:
      value_to_add= np.NaN
    value_buffer[:-1,i] = value_buffer[1:,i]
    value_buffer[-1,i] = value_to_add

    
    # sys.stderr.write("Buffer Value: %f\n" % value_to_add) #having this uncommented will print out every graphed data point

  #so long as the last column is the time column this if statement will never be entered
  if time_col >= 0:
    time_buffer.popleft()
    time_buffer.append(float(data[time_col]))
    sys.stderr.write(" Time: %f\n" % float(data[time_col]))

  plt.draw() #the draw is outside the below for loop that way the informatoin updates once and each line does not move separately
  plt.pause(0.02)#having th epause inside the for loops was causing it to jitter unnecesarily.
  # Every plotSkip rows, redraw the plot. Time stamps, relative to the 
  #  maximum time stamp, are on the x-axis.
  for i in range(num_pairs):
    counter += 1
    if np.mod(counter, plotSkip) == 0:
      plot_list[i].set_ydata(value_buffer[:,i])
      # print(value_buffer)
      relTime = np.array(time_buffer) - max(time_buffer)
      plot_list[i].set_xdata(relTime)
      mintime = min(relTime)
      plt.axis([mintime, 0, 0, 8 ])

      
      