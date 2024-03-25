import numpy as np


def solve_upper_triangle_system(matrix_A, vector_b):
    dim = len(vector_b)
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    vector_x = np.zeros(dim)
    for j in range(dim-1, -1, -1):
        vector_x[j] = (vector_b[j] - np.sum([matrix_A[j, k] * vector_x[k] for k in range(j+1, dim)])) / matrix_A[j, j]
    return vector_x


def solve_lower_triangle_system(matrix_A, vector_b):
    dim = len(vector_b)
    if matrix_A.shape != (dim, dim):
        raise ValueError("Dimension of matrix does not match dimension of vector.")

    vector_x = np.zeros(dim)
    for j in range(0, dim):
        vector_x[j] = (vector_b[j] - np.sum([matrix_A[j, k] * vector_x[k] for k in range(0, j)])) / matrix_A[j, j]
    return vector_x


if __name__ == "__main__":
    matrix_A = np.matrix([[3, 1, 6], [0, 3, 4], [0, 0, 2]])
    vector_b = np.array([1, 0, 3])
    vector_x = solve_upper_triangle_system(matrix_A, vector_b)

    print(f"x = {vector_x}, Ax = {matrix_A.dot(vector_x)}, b = {vector_b}")

    matrix_A = np.matrix([[-5, 0, 2], [0, 4, -4], [0, 0, 1]])
    vector_b = np.array([8, -5, 3])
    vector_x = solve_upper_triangle_system(matrix_A, vector_b)

    print(f"x = {vector_x}, Ax = {matrix_A.dot(vector_x)}, b = {vector_b}")

    matrix_A = np.matrix([[-5, 0, 0], [1, 4, 0], [-7, 6, -2]])
    vector_b = np.array([-9, 3, -8])
    vector_x = solve_lower_triangle_system(matrix_A, vector_b)

    print(f"x = {vector_x}, Ax = {matrix_A.dot(vector_x)}, b = {vector_b}")

