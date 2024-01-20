import os
import numpy as np
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
from main import read_data, pca, visualize_3d


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    # read data from csv
    _, data = read_data(f"n1", delimiter=",")
    data = np.matrix(data)

    # read sleep stages
    sleep_stages = np.loadtxt("data/CAPsleepdatan01.csv", delimiter=";", dtype=int, skiprows=1)
    sleep_stages = sleep_stages[5:452, 0]
    color_lst = cm.jet(np.linspace(0, 1, 5))
    colors = [color_lst[sleep_stages[i] - 1] for i in range(sleep_stages.shape[0])]

    # do pca or read from file
    if os.path.isfile("data/pca_output.csv"):
        pca_output = np.loadtxt("data/pca_output.csv", delimiter=",")
    else:
        print("pca started")
        pca_output, _, _ = pca(data[:, 1:].T)
        print("pca finished")
        np.savetxt("data/pca_output.csv", pca_output, delimiter=",", newline="\n")

    # show output
    visualize_3d(pca_output[:, 0], pca_output[:, 1], pca_output[:, 2], colors, ["pc1", "pc2", "pc3"])
