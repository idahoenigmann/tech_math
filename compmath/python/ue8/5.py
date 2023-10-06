import numpy as np


def xdiagonal(n):
    return (np.identity(n) + np.identity(n)[::-1]).clip(max=1)


if __name__ == "__main__":
    print(xdiagonal(5))
    print(xdiagonal(4))
