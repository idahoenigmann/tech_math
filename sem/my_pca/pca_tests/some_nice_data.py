from csv import writer
import numpy as np
from main import pca, normalize, read_data, visualize_data
from sklearn.decomposition import PCA


def generate_data(file_name):
    with open('data/' + file_name + '.csv', 'w') as file:
        csv_writer = writer(file, delimiter=",")
        csv_writer.writerow(["x position", "y position"])
        for k in range(-30, 35):
            x = k/10 + np.random.uniform(-0.2, 0.2)
            y = 1 * k/10 + np.random.uniform(-0.3, 0.3)

            if np.random.random() > 0.8:
                x += np.random.uniform(-1, 1)
            if np.random.random() > 0.8:
                y += np.random.uniform(-1, 1)

            csv_writer.writerow([x, y])
        for k in range(-20, 25):
            x = k/10 + np.random.uniform(-0.1, 0.1)
            y = 3 * k/10 + np.random.uniform(-0.4, 0.4)

            if np.random.random() > 0.8:
                x += np.random.uniform(-1.5, 1.5)
            if np.random.random() > 0.8:
                y += np.random.uniform(-1.5, 1.5)

            csv_writer.writerow([x, y])


if __name__ == '__main__':
    file_name = "non_orthogonal"
    generate_data(file_name)
    header, data = read_data(file_name)

    # visualize_data(data, header, file_name=file_name + "_org")

    data, _, _ = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    pca = PCA(n_components=2).fit(data)
    ref_data = np.dot(data, pca.components_.T)

    visualize_data(data, header, file_name=file_name + "_pc", pcs=pcs[::-1])
    # visualize_data(data, header, file_name=file_name + "_ref_pc", pcs=pca.components_.T)
    # visualize_data(ret_data, ["PC1", "PC2"], file_name=file_name + "_pca")
    # visualize_data(ref_data, ["PC1", "PC2"], file_name=file_name + "_ref_pca")
