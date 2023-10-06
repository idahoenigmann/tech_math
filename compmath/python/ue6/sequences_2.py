import random


def sequences_a(n=0, a=0, b=0, c=0):
    if n == 0:
        n = random.randint(2, 1000)
    if a == 0:
        a = random.randint(1, 1000)
    if b == 0:
        b = random.randint(1, 1000)
    if c == 0:
        c = random.randint(1, 1000)

    return not a ** n + b ** n == c ** n


def sequences_b(x0, y0, n):
    x, y = x0, y0
    for i in range(n):
        x = (2 * x ** 3) / (3 * x ** 2 - 1)
        y = 0.5 * (y + 1 / y)
    return x, y


if __name__ == "__main__":
    n, a, b, c = 12, 3987, 4365, 4472
    print(sequences_a(n, a, b, c))
    print(a ** n + b ** n)
    print(c ** n)

    for i in range(10000):
        if not sequences_a():
            print("there exists n,a,b,c so that a**n + b**n = c**n")

    print(sequences_b(3, 3, 100))
