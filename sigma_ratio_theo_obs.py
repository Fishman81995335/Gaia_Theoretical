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
file_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/Gaia_Theoretical/smaller test samples"


plots_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/ml_nml_2"


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


def get_err_mag(mag):
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

    mag_vals = []
    nums = []
    datum = []
    sources = []

    print("processing file " + str(file_name) + " \U0001f44d")
    line_num = 0
    file_path = file_dir + "/" + file_name
    m = 0
    with open(file_path, "r") as fil:
        fil_reader = csv.reader(fil)
        for line in fil_reader:
            m = m + 1
            if line_num == 0:
                line_num = line_num + 1
                continue
            err_vals.append(float(line[3]) * (np.sqrt(float(line[1]))))
            flux_vals.append(float(line[2]))
            nums.append(int(line[1]))
            datum.append((float(line[2]), int(line[1]), float(line[4]), int(line[0])))
            sources.append(int(line[0]))

    print("processing graph")

    # create cdf for fluxes
    datum.sort(key=lambda tup: tup[1])

    length = len(flux_vals) - 1
    stdev_rat = []
    means = []
    col = []
    nums = []
    for n in range(len(datum)):

        data = datum[n]
        flux = data[0]
        mag = data[2]
        theo_err_2 = get_err(flux)
        theo_err = get_err_mag(mag)
        num = data[1]
        s = np.random.normal(abs(flux), abs(theo_err), abs(num))
        theo_std = stats.stdev(s)
        rat = theo_std / err_vals[n]
        stdev_rat.append(rat)
        means.append(flux)
        nums.append(num)

    print("processing graph")
    plt.xlabel("log flux")
    plt.ylabel("log [theoretical err / experimental]")
    plt.title("Log Flux vs Error Rat")
    green = "Ratio of theoretical microlensed sigma to real sigma"
    green_patch = mpatches.Patch(color="green", label=green)
    plt.legend(
        bbox_transform=plt.gcf().transFigure,
        bbox_to_anchor=(1, 1),
        handles=[green_patch],
    )
    plt.scatter(np.log10(means), np.log10(stdev_rat), c="g", s=2)
    plt.savefig(plots_dir + "/" + file_name + " by mean" ".png", dpi=300)
    plt.close()

    plt.xlabel("num obs")
    plt.ylabel("log [theoretical err / experimental]")
    plt.title("Num Obs vs Error Rat")
    red = "Ratio of theoretical microlensed sigma to real sigma" + str(mic_amt)
    red_patch = mpatches.Patch(color="red", label=red)
    plt.legend(
        bbox_transform=plt.gcf().transFigure, bbox_to_anchor=(1, 1), handles=[red_patch]
    )
    plt.scatter(nums, np.log10(stdev_rat), c="r", s=2)
    plt.savefig(plots_dir + "/" + file_name + " by num" ".png", dpi=300)
    plt.close()
    print(m)
