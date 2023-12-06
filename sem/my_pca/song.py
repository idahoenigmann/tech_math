import numpy as np
from sklearn.decomposition import PCA
import matplotlib
import matplotlib.pyplot as plt
from csv import reader
from main import normalize, pca, read_data


def visualize_3d(x_data, y_data, z_data, colors, labels, file_name):
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    ax.scatter3D(x_data, y_data, z_data, c=colors)

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])

    plt.savefig('data/' + file_name + '.png')
    plt.show()


def plot_histogram(x_data, y_data, labels, color, ax):
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", color])
    ax.hist2d(x_data, y_data, bins=25, cmap=cmap)

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])


if __name__ == '__main__':
    file_name = "spotify_songs"
    categories = []

    header, data = read_data(file_name, ",")

    with open('data/' + file_name + '_categories.csv') as file:
        csv_reader = reader(file, delimiter=",")
        _ = next(csv_reader)
        for row in csv_reader:
            categories.append(row[0])

    category_to_color = dict()
    category_to_color["pop"] = "crimson"
    category_to_color["rap"] = "orchid"
    category_to_color["rock"] = "mediumturquoise"
    category_to_color["latin"] = "orange"
    category_to_color["r&b"] = "cornflowerblue"
    category_to_color["edm"] = "yellowgreen"

    x_var, y_var, z_var = 10, 1, 6

    # visualize original data
    x_data = [data[idx, x_var] for idx in range(data.shape[0])]
    y_data = [data[idx, y_var] for idx in range(data.shape[0])]
    z_data = [data[idx, z_var] for idx in range(data.shape[0])]
    colors = [category_to_color[categories[idx]] for idx in range(data.shape[0])]

    visualize_3d(x_data, y_data, z_data, colors, [header[x_var], header[y_var], header[z_var]], file_name+"_org")

    fig, ax = plt.subplots(2, 3)
    l = 0
    for category, color in category_to_color.items():
        x_data = [data[idx, x_var] for idx in range(data.shape[0]) if categories[idx] == category]
        y_data = [data[idx, y_var] for idx in range(data.shape[0]) if categories[idx] == category]

        plot_histogram(x_data, y_data, [header[x_var], header[y_var]], color, ax[l % 2, l % 3])
        l += 1

    plt.show()

    # pca
    data = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    # visualize pca results
    x_data = [ret_data[idx, 0] for idx in range(ret_data.shape[0])]
    y_data = [ret_data[idx, 1] for idx in range(ret_data.shape[0])]
    z_data = [ret_data[idx, 2] for idx in range(ret_data.shape[0])]
    colors = [category_to_color[categories[idx]] for idx in range(ret_data.shape[0])]

    visualize_3d(x_data, y_data, z_data, colors, ["PC 1", "PC 2", "PC 3"], file_name+"_pca")

    fig, ax = plt.subplots(2, 3)
    l = 0
    for category, color in category_to_color.items():
        x_data = [ret_data[idx, 0] for idx in range(ret_data.shape[0]) if categories[idx] == category]
        y_data = [ret_data[idx, 1] for idx in range(ret_data.shape[0]) if categories[idx] == category]

        plot_histogram(x_data, y_data, ["PC 1", "PC 2"], color, ax[l % 2, l % 3])
        l += 1

    plt.show()
