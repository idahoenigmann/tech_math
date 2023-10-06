
from math import sin, exp


def dev(fun):
    def inner_dev(ev):
        return fun(ev)
    return inner_dev


def comp(l):
    def inner_comp(val):
        res = l[-1](val)
        # print(l[-1])
        for f in l[:-1][::-1]:
            # print(f)
            res = f(res)
        return res
    return inner_comp


if __name__ == "__main__":
    sin_ = dev(sin)
    exp_ = dev(exp)
    print(sin_(1))
    print(exp_(1))

    sin_exp = comp([sin, exp, sin, sin])
    print(sin_exp(1))
