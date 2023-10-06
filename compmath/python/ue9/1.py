import numpy as np


def matrix_a(n):
    if n < 5:
        raise ValueError("Size of matrix must be bigger than 4.")
    res = np.zeros((n, n))
    res[0] = 1
    res[-1] = 1
    res[:, 0] = 1
    res[:, -1] = 1
    return res


def matrix_b(n):
    if n < 5:
        raise ValueError("Size of matrix must be bigger than 4.")
    if n % 2 == 0:
        raise ValueError("Size of matrix must be odd.")
    res = np.zeros((n, n))
    res[:, n // 2] = 1
    return res


def matrix_c(n):
    if n < 5:
        raise ValueError("Size of matrix must be bigger than 4.")
    if n % 2 == 0:
        raise ValueError("Size of matrix must be odd.")
    res = np.zeros((n, n))
    res[0] = 1
    res[n // 2] = 1
    res[-1] = 1
    res[range(n // 2, n), 0] = 1
    res[range(0, n // 2), -1] = 1
    return res


if __name__ == "__main__":
    try:
        print(matrix_a(4))
    except ValueError:
        print("matrix_a failed")

    print(matrix_a(5))

    print("-" * 25)

    print(matrix_b(5))

    try:
        print(matrix_b(6))
    except ValueError:
        print("matrix_b failed")

    print(matrix_b(7))

    print("-" * 25)

    print(matrix_c(5))
    print(matrix_c(11))
