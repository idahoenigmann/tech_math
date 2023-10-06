
from math import sin, cos, exp


def dev(fun):
    def inner_dev(ev):
        return fun(ev)
    return inner_dev


def count(f):
    counter = 0

    def inner_count(*args):
        nonlocal counter
        counter += 1
        return counter, f(*args)

    return inner_count


def comp(*args):
    def wrapper(f):
        def inner_comp(val):
            res = f(val)
            for g in args[::-1]:
                res = g(res)
            return res
        return inner_comp
    return wrapper


@dev
def sin_(x):
    return sin(x)


@dev
def exp_(x):
    return exp(x)


@count
def foo():
    print("Hello World!")


@comp(cos, exp)
def foo2(x):
    return x + 2


class Test:
    def foo(self, x):
        print(f"executing foo({self}, {x})")

    @classmethod
    def c_foo(cls, x):
        print(f"executing class_foo({cls}, {x})")

    @staticmethod
    def s_foo(x):
        print(f"executing static_foo({x})")


if __name__ == "__main__":
    print(sin_(1))
    print(exp_(1))

    print(foo())

    print(foo2(1))
    print(foo2(5))

    Test.s_foo(1)
    Test.c_foo(2)

    t = Test()

    t.foo(3)
    t.c_foo(4)
