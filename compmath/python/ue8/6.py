import numpy as np


def xdiagonal(n):
    first_row = [np.ones(n-1)]
    last_col = np.ones(n)[..., None]
    rest_matrix = np.matrix(np.identity(n-1)[::-1])
    return np.concatenate((np.concatenate((first_row, rest_matrix)), last_col), axis=1)


if __name__ == "__main__":
    print(xdiagonal(5))
    print()
    print(xdiagonal(10))
