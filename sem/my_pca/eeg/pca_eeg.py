import os
import numpy as np
import matplotlib
from matplotlib import cm
from main import read_data, pca, visualize_3d


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    patient_number = 2

    start, end = np.loadtxt("data/startend.csv", delimiter=",", skiprows=1)[patient_number - 1, :]
    start, end = int(start), int(end)

    # read data from csv
    _, data = read_data(f"n{patient_number}", delimiter=",")
    data = np.matrix(data)

    # read sleep stages
    sleep_stages = np.loadtxt(f"data/CAPsleepdatan{patient_number}.csv", delimiter=";", dtype=int, skiprows=1)
    sleep_stages = sleep_stages[0:data.shape[1]-1, 0]

    # do pca or read from file
    if os.path.isfile(f"data/pca_output{patient_number}.csv"):
        pca_output = np.loadtxt(f"data/pca_output{patient_number}.csv", delimiter=",")
    else:
        print("pca started")
        pca_output, _, _ = pca(data[:, 1:].T)
        print("pca finished")
        np.savetxt(f"data/pca_output{patient_number}.csv", pca_output, delimiter=",", newline="\n")

    # show output
    color_lst = cm.jet(np.linspace(0, 1, 5))
    colors = [color_lst[sleep_stages[i] - 1] for i in range(sleep_stages.shape[0])]
    visualize_3d(pca_output[:, 0], pca_output[:, 1], pca_output[:, 2], colors, ["pc1", "pc2", "pc3"])
