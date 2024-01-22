import os
import numpy as np
import matplotlib
from matplotlib import cm
from main import read_data, pca, visualize_3d


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    input_number = 1

    # do pca or read from file
    if not os.path.isfile(f"data/pca_output{input_number}.csv"):
        # read data from csv
        _, data = read_data(f"n{input_number}", delimiter=",")
        data = np.matrix(data)

        print("pca started")
        pca_output, _, _ = pca(data)
        print("pca finished")
        np.savetxt(f"data/pca_output{input_number}.csv", pca_output, delimiter=",", newline="\n")

    pca_output = np.loadtxt(f"data/pca_output{input_number}.csv", delimiter=",")

    # read sleep stages
    sleep_stages = np.loadtxt(f"data/CAPsleepdatan{input_number}.csv", delimiter=";", dtype=int, skiprows=1)

    sleep_stages = sleep_stages[0:pca_output.shape[0], 0]

    # generate color list
    color_lst = cm.jet(np.linspace(0, 1, 5))
    colors = [color_lst[sleep_stages[i] - 1] for i in range(sleep_stages.shape[0])]

    # show output
    visualize_3d(pca_output[:, 0], pca_output[:, 1], pca_output[:, 2], colors, ["pc1", "pc2", "pc3"])
