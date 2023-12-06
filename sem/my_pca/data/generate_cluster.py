from csv import writer
import numpy as np


if __name__ == '__main__':
    dimension = 3
    cnt_clusters = 4
    cnt_points_per_cluster = 100
    variance = [3, 2, 3, 2]
    mean = [[1, 4, 0], [5, 5, 2], [-1, 4, 0], [6, -1, -2]]

    with open('cluster.csv', 'w') as file:
        csv_writer = writer(file, delimiter=" ")

        header = ["feature " + str(d) for d in range(dimension)]
        csv_writer.writerow(header)

        with open('cluster_categories.csv', 'w') as cat_file:
            csv_writer_cat = writer(cat_file, delimiter=" ")

            csv_writer_cat.writerow(["cluster"])

            for cluster in range(cnt_clusters):
                for _ in range(cnt_points_per_cluster):
                    x = [np.random.normal(loc=mean[cluster][d], scale=variance[cluster]) for d in range(dimension)]
                    csv_writer.writerow(x)
                    csv_writer_cat.writerow([cluster])