import numpy as np


def cholesky(matrix_A):
    dim = matrix_A.shape[0]
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    matrix_L = np.zeros((dim, dim))

    for k in range(dim):
        matrix_L[k, k] = np.sqrt(matrix_A[k, k] - np.sum([matrix_L[k, j]**2 for j in range(k-1)]))
        for i in range(k+1, dim):
            matrix_L[i, k] = (matrix_A[i, k] - np.sum([matrix_L[i, j] * np.conjugate(matrix_L[k, j]) for j in range(k-1)])) / matrix_L[k, k]

    return matrix_L


if __name__ == "__main__":
    matrix_A = np.matrix([[1, -2, 9], [-2, 6, 3], [9, 3, 652]])

    print(matrix_A)

    matrix_L = cholesky(matrix_A)
    print(f"L:\n{matrix_L},\nLL^H^T:\n{matrix_L.dot(np.transpose(np.conjugate(matrix_L)))}")
