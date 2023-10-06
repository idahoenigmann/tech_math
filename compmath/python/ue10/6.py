import numpy as np


def save_matrix(matrix, file_name):
    with open(file_name, "w") as file:
        for e in matrix:
            file.write(",".join(str(n) for n in e))
            file.write("\n")


def load_matrix(file_name):
    matrix = []
    with open(file_name, "r") as file:
        for line in file.read().splitlines():
            matrix.append([float(e) for e in line.split(",")])
    return np.array(matrix)


if __name__ == "__main__":
    matrix = np.array([[42, 9, -11], [0, 0, 10], [-1, 3, -21]])

    save_matrix(matrix, "matrix.dat")
    new_matrix = load_matrix("matrix.dat")

    print(new_matrix)

    np.savetxt("np_matrix.dat", matrix)
    new_np_matrix = np.loadtxt("np_matrix.dat")
    print(new_np_matrix)
