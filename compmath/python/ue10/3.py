import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

    fig, (ax1, ax2) = plt.subplots(2, 2, sharex="all")

    x = np.linspace(-2, 2, 100)
    y1 = np.sin(4 * x)
    y2 = np.cos(x) * np.sin(x)
    y3 = np.cos(x)
    y4 = np.cos(x) + np.sin(x)

    ax1[0].plot(x, y1, color="red")
    ax1[1].plot(x, y2, color="blue")
    ax2[0].plot(x, y3, color="blue")
    ax2[1].plot(x, y4, color="blue")

    ax1[0].legend(["sin(4x)"], loc=7)
    ax1[1].legend(["cos(x)sin(x)"], loc=10)
    ax2[0].legend(["cos(x)"], loc=8)
    ax2[1].legend(["cos(x)+sin(x)"], loc=4)

    ax1[0].set_xlabel("x")
    ax1[1].set_xlabel("x")
    ax2[0].set_xlabel("x")
    ax2[1].set_xlabel("x")

    plt.show()
