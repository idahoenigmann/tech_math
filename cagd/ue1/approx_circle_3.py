import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from ue1.bez import bez

if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots()

    p = [[0, 1], [8/3*(np.cos(np.pi/4) - 1/2), 1], [1, 8/3*(np.sin(np.pi/4) - 1/2)], [1, 0]]

    t_values = [t*0.01 for t in range(0, 100)]
    x_coord, y_coord = [bez(t, p)[0] for t in t_values], [bez(t, p)[1] for t in t_values]
    circle = plt.Circle((0, 0), 1, color='b')

    ax.add_patch(circle)
    ax.scatter(x_coord, y_coord, c="r")
    ax.scatter([p[i][0] for i in range(len(p))], [p[i][1] for i in range(len(p))], c="black")
    ax.axis('equal')

    plt.show()
