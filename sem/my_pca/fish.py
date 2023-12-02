import numpy as np
from sklearn.decomposition import PCA
import matplotlib
import matplotlib.pyplot as plt
from csv import reader
from matplotlib.lines import Line2D


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
    eigenvalues, eigenvectors = eigenvalues[key], eigenvectors[:, key]

    return np.dot(data, eigenvectors), eigenvalues, eigenvectors


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    file_name = "fossil_fish_teeth"
    categories = []

    with open('data/' + file_name + '.csv') as file:
        csv_reader = reader(file, delimiter=" ")
        header = next(csv_reader)
        data = np.array([[float(r) for r in row] for row in csv_reader])

    data = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    pca = PCA(n_components=2).fit(data)
    ref_data = np.dot(data, pca.components_.T)

    header = ["PC1", "PC2"]

    # visualize
    fig, axes = plt.subplots(nrows=1, ncols=1)
    plt.subplots_adjust(hspace=0.8)

    axes.set_title("PCA on fossil fish teeth data")

    x_data = [ret_data[idx, 0] for idx in range(ret_data.shape[0])]
    y_data = [ret_data[idx, 1] for idx in range(ret_data.shape[0])]
    axes.scatter(x_data, y_data, c="black", s=10)
    # axes.annotate(text='pc1', xy=(0, 0), xytext=pcs[0], arrowprops=dict(arrowstyle='<-', color="mediumseagreen"), c="mediumseagreen")
    # axes.annotate(text='pc2', xy=(0, 0), xytext=pcs[1], arrowprops=dict(arrowstyle='<-', color="mediumseagreen"), c="mediumseagreen")
    # axes.annotate(text='pc1', xy=(0, 0), xytext=pca.components_[0][1:3], arrowprops=dict(arrowstyle='<-', color="orange"), c="orange")
    # axes.annotate(text='pc2', xy=(0, 0), xytext=pca.components_[1][1:3], arrowprops=dict(arrowstyle='<-', color="orange"), c="orange")
    axes.set_xlabel(header[0])
    axes.set_ylabel(header[1])

    plt.savefig('data/' + file_name + '.png')
    plt.show()
