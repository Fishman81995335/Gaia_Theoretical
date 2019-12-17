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


plots_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/new2"


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
            flux = float(line[2])
            error = float(line[3])
            num = int(line[1])
            source = int(line[0])
            magnitude = float(line[4])

            mic_or_not = r.random()
            if mic_or_not < 0.05:
                micro_bool.append(True)
            else:
                micro_bool.append(False)
            nums.append(int(line[1]))

            err_vals.append(error * (np.sqrt(num)))
            flux_vals.append(flux)
            datum.append([flux, num, magnitude, source, error])

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

# begin calculations

    length = len(flux_vals) - 1
    stdev = []
    mean = []
    mean2 = []
    col = []
    rat = []
    for n in range(len(datum)):
        data = datum[n]
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
            mean.append(flux)
            col.append("r")
        else:
            err = get_err(flux)
            err2 = get_err_mag(mag)
            og_err = err_vals[n]
            num = data[1]
            s = np.random.normal(abs(flux), abs(err), abs(num))
            theo_err = stats.stdev(s)
            stdev.append(theo_err)
            mean.append(flux)
            mean2.append(flux)

            # Assert statements
            if flux != data[0]:
                print("OH NO")
            if flux != flux_vals[n]:
                print("oh no")
                print(flux)
                print(flux_vals[n])

            rat.append(theo_err / og_err)
            if (theo_err / og_err) > 1:
                print(data[3])
                col.append("cyan")
            else:
                col.append("b")
        if err - err2 > 0.1:
            print("Wrong")

    print("processing graph")
    plt.scatter(np.log10(flux_vals), np.log10(stdev), c=col, s=2)
    plt.savefig(plots_dir + "/" + file_name + ".png", dpi=300)
    plt.close()

    plt.scatter(np.log10(mean2), np.log10(rat))
    plt.savefig(plots_dir + "/" + file_name + "_rats" ".png", dpi=300)
    plt.close()

