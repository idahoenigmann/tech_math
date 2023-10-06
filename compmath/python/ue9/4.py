import numpy as np


def ishermitian(a):
    return np.array_equal(np.conjugate(a).transpose(), a)


if __name__ == "__main__":
    a = np.matrix([[3, 3+1j], [3-1j, 2]])
    b = np.matrix([[6+1j, 2 + 5j], [4 - 1j, -4-8j]])
    c = np.matrix([[1, 7j, 5-3j], [-7j, 5, -3+1j], [5+3j, -3-1j, -42]])

    print(ishermitian(a))
    print(ishermitian(b))
    print(ishermitian(c))
