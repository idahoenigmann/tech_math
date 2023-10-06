class Vector():
    v = []

    def __init__(self, v):
        self.v = v

    def __str__(self):
        return str(self.v)

    def norm(self, p):
        return (sum(abs(e) ** p for e in self.v)) ** (1 / p)

    def sum(self):
        return sum(e for e in self.v)

    def ncount(self):
        return len(self.v)

    def __add__(self, other):
        return Vector([self.v[i] + other.v[i] for i in range(min(self.ncount(), other.ncount()))])

    def __sub__(self, other):
        return Vector([self.v[i] - other.v[i] for i in range(min(self.ncount(), other.ncount()))])


class VectorComplex(Vector):
    imag = []

    def __init__(self, real, imag):
        self.v = real
        self.imag = imag

    def __str__(self):
        res = []
        for i in range(self.ncount()):
            res.append(complex(self.v[i], self.imag[i]))
        return str(res)

    def norm(self, p):
        return (sum((self.v[i] ** 2 + self.imag[i] ** 2) ** (p / 2) for i in range(self.ncount()))) ** (1 / p)

    def sum(self):
        return complex(sum(e for e in self.v), sum(e for e in self.imag))

    def __add__(self, other):
        return VectorComplex([self.v[i] + other.v[i] for i in range(min(self.ncount(), other.ncount()))],
                             [self.imag[i] + other.imag[i] for i in range(min(self.ncount(), other.ncount()))])

    def __sub__(self, other):
        return VectorComplex([self.v[i] - other.v[i] for i in range(min(self.ncount(), other.ncount()))],
                             [self.imag[i] - other.imag[i] for i in range(min(self.ncount(), other.ncount()))])


if __name__ == "__main__":
    a = VectorComplex([1, 2, 3, 4], [5, 6, 7, 8])
    b = VectorComplex([2, 3, 4, 5], [4, 3, 2, 1])

    print(a.norm(2))
    print(a.sum())
    print(a.ncount())

    print(a + b)
    print(a - b)
