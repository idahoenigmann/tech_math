import numpy as np


def block_matrix(n):
    res = np.identity(2*n)
    res[range(0, 2*n-1, 2), range(1, 2*n, 2)] = 1
    res[range(1, 2*n, 2), range(0, 2*n-1, 2)] = 1
    return res


if __name__ == "__main__":
    print(block_matrix(6))
    print()
    print(block_matrix(3))
