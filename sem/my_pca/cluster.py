from main import *


if __name__ == '__main__':
    """
    call python generate_cluster.py with dim=3 in advance
    """

    file_name = "cluster"
    categories = []

    header, data = read_data(file_name, ",")

    with open('data/' + file_name + '_categories.csv') as file:
        csv_reader = reader(file, delimiter=" ")
        _ = next(csv_reader)
        for row in csv_reader:
            categories.append(int(row[0]))

    cnt_categories = len(set(categories))
    color_list = ["crimson", "orchid", "mediumturquoise", "orange", "cornflowerblue", "yellowgreen"]

    x_var, y_var, z_var = 0, 1, 2

    # visualize original data
    x_data = [data[idx, x_var] for idx in range(data.shape[0])]
    y_data = [data[idx, y_var] for idx in range(data.shape[0])]
    z_data = [data[idx, z_var] for idx in range(data.shape[0])]
    colors = [color_list[categories[idx]] for idx in range(data.shape[0])]

    visualize_3d(x_data, y_data, z_data, colors, [header[x_var], header[y_var], header[z_var]], file_name+"_org")
    visualize_histogram(data, header, categories, color_list, x_var, y_var)

    # pca
    data, avg, var = normalize(np.matrix(data))
    ret_data, evs, pcs = pca(data)

    # visualize pca results
    x_data = [ret_data[idx, 0] for idx in range(ret_data.shape[0])]
    y_data = [ret_data[idx, 1] for idx in range(ret_data.shape[0])]
    z_data = [ret_data[idx, 2] for idx in range(ret_data.shape[0])]
    colors = [color_list[categories[idx]] for idx in range(ret_data.shape[0])]

    visualize_3d(x_data, y_data, z_data, colors, ["PC 1", "PC 2", "PC 3"], file_name+"_pca")
    visualize_histogram(ret_data, ["PC 1", "PC 2"], categories, color_list, 0, 1)

    point = [0, 0, 0]
    point = (np.array(point) - avg) / var
    point = np.dot(point, pcs)

    print(k_nearest_neighbour(15, ret_data, categories, point))
