import numpy as np


def is_symmetric(a):
    return np.array_equal(a, a.transpose())


def poweriteration(a, tau, x):
    if not is_symmetric(a):
        raise ValueError("matrix is not symmetric!")

    n = a.shape[0]
    x_new = x
    l = 0
    l_last = 0
    ax = a * x_new
    while True:
        norm_ax = (sum(ax[j, 0] ** 2 for j in range(n))) ** 0.5
        x_new = ax / norm_ax
        ax = a * x_new
        l = sum(x_new[j, 0] * ax[j, 0] for j in range(n))
        tmp = ax - l * x_new
        norm_ax_lx = (sum(tmp[j, 0] ** 2 for j in range(n))) ** 0.5

        if abs(l_last - l) <= tau:
            if (norm_ax_lx <= tau) and (abs(l_last - l) <= tau):
                break
        else:
            if (norm_ax_lx <= tau) and (abs(l_last - l) <= tau * abs(l)):
                break
        l_last = l
    return l, x_new


if __name__ == "__main__":
    matrix = np.matrix([[9, 13, 3, 6], [13, 11, 7, 6], [3, 7, 4, 7], [6, 6, 7, 10]])
    print(matrix)

    non_sym_matrix = np.matrix([[9, 13, 5, 2], [1, 11, 7, 6], [3, 7, 4, 1], [6, 0, 7, 10]])

    print(is_symmetric(matrix))
    print(is_symmetric(non_sym_matrix))

    x_0 = np.array([1, 1, 1, 1])[..., None]

    e_val, e_vec = poweriteration(matrix, 0.01, x_0)
    print(e_val)
    print(e_vec)

    print("-" * 25)

    w, v = np.linalg.eig(matrix)
    print(w)
    print(v)
