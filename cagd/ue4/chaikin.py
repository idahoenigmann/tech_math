import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def chaikin(px, py):
    # TODO
    return px, py


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, ax = plt.subplots()

    px = [0, 0, 3, 7, 7, 6]
    py = [2, 4, 5, 3, 2, 0]

    c1x, c1y = chaikin(px, py)
    print(c1x)
    print(c1y)

    for i in range(len(px)):
        ax.plot(px[i:i+2], py[i:i+2], c='black')

    for i in range(len(px)):
        ax.plot(c1x[i:i+2], c1y[i:i+2], c='blue')

    plt.show()
