import numpy as np


def solve_upper_triangle_system(matrix_A, vector_b):
    dim = len(vector_b)
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    vector_x = np.zeros(dim)
    for j in range(dim-1, -1, -1):
        vector_x[j] = (vector_b[j] - np.sum([matrix_A[j, k] * vector_x[k] for k in range(j+1, dim)])) / matrix_A[j, j]
    return vector_x


if __name__ == "__main__":
    matrix_A_1 = np.matrix([[3, 1, 6],
                          [0, 3, 4],
                          [0, 0, 2]])
    vector_b_1 = np.array([1, 0, 3])

    vector_x_1 = solve_upper_triangle_system(matrix_A_1, vector_b_1)

    print(f"x = {vector_x_1}, Ax = {matrix_A_1.dot(vector_x_1)}, b = {vector_b_1}")

