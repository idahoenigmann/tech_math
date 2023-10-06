import pdb
from math import sin


def f(x):
    # pdb.set_trace()
    x = x + 1.0

    return sin(x)**2 + x


if __name__ == "__main__":

    print("value of f(x)", f(1))

# n ... next
# s ... step
# l ... list
# c ... continue
