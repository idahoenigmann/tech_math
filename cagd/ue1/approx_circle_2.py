import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from ue1.bez import bez

if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots()

    p = [[0, 1], [1, 1], [1, 0]]

    t_values = np.arange(-1, 2, 0.001)
    x_coord, y_coord = [bez(t, p)[0] for t in t_values], [bez(t, p)[1] for t in t_values]
    circle = plt.Circle((0, 0), 1, color='lightblue')

    ax.add_patch(circle)
    ax.scatter(x_coord, y_coord, c="grey")
    ax.scatter([p[i][0] for i in range(len(p))], [p[i][1] for i in range(len(p))], c="black")
    ax.axis('equal')
    ax.set_xlim([-0.5, 1.5])
    ax.set_ylim([-0.5, 1.5])
    ax.plot([0, 1, 1], [1, 1, 0], c="black")

    plt.show()
