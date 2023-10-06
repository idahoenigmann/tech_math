import matplotlib.pyplot as plt
import numpy as np


def f(x, y):
    if x > 0:
        return [1-y, 1+x]
    else:
        return [-1+y, -1-x]


if __name__ == "__main__":
    fig, ax = plt.subplots()

    n = 10

    [x, y] = np.mgrid[-1:1:2 / 10, -2:1:3 / 10]

    f_xy = np.array([f(x[i, j], y[i, j]) for i in range(n) for j in range(n)])
    u = f_xy[:, 0]
    v = f_xy[:, 1]

    ax.quiver(x, y, u, v)

    plt.show()
