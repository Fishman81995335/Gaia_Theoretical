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


plots_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/new"


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
    c = 25.68836
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
            err_vals.append(float(line[3]) * (np.sqrt(float(line[1]))))
            flux_vals.append(float(line[2]))

            mic_or_not = r.random()
            if mic_or_not < 0.05:
                micro_bool.append(True)
            else:
                micro_bool.append(False)
            nums.append(int(line[1]))
            datum.append(
                (
                    float(line[2]),
                    int(line[1]),
                    float(line[4]),
                    int(line[0]),
                    float(line[3]),
                )
            )

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
    plt.scatter(np.log10(flux_vals), np.log10(err_vals), c="g", s=2)

    # create cdf for fluxes
    datum.sort(key=lambda tup: tup[1])

    length = len(flux_vals) - 1
    stdev = []
    mean = []
    mean2 = []
    col = []
    rat = []
    for n in range(1000):
        data = datum[r.randint(0, length)]
        flux = data[0]
        mag = data[2]
        if micro_bool[n]:
            err = get_err(flux)
            err2 = get_err_mag(mag)
            num = data[1]
            s = np.random.normal(abs(flux), abs(err), abs(num))
            to_change = r.randint(0, num - 1)
            s[to_change] = s[to_change] * mic_amt
            theo_err = stats.stdev(s)
            stdev.append(theo_err)
            m = stats.mean(s)
            mean.append(m)
            col.append("r")
        else:
            err = get_err(flux)
            err2 = get_err_mag(mag)
            og_err = data[4]
            num = data[1]
            s = np.random.normal(abs(flux), abs(err), abs(num))
            theo_err = stats.stdev(s)
            stdev.append(theo_err)
            m = stats.mean(s)
            mean.append(m)
            col.append("b")

    print("processing graph")
    plt.scatter(np.log10(mean), np.log10(stdev), c=col, s=2)
    plt.savefig(plots_dir + "/" + file_name + ".png", dpi=300)
    plt.close()

    # plt.scatter(np.log10(mean2), np.log10(rat))
    # plt.show()
    # plt.close()

