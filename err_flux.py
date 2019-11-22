import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches

#
#
# Takes in folder directory of randomly sampled gaia dr2 sources as csv files
# plots err and flux on x y axis
#
#
file_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/Gaia_Theoretical/test samples"


plots_dir = "/Users/vineetkamat/Documents/College/Fifth Semester/Research/flux_err_plots_data"


count = 0

for file_name in os.listdir(file_dir):
    err_vals = []
    flux_vals = []
    print("processing file " + str(file_name) + " \U0001f44d")
    line_num = 0
    file_path = file_dir + "/" + file_name
    with open(file_path, "r") as fil:
        fil_reader = csv.reader(fil)
        for line in fil_reader:
            if line_num == 0:
                line_num = line_num + 1
                continue

            err = np.log(float(line[3]))
            flux = np.log(float(line[2]))
            err_vals.append(err)
            flux_vals.append(flux)

    print("processing graph")
    plt.scatter(x=flux_vals, y=err_vals,s=1)
    plt.xlabel("Log Flux")
    plt.ylabel("Log Error")
    plt.title("Flux vs Error")
    ax = plt.gca()
    plt.savefig(plots_dir + "/" + file_name + ".png")
    plt.close()
    count = count + 1

