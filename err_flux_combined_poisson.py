import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches
import random as r
import statistics as stats

#
#
# Takes in folder directory of randomly sampled gaia dr2 sources as csv files
# plots err and flux on x y axis
#
#
file_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/Gaia_Theoretical/test samples"


plots_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/gaussian"


count = 0

mag_min = 20
mag_max = 12
num_min = 5
num_max = 50
mic_amt = 2
c = 25.68836


def get_err(flux):
    mag = c - 2.5 * np.log10(flux)
    z = max([10.0 ** ((0.4) * (12 - 15)), 10.0 ** ((0.4) * (mag - 15))])
    mag_theo_err = 0.001 * (((0.04895 * z ** 2) + (1.8633 * z) + 0.0001985) ** (1 / 2))
    val_1 = mag + mag_theo_err
    val_2 = mag - mag_theo_err
    f_v_1 = 10 ** ((c - val_1) / 2.5)
    f_v_2 = 10 ** ((c - val_2) / 2.5)
    return (f_v_2 - f_v_1) / 2


for file_name in os.listdir(file_dir):
    err_vals = []
    flux_vals = []

    flux_vals_2 = []
    mag_vals = []
    err_vals_2 = []
    nums = []
    micro_bool = []
    datum = []

    print("processing file " + str(file_name) + " \U0001f44d")
    line_num = 0
    file_path = file_dir + "/" + file_name
    with open(file_path, "r") as fil:
        fil_reader = csv.reader(fil)
        for line in fil_reader:
            if line_num == 0:
                line_num = line_num + 1
                continue
            err_vals.append(float(line[3]))
            flux_vals.append(float(line[2]))

            mic_or_not = r.random()
            if mic_or_not < 0.05:
                micro_bool.append(True)
            else:
                micro_bool.append(False)
            nums.append(int(line[1]))
            datum.append((float(line[2]), int(line[1])))

    print("processing graph")
    plt.xlabel("log flux")
    plt.ylabel("log err")
    plt.title("Flux vs Error")
    blue = "No microlensing"
    red = "Microlensed 1 event by factor of " + str(mic_amt)
    green = "Actual data"
    blue_patch = mpatches.Patch(color="blue", label=blue)
    red_patch = mpatches.Patch(color="red", label=red)
    green_patch = mpatches.Patch(color="green", label=green)
    plt.legend(
        bbox_transform=plt.gcf().transFigure,
        bbox_to_anchor=(1, 1),
        handles=[blue_patch, red_patch, green_patch],
    )
    # plt.scatter(np.log(flux_vals), np.log(err_vals), c="g", s=2)

    # create cdf for fluxes
    datum.sort(key=lambda tup: tup[1])

    length = len(flux_vals) - 1
    stdev = []
    mean = []
    col = []
    col2 = []
    stdev_2 = []
    for n in range(1000):
        if micro_bool[n]:
            data = datum[r.randint(0, length)]
            flux = data[0]
            err = get_err(flux)
            num = data[1]
            s = np.random.normal(abs(flux), abs(err), abs(num))
            s_2 = np.random.poisson(abs(flux), abs(num))
            to_change = r.randint(0, num - 1)
            s[to_change] = s[to_change] * mic_amt
            stdev.append(stats.stdev(s))
            stdev_2.append(stats.stdev(s_2))
            mean.append(stats.mean(s))
            col.append("r")
            col2.append("g")
        else:
            data = datum[r.randint(0, length)]
            flux = data[0]
            err = get_err(flux)
            num = data[1]
            s = np.random.normal(abs(flux), abs(err), abs(num))
            s_2 = np.random.poisson(abs(flux), abs(num))
            to_change = r.randint(0, num - 1)
            stdev.append(stats.stdev(s))
            stdev_2.append(stats.stdev(s_2))
            mean.append(stats.mean(s))
            col.append("b")
            col2.append("g")

    print("processing graph")
    plt.scatter(np.log(mean), np.log(stdev), c=col, s=2)
    plt.scatter(np.log(mean), np.log(stdev_2), c=col, s=2)
    plt.savefig(plots_dir + "/" + file_name + ".png")
    plt.close()

