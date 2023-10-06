import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":

    fig = plt.figure()

    ax1 = fig.add_axes([0.11, 0.11, 0.35, 0.8])
    ax2 = fig.add_axes([0.6, 0.11, 0.35, 0.8])

    x = np.linspace(0, 2, 100)
    y = x ** 2

    ax1.plot(x, y, color="red")
    ax2.plot(x, x, color="blue")

    ax1.set_title("first plot")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y=x^2")
    ax1.legend(["x^2"])

    ax2.set_title("second plot")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y=x")
    ax2.legend(["x"])

    plt.show()

    # gca ... get current axis
    # gcf ... get current figure
