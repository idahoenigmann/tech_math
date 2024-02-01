import numpy as np
import matplotlib
from matplotlib import cm
from main import read_data, pca, visualize_3d, visualize_histogram


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    input_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16]

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

    print(f"Data size: {data.shape}")

    # pca
    print("pca started")
    pca_output, eval, evec = pca(data)
    print("pca finished")

    print(f"The first {[idx for idx in range(len(eval)) if np.sum(eval[0:idx]) / np.sum(eval) > 0.5][0]} of {len(eval)}"
          f" axis explain 50% of the variance.")
    print(f"The first {[idx for idx in range(len(eval)) if np.sum(eval[0:idx]) / np.sum(eval) > 0.8][0]} of {len(eval)}"
          f" axis explain 80% of the variance.")
    print(f"The first {[idx for idx in range(len(eval)) if np.sum(eval[0:idx]) / np.sum(eval) > 0.9][0]} of {len(eval)}"
          f" axis explain 90% of the variance.")
    print(f"The first {[idx for idx in range(len(eval)) if np.sum(eval[0:idx]) / np.sum(eval) > 0.95][0]} of {len(eval)}"
          f" axis explain 95% of the variance.")

    # generate color list
    color_lst = ["blue", "green", "yellow", "orange", "red"]
    colors = [color_lst[sleep_stages[i] - 1] for i in range(sleep_stages.shape[0])]

    x_data = np.squeeze(np.asarray(pca_output[:, 0]))
    y_data = np.squeeze(np.asarray(pca_output[:, 1]))
    z_data = np.squeeze(np.asarray(pca_output[:, 2]))

    # show output
    visualize_3d(x_data, y_data, z_data, colors, ["pc1", "pc2", "pc3"])

    # visualize_histogram([x_data, y_data], ["pc1", "pc2"], colors, color_lst, 0, 1)
