import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    fig, (ax1, ax2) = plt.subplots(1, 2)

    n, m = 25, 10
    a, b, c, d = (1, 1, 1, 0.5)

    deg = np.linspace(0, 2 * np.pi, n)
    x1 = np.array([i * np.sin(deg) for i in np.linspace(0, a, m)])
    y1 = np.array([i * np.cos(deg) for i in np.linspace(0, b, m)])

    x2 = np.array([i * np.sin(deg) for i in np.linspace(0, c, m)])
    y2 = np.array([i * np.cos(deg) for i in np.linspace(0, d, m)])

    z = np.array([[e for i in range(n)] for e in range(m)])

    print(x1.shape)
    print(z.shape)

    ax1.scatter(x1, y1, c=z, cmap="rainbow")
    ax2.scatter(x2, y2, c=z, cmap="rainbow")

    ax1.set(xlim=(-1, 1), ylim=(-1, 1))
    ax2.set(xlim=(-1, 1), ylim=(-1, 1))

    ax1.legend(["circles"])
    ax2.legend(["ellipses"])

    plt.show()