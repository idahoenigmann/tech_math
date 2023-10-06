import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

    fig = plt.figure()

    ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax2 = fig.add_axes([0.2, 0.5, 0.2, 0.2])

    x1 = np.linspace(0, 100, 100)
    y1 = 2 * x1

    x2 = np.linspace(20, 22, 50)
    y2 = 2 * x2

    ax1.plot(x1, y1, color="red")
    ax2.plot(x2, y2, color="red")

    ax1.set_xlabel("x")
    ax1.set_ylabel("2x")
    ax1.legend(["2x"])

    ax2.set_title("zoom")
    ax2.set_xlabel("x")
    ax2.set_ylabel("2x")
    ax2.set(xlim=(20, 22), ylim=(30, 50))

    plt.show()
