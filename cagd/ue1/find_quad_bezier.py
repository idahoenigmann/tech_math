import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
from ue1.bez import bez


def find_quad_bezier(t, p0, pt, p1):
    denom = 2 * t * (1-t)

    res = []
    for dim in range(len(p0)):
        num = pt[dim] - (1-t)*(1-t)*p0[dim] - t*t*p1[dim]
        res.append(num / denom)

    return [p0, res, p1]


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots()

    p0 = [0, 0]
    pt = [3, 4]
    p1 = [9, -1]

    control_points = find_quad_bezier(0.2, p0, pt, p1)

    t_values = np.arange(0, 1, 0.001)
    x_coord, y_coord = [bez(t, control_points)[0] for t in t_values], [bez(t, control_points)[1] for t in t_values]

    ax.scatter(x_coord, y_coord, label="bezier curve", c="lightgrey")
    ax.scatter([p[0] for p in control_points], [p[1] for p in control_points], label="control points", c="blue")
    ax.scatter([pt[0]], [pt[1]], label="pt", c="red")

    plt.legend()
    plt.show()
