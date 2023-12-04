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
    return ret_matrix


def pca(matrix, pc_count=None):
    # compute eigenvalues eigenvectors
    covariance_matrix = np.dot(matrix.T, matrix) / matrix.shape[0]
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # sort according to eigenvalue
    key = np.argsort(eigenvalues)[::-1][:pc_count]
    eigenvalues, eigenvectors = eigenvalues[key], eigenvectors[:,key]

    return np.dot(matrix, eigenvectors), eigenvalues, eigenvectors


def read_data(file_name, delimiter=" "):
    with open('data/' + file_name + '.csv') as file:
        csv_reader = reader(file, delimiter=delimiter)
        header = next(csv_reader)
        data = np.array([[float(r) for r in row] for row in csv_reader])
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

    ax_lim = max(abs(np.max(x_data)), abs(np.min(x_data)), abs(np.max(y_data)), abs(np.min(y_data))) * 1.1

    plt.xlim(-ax_lim, ax_lim)
    plt.ylim(-ax_lim, ax_lim)
    axes.set_aspect('equal', adjustable='box')

    if file_name != "":
        plt.savefig('data/' + file_name + '.png')
    plt.show()
