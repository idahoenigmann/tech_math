import numpy as np


def crout(matrix_A):
    dim = matrix_A.shape[0]
    if matrix_A.shape != (dim, dim):
        raise ValueError("Matrix is not square.")

    matrix_L = np.zeros((dim, dim))
    matrix_U = np.zeros((dim, dim))

    for i in range(dim):
        for k in range(i, dim):
            matrix_U[i, k] = matrix_A[i, k] - np.sum([matrix_L[i, j] * matrix_U[j, k] for j in range(i)])
        for k in range(i+1, dim):
            matrix_L[k, i] = (matrix_A[k, i] - np.sum([matrix_L[k, j] * matrix_U[j, i] for j in range(i)])) / matrix_U[i, i]
        matrix_L[i, i] = 1
    return matrix_L, matrix_U


if __name__ == "__main__":
    matrix_A = np.matrix([[1, 4, 9], [-2, 4, 1], [8, 3, -8]])

    matrix_L, matrix_U = crout(matrix_A)
    print(f"L:\n{matrix_L},\nU:\n{matrix_U},\nLU:\n{matrix_L.dot(matrix_U)}")
