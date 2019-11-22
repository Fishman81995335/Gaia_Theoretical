import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches
import random as r
from mpl_toolkits.mplot3d import Axes3D
import statistics as stats

#
#
#
# Graphs out the theoretical microlensing flux of events with different
# starting flux and number of events.
#
c = 25.68836


print("Creating random values ...")
num_events = 30000
mag_min = 20
mag_max = 12
num_min = 5
num_max = 50
mic_amt = 2

# make new arrays to hold random magnitude values
flux_vals = []
mag_vals = []
err_vals = []
nums = []
micro_bool = []
for x in range(0, num_events):
    mag = r.random() * (mag_max - mag_min) + mag_min
    mag_vals.append(mag)
    num = r.randint(num_min, num_max)
    nums.append(num)
    z = max([10.0 ** ((0.4) * (12 - 15)), 10.0 ** ((0.4) * (mag - 15))])
    mag_theo_err = 0.001 * (((0.04895 * z ** 2) + (1.8633 * z) + 0.0001985) ** (1 / 2))
    val_1 = mag + mag_theo_err
    val_2 = mag - mag_theo_err
    f_v_1 = 10 ** ((c - val_1) / 2.5)
    f_v_2 = 10 ** ((c - val_2) / 2.5)
    err = (f_v_2 - f_v_1) / 2
    err_vals.append(err)
    flux = 10 ** ((c - mag) / 2.5)
    flux_vals = flux_vals + [flux]
    theo_err = np.sqrt((num * ((abs(f_v_2 - f_v_1) / 2) ** 2)) / (num - 1))
    mic_or_not = r.random()
    if mic_or_not < 0.05:
        micro_bool.append(True)
    else:
        micro_bool.append(False)


print("Simulating Measurements")

flux_ts_lists = []
stdev = []
mean = []
col = []
for n in range(len(flux_vals)):
    if micro_bool[n]:
        flux = flux_vals[n]
        err = err_vals[n]
        num = nums[n]
        s = np.random.poisson(flux, num)
        to_change = r.randint(0, num - 1)
        s[to_change] = s[to_change] * mic_amt
        flux_ts_lists.append(s)
        stdev.append(stats.stdev(s))
        mean.append(stats.mean(s))
        col.append("r")
    else:
        flux = flux_vals[n]
        err = err_vals[n]
        num = nums[n]
        s = np.random.poisson(flux, num)
        flux_ts_lists.append(s)
        stdev.append(stats.stdev(s))
        mean.append(stats.mean(s))
        col.append("b")


fig = plt.figure()
tf = True
plt.plot
blue = "No microlensing"
red = "Microlensed 1 event by factor of " + str(mic_amt)
blue_patch = mpatches.Patch(color="blue", label=blue)
red_patch = mpatches.Patch(color="red", label=red)
plt.legend(
    bbox_transform=plt.gcf().transFigure,
    bbox_to_anchor=(1, 1),
    handles=[blue_patch, red_patch],
)
print("Making plot...")
ax = plt.subplot()
ax.scatter(np.log(mean), np.log(stdev), c=col, s=2)
ax.set_xlabel("log flux")
ax.set_ylabel("log error")
plt.show()
