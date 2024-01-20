import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from main import read_data, pca, visualize_data


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    _, data = read_data(f"n1", delimiter=",")
    data = np.matrix(data)

    print(data[:, 0:2])

    visualize_data(data[:, 0:2], ["frequency", "amplitude"])
    pca_output, _, _ = pca(data[:, 1:].T)
    visualize_data(pca_output, ["pc1", "pc2"])

    fig, axes = plt.subplots(nrows=1, ncols=1)
    plt.subplots_adjust(hspace=0.8)

    x_data = [pca_output[idx, 0] for idx in range(pca_output.shape[0])]
    y_data = [pca_output[idx, 1] for idx in range(pca_output.shape[0])]
    axes.plot(x_data, y_data)
    axes.set_xlabel("pc1")
    axes.set_ylabel("pc2")

    plt.show()
