from scipy.special import binom
from matplotlib import pyplot as plt
import numpy as np


def bernstein(t, i, j):
    if i > j:
        raise ValueError(f"{i} <= {j} (i <= j) does not hold")
    if t < 0 or t > 1:
        raise ValueError(f"{t} is not in [0,1] (t={t}) does not hold")

    return binom(j, i) * t**i * (1-t)**(j-i)


if __name__ == '__main__':
    plt.plot(np.array([bernstein(t*0.1, i=1, j=1) for t in range(0, 10)]), np.array([t*0.1 for t in range(1, 10)]))
