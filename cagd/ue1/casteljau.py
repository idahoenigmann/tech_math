import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
from ue1.bernstein import bernstein


def casteljau(t, p):
    res = []
    for dim in range(len(p[0])):
        b = [p[i][dim] for i in range(len(p))]
        while len(b) > 1:
            b = [(1-t) * b[i] + t * b[i+1] for i in range(len(b) - 1)]
        res.append(b[0])
    return res


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots(nrows=2, ncols=1)

    p = [[0, 0], [1, 5], [11, 4], [10, 0]]

    t_values = [t*0.01 for t in range(0, 100)]

    x_coord, y_coord = [casteljau(t, p)[0] for t in t_values], [casteljau(t, p)[1] for t in t_values]

    subplot1 = ax[0]
    subplot1.scatter(x_coord, y_coord)
    subplot1.scatter([p[i][0] for i in range(len(p))], [p[i][1] for i in range(len(p))])

    p = [[-3, 1], [6, 10], [8, 3]]

    t_values = [random.random() for t in range(0, 100)]
    x_coord, y_coord = [casteljau(t, p)[0] for t in t_values], [casteljau(t, p)[1] for t in t_values]

    subplot2 = ax[1]
    subplot2.scatter(x_coord, y_coord)
    subplot2.scatter([p[i][0] for i in range(len(p))], [p[i][1] for i in range(len(p))])

    plt.show()
