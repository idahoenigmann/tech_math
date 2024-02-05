import numpy as np
import matplotlib
from matplotlib import cm
from main import read_data, pca, visualize_3d, k_nearest_neighbour


def read_patient_data(number):
    _, data_seg = read_data(f"n{number}", delimiter=",")
    sleep_stages_seg = np.loadtxt(f"data/CAPsleepdatan{number}.csv", delimiter=";", dtype=int, skiprows=1)

    length = min(data_seg.shape[0], len(sleep_stages_seg))

    data_seg = data_seg[0:length, :]
    sleep_stages_seg = sleep_stages_seg[0:length, 0]
    return data_seg, sleep_stages_seg


def get_data_and_stages(number_list):
    data = []
    sleep_stages = []
    for input_number in number_list:
        data_seg, sleep_stages_seg = read_patient_data(input_number)

        data.append(np.matrix(data_seg))
        sleep_stages.append(sleep_stages_seg)
    data = np.concatenate(data)
    sleep_stages = np.concatenate(sleep_stages)
    return data, sleep_stages


if __name__ == "__main__":
    matplotlib.use('TkAgg')
    PCA = False
    SHOW_PLOT = False

    train_input_numbers = [2, 4, 5, 7, 8, 9, 10, 11, 12, 15, 16]
    val_input_numbers = [1, 3, 6]

    train_data, train_sleep_stages = get_data_and_stages(train_input_numbers)
    val_data, val_sleep_stages = get_data_and_stages(val_input_numbers)

    print(f"Train data size: {train_data.shape}")
    print(f"Val data size: {val_data.shape}")

    # pca
    if PCA:
        print("pca started")
        pca_output, eval, evec = pca(train_data)
        print("pca finished")

        percentages = [0.5, 0.8, 0.9, 0.95]

        for per in percentages:
            print(f"The first {[idx for idx in range(len(eval)) if np.sum(eval[0:idx]) / np.sum(eval) > per][0]}"
                  f" of {len(eval)} axis explain {per * 100}% of the variance.")

        transformed_val = np.dot(val_data, evec)
    else:
        pca_output = train_data
        transformed_val = val_data

    if SHOW_PLOT:
        # train
        color_lst = ["blue", "green", "yellow", "orange", "red"]
        colors = [color_lst[train_sleep_stages[i] - 1] for i in range(train_sleep_stages.shape[0])]

        x_data = np.squeeze(np.asarray(pca_output[:, 0]))
        y_data = np.squeeze(np.asarray(pca_output[:, 1]))
        z_data = np.squeeze(np.asarray(pca_output[:, 2]))

        visualize_3d(x_data, y_data, z_data, colors, ["pc1", "pc2", "pc3"])

        # validation
        color_lst = ["blue", "green", "yellow", "orange", "red"]
        colors = [color_lst[val_sleep_stages[i] - 1] for i in range(val_sleep_stages.shape[0])]

        x_data = np.squeeze(np.asarray(transformed_val[:, 0]))
        y_data = np.squeeze(np.asarray(transformed_val[:, 1]))
        z_data = np.squeeze(np.asarray(transformed_val[:, 2]))

        visualize_3d(x_data, y_data, z_data, colors, ["pc1", "pc2", "pc3"])

    if PCA:
        pca_output = pca_output[:, 0:26]
        transformed_val = transformed_val[:, 0:26]

    states = ["S3", "S2", "S1", "REM", "awake"]
    for k in [30, 35]:
        print(f"k = {k}")
        val_matrix = np.zeros((5, 5))

        for idx in range(len(val_sleep_stages)):
            guess = k_nearest_neighbour(k, pca_output, train_sleep_stages, transformed_val[idx])
            truth = val_sleep_stages[idx]
            val_matrix[int(guess - 1), int(truth - 1)] += 1

        for i in range(5):
            row = val_matrix[i]
            print(states[i], end="")
            for e in row:
                print("", end=f" & {int(e)} ")
            print("\\\\")

        t = val_matrix[0, 0] + val_matrix[1, 1] + val_matrix[2, 2] + val_matrix[3, 3] + val_matrix[4, 4]
        print(f"{t} / {np.sum(val_matrix)} = {t/np.sum(val_matrix)}\n\n")
