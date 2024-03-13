import numpy as np


if __name__ == '__main__':
    dimension = 2
    cnt_clusters = 3
    cnt_points_per_cluster = 10
    variance = [5, 3, 4, 7, 7]
    mean = [[4, 4, 0], [5, 6, 2], [-1, -3, 0], [6, -1, -2], [0, 0, 0]]

    a = np.zeros(shape=(dimension, dimension))
    for i in range(dimension):
        a[i, i:dimension] = np.random.random(size=(dimension-i))
    b = np.zeros(shape=(dimension, dimension))
    for i in range(dimension):
        b[i, 0:(i+1)] = np.random.random(size=(i+1))
    basis_change = a*b + np.random.random(size=(dimension, dimension))

    header = ",".join(["feature " + str(d) for d in range(dimension)])
    data = np.zeros((cnt_clusters * cnt_points_per_cluster, dimension))
    categories = np.zeros((cnt_clusters * cnt_points_per_cluster))

    for cluster in range(cnt_clusters):
        cluster_data = np.matrix([[np.random.normal(loc=mean[cluster][d], scale=variance[cluster])
                                   for d in range(dimension)] for _ in range(cnt_points_per_cluster)])
        data[cluster * cnt_points_per_cluster:(cluster + 1) * cnt_points_per_cluster, :] = cluster_data
        categories[cluster * cnt_points_per_cluster: (cluster + 1) * cnt_points_per_cluster] =\
            [cluster for _ in range(cnt_points_per_cluster)]

    # data = np.dot(data, basis_change)

    np.savetxt("cluster.csv", data, delimiter=",", header=header, fmt="%10.5f")
    np.savetxt("cluster_categories.csv", categories, delimiter=",", header="category", fmt="%d")
