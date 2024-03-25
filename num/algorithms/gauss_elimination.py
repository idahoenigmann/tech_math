import numpy as np


def gauss_elim(matrix_A, vector_b):
    dim = len(vector_b)
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    matrix_L = np.zeros((dim, dim))

    for k in range(dim-1):
        for i in range(k+1, dim):
            matrix_L[i, k] = matrix_A[i, k] / matrix_A[k, k]
            vector_b[i] = vector_b[i] - matrix_L[i, k] * vector_b[k]
            for j in range(k+1, dim):
                matrix_A[i, j] = matrix_A[i, j] - matrix_L[i, k] * matrix_A[k, j]
        matrix_L[k, k] = 1
    matrix_L[dim-1, dim-1] = 1

    for k in range(1, dim):
        for i in range(k):
            matrix_A[k, i] = 0

    return matrix_L, matrix_A, vector_b


# TODO fix me
def gauss_elim_with_pivot(matrix_A, vector_b):
    dim = len(vector_b)
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    matrix_L = np.zeros((dim, dim))

    for k in range(dim - 1):
        v = np.abs([matrix_A[l, k] for l in range(k, dim)])
        p = k + max(enumerate(v), key=lambda x: x[1])[0]
        tmp = matrix_A[p, :]
        matrix_A[p, :] = matrix_A[k, :]
        matrix_A[k, :] = tmp

        for i in range(k + 1, dim):
            matrix_L[i, k] = matrix_A[i, k] / matrix_A[k, k]
            vector_b[i] = vector_b[i] - matrix_L[i, k] * vector_b[k]
            for j in range(k + 1, dim):
                matrix_A[i, j] = matrix_A[i, j] - matrix_L[i, k] * matrix_A[k, j]
        matrix_L[k, k] = 1
    matrix_L[dim - 1, dim - 1] = 1

    for k in range(1, dim):
        for i in range(k):
            matrix_A[k, i] = 0

    return matrix_L, matrix_A, vector_b


if __name__ == "__main__":
    matrix_A = np.matrix([[1, 4, 9], [-2, 4, 1], [8, 3, -8]])
    vector_b = np.array([1, 0, 3])

    matrix_L, matrix_U, vector_y = gauss_elim(matrix_A, vector_b)

    print(f"L:\n{matrix_L},\nU:\n{matrix_U},\nLU:\n{matrix_L.dot(matrix_U)}")
    print(f"y: {vector_y}\n\n")

    matrix_A = np.matrix([[1, 4, 9], [-2, 4, 1], [8, 3, -8]])
    vector_b = np.array([1, 0, 3])

    matrix_L, matrix_U, vector_y = gauss_elim_with_pivot(matrix_A, vector_b)

    print(f"L:\n{matrix_L},\nU:\n{matrix_U},\nLU:\n{matrix_L.dot(matrix_U)}")
    print(f"y: {vector_y}")
