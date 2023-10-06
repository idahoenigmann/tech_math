import numpy as np


def solve_u(u, b):
    x = np.zeros(b.size)
    for i in range(b.size - 1, -1, -1):
        sum = 0
        for k in range(i + 1, b.size):
            sum += u[i, k] * x[k]
        x[i] = (b[i] - sum) / u[i, i]
    return x


if __name__ == "__main__":
    u = np.matrix([[4, -1, 1], [0, 2, 5], [0, 0, 3]])
    b = np.array([1, 42, -3])

    print(u)
    print(b)
    print(solve_u(u, b))
    print(np.linalg.solve(u, b))

    print("-" * 25)

    u = np.matrix([[4, -1, 1, 8], [0, 2, 5, 2], [0, 0, 3, -10], [0, 0, 0, 1]])
    b = np.array([1, 42, -3, 42])

    print(u)
    print(b)
    print(solve_u(u, b))
    print(np.linalg.solve(u, b))

    """
    a)
    es existiert genau eine Zahl, sodass die letze Zeile gilt.
    Dann existiert auch genau eine Zahl sodass die letzen beiden Zeilen stimmen,
    und so weiter bis zur ersten Zeile.
    """
