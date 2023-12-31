from scipy.special import binom
import matplotlib
import matplotlib.pyplot as plt


def bernstein(t, i, j):
    return binom(j, i) * t**i * (1-t)**(j-i)


if __name__ == '__main__':
    matplotlib.use('TkAgg')

    fig, axes = plt.subplots()

    for i, j in [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]:
        x_coord = [t*0.01 for t in range(0, 100)]
        y_coord = [bernstein(t, i, j) for t in x_coord]

        axes.scatter(x_coord, y_coord, label=f"$H_{i}^{j}(t)$")
    axes.legend()
    plt.xlabel("t")
    plt.show()
