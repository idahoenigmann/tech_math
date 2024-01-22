import numpy as np
import matplotlib
from matplotlib import cm
from main import read_data, pca, visualize_3d


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    input_numbers = [1]

    data = []
    sleep_stages = []
    for input_number in input_numbers:
        # read data from files
        _, data_seg = read_data(f"n{input_number}", delimiter=",")
        sleep_stages_seg = np.loadtxt(f"data/CAPsleepdatan{input_number}.csv", delimiter=";", dtype=int, skiprows=1)

        length = min(data_seg.shape[0], len(sleep_stages_seg))

        data_seg = data_seg[0:length, :]
        sleep_stages_seg = sleep_stages_seg[0:length, 0]

        data.append(np.matrix(data_seg))
        sleep_stages.append(sleep_stages_seg)
    data = np.concatenate(data)
    sleep_stages = np.concatenate(sleep_stages)

    # pca
    print("pca started")
    pca_output, _, _ = pca(data)
    print("pca finished")

    # generate color list
    color_lst = cm.jet(np.linspace(0, 1, 5))
    colors = [color_lst[sleep_stages[i] - 1] for i in range(sleep_stages.shape[0])]

    x_data = np.squeeze(np.asarray(pca_output[:, 0]))
    y_data = np.squeeze(np.asarray(pca_output[:, 1]))
    z_data = np.squeeze(np.asarray(pca_output[:, 2]))

    # show output
    visualize_3d(x_data, y_data, z_data, colors, ["pc1", "pc2", "pc3"])
