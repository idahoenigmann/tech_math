import numpy as np


def invert_l(l):
    n, m = l.shape

    if n == 1 and m == 1:
        return np.matrix([[1 / l[0, 0]]])
    elif n <= 1 or m <= 1:
        raise ValueError("matrix dimensions are not supported")

    left_upper = l[range(n // 2)][..., range(m // 2)]
    right_upper = l[range(n // 2)][..., range(m // 2, m)]
    left_lower = l[range(n // 2, n)][..., range(m // 2)]
    right_lower = l[range(n // 2, n)][..., range(m // 2, m)]

    inv_left_upper = invert_l(left_upper)
    inv_right_lower = invert_l(right_lower)

    return np.block([[inv_left_upper, right_upper], [-inv_right_lower * left_lower * inv_left_upper, inv_right_lower]])


if __name__ == "__main__":
    m1 = np.matrix([[1, 0, 0, 0], [2, 4, 0, 0], [3, 5, 8, 0], [4, 6, 7, 16]])
    m2 = np.matrix([[1, 0, 0, 0, 0], [2, 4, 0, 0, 0], [3, 5, 8, 0, 0], [4, 6, 7, 16, 0], [5, 8, 9, 10, 32]])

    print(m1)
    print(invert_l(m1))
    print(np.linalg.inv(m1))

    print(m2)
    print(np.round(invert_l(m2), 5))
    print(np.round(np.linalg.inv(m2), 5))


    """
    a) siehe Satz 7.4.2 aus Lineare Algebra für Technische Mathematiker von Hans Havlicek
    b) siehe Zettel (Kurzfassung: L * angegebene Matrix = Einheitsmatrix)
    """

