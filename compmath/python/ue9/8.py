import numpy as np


def trim_vec(v):
    res = v[abs(v) != max(abs(v))]
    res = res[abs(res) != min(abs(v))]
    res = sorted(res, key=lambda x: (abs(x), x.imag))
    return res


if __name__ == "__main__":
    vector = np.array([-5+3j, -42+4j, 10+100j, -42-4j, 11+100j])

    print(vector)
    print(abs(vector))
    print(trim_vec(vector))
