import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
#
#
#
# Graphs out the theoretical microlensing flux of events with different
# starting flux and number of events.
#
c = 25.68836


# make new arrays
x_reg = []
y_reg = []
z_reg = []

print('Calculating...')
mag_min = 20
mag_max = 10
num_min = 5
num_max = 50

for mag in range(mag_max,mag_min,1):
  for num in range(num_min,num_max,5):
    # calculate flux and errors
    z = max([10.**((0.4)*(12 - 15)), 10.**((0.4)*(mag - 15))])
    mag_theo_err = (.001*(((0.04895 * z**2) + (1.8633 * z) + 0.0001985)**(1/2)))
    val_1 = mag + mag_theo_err
    val_2 = mag - mag_theo_err
    f_v_1 = 10**((c-val_1)/2.5)
    f_v_2 = 10**((c-val_2)/2.5)
    flux = 10**((c-mag)/2.5)
    theo_err = np.sqrt((num*((abs(f_v_2 - f_v_1)/2)**2))/(num-1))
    x_reg = x_reg + [flux]
    y_reg = y_reg + [num]
    z_reg = z_reg + [theo_err]

# microlens each and scatter new
x_new = []
z_new = []
for i in range(0,len(x_reg)):
  # reset flux
  flux = x_reg[i]
  num = y_reg[i]
  flux_mean = (flux*(num-1)+2*flux)/num
  x_new = x_new + [flux_mean]

  # reset error
  theo_err = z_reg[i]
  new_theo_err = np.sqrt(((num-1)*((theo_err*np.sqrt(num-1))/(num)) + flux**2)/(num-1))
  z_new = z_new + [new_theo_err]



blue = 'Microlensing 1 of 20 events'
red = 'Microlensing 1 of 50 events'
green = 'Microlensing 1 of 80 events'
blue_patch = mpatches.Patch(color='blue', label=blue)
red_patch = mpatches.Patch(color='red', label=red)
green_patch = mpatches.Patch(color='green', label=green)



print('processing graph')

plt.close()
fig = plt.figure()
tf = True
plt.plot
plt.legend(bbox_transform=plt.gcf().transFigure, bbox_to_anchor = (1,1),handles=[blue_patch, red_patch, green_patch])
ax = fig.add_subplot(211, projection='3d')
ax.scatter(x_reg,y_reg,z_reg,'b')
ax2 = fig.add_subplot(212, projection='3d')
ax2.scatter(x_new,y_reg,z_new,'r')
plt.show()