import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
from ue1.bernstein import bernstein


def bez(t, p):
    n = len(p) - 1
    dim = len(p[0])
    """res = []
    for d in range(dim):
        sum = 0
        for l in range(0, n+1):
            sum += bernstein(t, l, n) * p[l][d]
        res.append(sum)
    return res"""
    return [np.sum([bernstein(t, l, n) * p[l][d] for l in range(n + 1)]) for d in range(dim)]


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, axes = plt.subplots()

    p = [[0, 0], [1, 5], [11, 4], [10, 0]]

    t_values = [t*0.01 for t in range(0, 100)]
    x_coord, y_coord = [bez(t, p)[0] for t in t_values], [bez(t, p)[1] for t in t_values]

    axes.scatter(x_coord, y_coord)
    axes.scatter([p[i][0] for i in range(len(p))], [p[i][1] for i in range(len(p))])
    axes.legend()
    plt.xlabel("t")
    plt.show()
