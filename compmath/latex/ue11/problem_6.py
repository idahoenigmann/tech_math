import sympy
from sympy.abc import a, b, c, d

if __name__ == "__main__":
    V = sympy.Matrix([[1, a, a ** 2, a ** 3],
                      [1, b, b ** 2, b ** 3],
                      [1, c, c ** 2, c ** 3],
                      [1, d, d ** 2, d ** 3]])

    det = V.det()
    print(sympy.latex(sympy.simplify(det)))
    print(sympy.latex(sympy.factor(det)))
