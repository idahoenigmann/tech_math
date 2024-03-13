import numpy as np
from csv import reader
import matplotlib
import matplotlib.pyplot as plt


def normalize(matrix):
    ret_matrix = np.copy(matrix)

    avg = np.mean(matrix, axis=0)
    var = np.var(matrix, axis=0)

    for i in range(matrix.shape[1]):
        ret_matrix[:, i] = ((matrix[:, i] - avg[0, i]) / np.sqrt(var[0, i])).ravel()
    return ret_matrix, avg, var


def pca(matrix, pc_count=None):
    # compute eigenvalues eigenvectors
    covariance_matrix = np.dot(matrix.T, matrix) / matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # sort according to eigenvalue
    key = np.argsort(eigenvalues)[::-1][:pc_count]
    eigenvalues, eigenvectors = eigenvalues[key], eigenvectors[:, key]

    return np.dot(matrix, eigenvectors), eigenvalues, eigenvectors


def k_nearest_neighbour(k, data, categories, point):
    distances_categories = np.array([[np.linalg.norm(data[idx] - point), categories[idx]] for idx in range(len(data))])
    unique, counts = np.unique(distances_categories[distances_categories[:, 0].argsort()][0:k, 1], return_counts=True)
    return unique[np.argmax(counts)]


def read_data(file_name, delimiter=" "):
    with open('data/' + file_name + '.csv') as file:
        csv_reader = reader(file, delimiter=delimiter)
        header = next(csv_reader)
        # data = np.array([[float(r) for r in row] for row in csv_reader])
    data = np.loadtxt('data/' + file_name + '.csv', delimiter=delimiter, skiprows=1, dtype=float)
    return header, data


def visualize_data(data, header, file_name="", pcs=None):
    matplotlib.use('TkAgg')

    fig, axes = plt.subplots(nrows=1, ncols=1)
    plt.subplots_adjust(hspace=0.8)

    # axes.set_title(file_name)

    x_data = [data[idx, 0] for idx in range(data.shape[0])]
    y_data = [data[idx, 1] for idx in range(data.shape[0])]
    axes.scatter(x_data, y_data, c="black", s=10)
    if pcs is not None:
        axes.arrow(x=0, y=0, dx=pcs[0][0], dy=pcs[0][1], width=.04, color="mediumseagreen")
        axes.arrow(x=0, y=0, dx=pcs[1][0], dy=pcs[1][1], width=.04, color="mediumseagreen")
        axes.text(x=pcs[0][0] * 1.5, y=pcs[0][1] * 1.5, s="PC1", color="mediumseagreen", fontsize=12)
        axes.text(x=pcs[1][0] * 1.5, y=pcs[1][1] * 1.5, s="PC2", color="mediumseagreen", fontsize=12)
    axes.set_xlabel(header[0])
    axes.set_ylabel(header[1])

    """ax_lim = max(abs(np.max(x_data)), abs(np.min(x_data)), abs(np.max(y_data)), abs(np.min(y_data))) * 1.1

    plt.xlim(-ax_lim, ax_lim)
    plt.ylim(-ax_lim, ax_lim)
    axes.set_aspect('equal', adjustable='box')"""

    if file_name != "":
        plt.savefig('data/' + file_name + '.svg')
    plt.show()


def visualize_3d(x_data, y_data, z_data, colors, labels, file_name=""):
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    # ax.plot(x_data, y_data, z_data, "darkgray")
    ax.scatter3D(x_data, y_data, z_data, c=colors)

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])

    if file_name != "":
        plt.savefig('data/' + file_name + '.png')
    plt.show()


def plot_histogram(x_data, y_data, labels, color, ax, min=None, max=None):
    if min is not None and max is not None:
        binwidth = (max - min) / 25
        bins = np.arange(min, max + binwidth, binwidth)
    else:
        bins = 25
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["white", color])
    ax.hist2d(x_data, y_data, bins=bins, cmap=cmap)

    if min is not None and max is not None:
        ax.set_xlim([min, max])
        ax.set_ylim([min, max])
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_aspect('equal', 'box')


def visualize_histogram(data, header, categories, color_list, x_var, y_var):
    fig, ax = plt.subplots(int(np.ceil(len(set(categories)) / 2)), 2)
    l = 0
    for i in range(len(set(categories))):
        category = list(set(categories))[i]
        x_data = [data[idx, x_var] for idx in range(data.shape[0]) if categories[idx] == category]
        y_data = [data[idx, y_var] for idx in range(data.shape[0]) if categories[idx] == category]

        min_x, max_x = np.min([data[:, x_var]]), np.max([data[:, x_var]])
        min_y, max_y = np.min([data[:, y_var]]), np.max([data[:, y_var]])

        plot_histogram(x_data, y_data, [header[x_var], header[y_var]], color_list[i], ax[i // 2, i % 2],
                       min(min_x, min_y), max(max_x, max_y))
        l += 1

    plt.show()
