import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from csv import reader
from main import read_data


if __name__ == '__main__':
    """
        call python generate_cluster.py with dim=2 in advance
    """

    file_name = "cluster"
    categories = []

    header, data = read_data(file_name, ",")

    with open('data/' + file_name + '_categories.csv') as file:
        csv_reader = reader(file, delimiter=" ")
        _ = next(csv_reader)
        for row in csv_reader:
            categories.append(int(row[0]))

    cnt_categories = len(set(categories))
    color_list = ["crimson", "orchid", "mediumturquoise", "orange", "cornflowerblue", "yellowgreen"]
    marker_list = ["^", "*", "o", ">", "s", "<", "D"]

    point = [-1, -1]
    k = 10

    # visualize original data
    x_data = [data[idx, 0] for idx in range(data.shape[0])]
    y_data = [data[idx, 1] for idx in range(data.shape[0])]
    colors = [color_list[categories[idx]] for idx in range(data.shape[0])]
    markers = [marker_list[categories[idx]] for idx in range(data.shape[0])]

    matplotlib.use('TkAgg')

    fig, axes = plt.subplots(nrows=1, ncols=1)
    plt.subplots_adjust(hspace=0.8)

    distances_idx = np.array([[np.linalg.norm(data[idx] - point), idx] for idx in range(len(data))])
    closest = distances_idx[distances_idx[:, 0].argsort()][0:k, 1]

    for idx in closest:
        idx = int(idx)
        axes.plot([x_data[idx], point[0]], [y_data[idx], point[1]], linestyle="-", c="grey", zorder=0)

    k = 0
    for c in set(categories):
        x = [x_data[idx] for idx in range(data.shape[0]) if categories[idx] == c]
        y = [y_data[idx] for idx in range(data.shape[0]) if categories[idx] == c]
        axes.scatter(x, y, c=color_list[k], marker=marker_list[k], s=20, zorder=1)
        k += 1
    axes.scatter(point[0], point[1], c="black", s=20, zorder=1)

    ax_lim = max(abs(np.max(x_data)), abs(np.min(x_data)), abs(np.max(y_data)), abs(np.min(y_data))) * 1.1

    plt.xlim(-ax_lim, ax_lim)
    plt.ylim(-ax_lim, ax_lim)
    axes.set_aspect('equal', adjustable='box')

    file_name = "k_nearest_neighbors"
    if file_name != "":
        plt.savefig('data/' + file_name + '.png')
    plt.show()
