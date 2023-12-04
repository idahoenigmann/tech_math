import numpy as np
from sklearn.decomposition import PCA
from main import pca, normalize, read_data, visualize_data


if __name__ == '__main__':
    file_name = "fossil_fish_teeth"
    header, data = read_data(file_name)

    data = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    pca = PCA(n_components=2).fit(data)
    ref_data = np.dot(data, pca.components_.T)

    visualize_data(data, header, file_name, pcs)
    visualize_data(data, header, file_name, pca.components_.T)

    header = ["PC1", "PC2"]
    visualize_data(ret_data, header, file_name)
    visualize_data(ref_data, header, file_name)
