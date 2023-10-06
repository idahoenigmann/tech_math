import numpy as np


def norm(matrix, p):
    return (np.sum(matrix ** p)) ** (1/p)


if __name__ == "__main__":
    matrix = np.identity(10)
    print(norm(matrix, 2))

    matrix = np.matrix([[1, 2, 3], [2, 4, 8], [-1, 8, -4]])
    print(norm(matrix, 3))
