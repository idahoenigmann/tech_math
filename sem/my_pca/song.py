import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from csv import reader
from matplotlib.lines import Line2D
from main import normalize, pca, read_data


if __name__ == '__main__':
    file_name = "spotify_songs"
    categories = []

    header, data = read_data(file_name, ",")

    with open('data/' + file_name + '_categories.csv') as file:
        csv_reader = reader(file, delimiter=",")
        _ = next(csv_reader)
        for row in csv_reader:
            categories.append(row[0])

    data = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    pca = PCA(n_components=2).fit(data)
    ref_data = np.dot(data, pca.components_.T)

    x_var, y_var = 1, 10

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
    subplot1.set_xlabel(header[x_var])
    subplot1.set_ylabel(header[y_var])

    legend_elements = []
    for cat, col in category_to_color.items():
        legend_elements.append(Line2D([0], [0], marker='o', color=col, label=cat, markerfacecolor=col, markersize=2))
    subplot1.legend(handles=legend_elements)

    subplot2 = axes[1]
    subplot2.set_title("pca data")
    x_data = [ret_data[idx, 0] for idx in range(data.shape[0])]
    y_data = [ret_data[idx, 1] for idx in range(data.shape[0])]
    subplot2.scatter(x_data, y_data, c=colors, s=2)
    subplot2.set_xlabel("PC1")
    subplot2.set_ylabel("PC2")

    subplot3 = axes[2]
    subplot3.set_title("ref pca data")
    x_data = [ref_data[idx, 0] for idx in range(data.shape[0])]
    y_data = [ref_data[idx, 1] for idx in range(data.shape[0])]
    subplot3.scatter(x_data, y_data, c=colors, s=2)
    subplot3.set_xlabel("PC1")
    subplot3.set_ylabel("PC2")

    plt.savefig('data/' + file_name + '.png')
    plt.show()
