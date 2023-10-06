
from math import sin, cos, exp


def count(f):
    counter = 0

    def inner_count(*args):
        nonlocal counter
        counter += 1
        return counter, f(*args)

    return inner_count


if __name__ == "__main__":
    f = count(sin)
    g = count(cos)
    print(f(0.1))
    print(f(0.2))
    print(f(0.3))
    print(g(0.1))
    print(f(0.4))
