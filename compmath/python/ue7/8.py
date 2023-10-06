from math import sin, pi


def midpointrule(a, b, f, n):
    res = []
    for k in range(n+1):
        N = 2**k
        sum = 0
        for j in range(1, N+1):
            x_j = a + j * (b-a) / N
            x_j_last = a + (j-1)*(b-a) / N

            sum += f((x_j_last + x_j) / 2)
        res.append(sum * (b-a) / N)
    return res


def check_convergence():
    n = 5
    c = 1.5
    for i in range(n):
        print(str(abs(2 - midpointrule(0, pi, sin, n)[i])) + " <= " + str((2 ** i)**(-2) * c))


if __name__ == "__main__":
    print(midpointrule(0, pi, sin, 5))

    check_convergence()

    print(midpointrule(0, 1, lambda x: 4 * x + 2, 3))
    print(midpointrule(0, 1, lambda x: x**2 + 4*x + 2, 3))
    print(midpointrule(0, 1, lambda x: x ** 3 + 4 * x + 2, 3))
    print(midpointrule(0, 1, lambda x: x**4 + 4*x + 2, 3))
