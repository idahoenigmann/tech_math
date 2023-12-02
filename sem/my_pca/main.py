import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
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

    file_name = "spotify_songs"
    categories = []

    with open('data/' + file_name + '.csv') as file:
        csv_reader = reader(file, delimiter=",")
        header = next(csv_reader)
        data = np.array([[float(r) for r in row] for row in csv_reader])

    with open('data/' + file_name + '_categories.csv') as file:
        csv_reader = reader(file, delimiter=",")
        _ = next(csv_reader)
        idx = 0
        for row in csv_reader:
            categories.append(row[0])

    data = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    pca = PCA(n_components=2).fit(data)
    ref_data = np.dot(data, pca.components_.T)

    """
    print("cluster original data")
    kmeans_org = KMeans(init="random", n_clusters=6, n_init=10, max_iter=100, random_state=42)
    kmeans_org.fit(data)

    result = {"pop": [], "rap": [], "rock": [], "latin": [], "r&b": [], "edm": []}
    for l in range(len(kmeans_org.labels_)):
        result[categories[l]].append(kmeans_org.labels_[l])

    for genre, values in result.items():
        print(genre, end=",")
        print(f"{values.count(0)},{values.count(1)},{values.count(2)},{values.count(3)},"
              f"{values.count(4)},{values.count(5)}", end="\n")

    print("cluster pca data")
    kmeans_pca = KMeans(init="random", n_clusters=6, n_init=10, max_iter=100, random_state=42)
    kmeans_pca.fit(ref_data)

    result = {"pop": [], "rap": [], "rock": [], "latin": [], "r&b": [], "edm": []}
    for l in range(len(kmeans_pca.labels_)):
        result[categories[l]].append(kmeans_pca.labels_[l])

    for genre, values in result.items():
        print(genre, end=",")
        print(f"{values.count(0)},{values.count(1)},{values.count(2)},{values.count(3)},"
              f"{values.count(4)},{values.count(5)}", end="\n")
    """

    x_var = 1
    y_var = 10
    z_var = 5

    category_to_color = dict()
    category_to_color["pop"] = "crimson"
    category_to_color["rap"] = "orchid"
    category_to_color["rock"] = "mediumturquoise"
    category_to_color["latin"] = "orange"
    category_to_color["r&b"] = "cornflowerblue"
    category_to_color["edm"] = "yellowgreen"

    # visualize
    fig, axes = plt.subplots(nrows=3, ncols=1)
    plt.subplots_adjust(hspace=0.8)

    subplot1 = axes[0]
    subplot1.set_title("original data")

    x_data = [data[idx, x_var] for idx in range(data.shape[0])]
    y_data = [data[idx, y_var] for idx in range(data.shape[0])]
    colors = [category_to_color[categories[idx]] for idx in range(data.shape[0])]
    subplot1.scatter(x_data, y_data, c=colors, s=2)
    # subplot1.annotate(text='pc1', xy=(0, 0), xytext=pcs[0][1:3], arrowprops=dict(arrowstyle='<-', color="green"), c="green")
    # subplot1.annotate(text='pc2', xy=(0, 0), xytext=pcs[1][1:3], arrowprops=dict(arrowstyle='<-', color="green"), c="green")
    # subplot1.annotate(text='pc1', xy=(0, 0), xytext=pca.components_[0][1:3], arrowprops=dict(arrowstyle='<-', color="orange"), c="orange")
    # subplot1.annotate(text='pc2', xy=(0, 0), xytext=pca.components_[1][1:3], arrowprops=dict(arrowstyle='<-', color="orange"), c="orange")
    subplot1.set_xlabel(header[x_var])
    subplot1.set_ylabel(header[y_var])

    legend_elements = []
    for cat, col in category_to_color.items():
        legend_elements.append(Line2D([0], [0], marker='o', color=col, label=cat, markerfacecolor=col, markersize=2))
    subplot1.legend(handles=legend_elements)
    # subplot1.set_aspect('equal', adjustable='box')

    subplot2 = axes[1]
    subplot2.set_title("pca data")
    x_data = [ret_data[idx, 0] for idx in range(data.shape[0])]
    y_data = [ret_data[idx, 1] for idx in range(data.shape[0])]
    subplot2.scatter(x_data, y_data, c=colors, s=2)
    subplot2.set_xlabel("PC1")
    subplot2.set_ylabel("PC2")
    # subplot2.set_aspect('equal', adjustable='box')

    subplot3 = axes[2]
    subplot3.set_title("ref pca data")
    x_data = [ref_data[idx, 0] for idx in range(data.shape[0])]
    y_data = [ref_data[idx, 1] for idx in range(data.shape[0])]
    subplot3.scatter(x_data, y_data, c=colors, s=2)
    subplot3.set_xlabel("PC1")
    subplot3.set_ylabel("PC2")
    # subplot3.set_aspect('equal', adjustable='box')"""

    plt.savefig('data/' + file_name + '.png')
    plt.show()
