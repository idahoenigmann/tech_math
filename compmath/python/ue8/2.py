

class Poly:
    coeff = []

    def __init__(self, coeff_):
        self.coeff = coeff_

    def __str__(self):
        res = ""
        for i in range(len(self.coeff)):
            res += (" + " if self.coeff[i] >= 0 else " - ") + str(abs(self.coeff[i])) + " * x^" + str(i)
        return res

    def poly_eval(self, x):
        return sum(self.coeff[i] * x ** i for i in range(len(self.coeff)))

    def poly_der_coef(self, k):
        if k == 0:
            return self

        res = Poly(list(0 for _ in range(len(self.coeff) - 1)))
        for i in range(len(self.coeff) - 1):
            res.coeff[i] = (i+1) * self.coeff[i+1]
        return res.poly_der_coef(k - 1)


if __name__ == "__main__":
    p = Poly([1, -2, 0, 0, 1, -10])
    print(p.poly_eval(0))
    print(p.poly_eval(1))

    print(p)
    print(p.poly_der_coef(1))
    print(p.poly_der_coef(2))
    print(p.poly_der_coef(3))
