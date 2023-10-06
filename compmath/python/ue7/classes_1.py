
class Complex:
    z = (0, 0)

    def __init__(self, z1_, z2_):
        self.z = (z1_, z2_)

    def __str__(self):
        return str(self.z[0]) + (" + i" if self.z[1] >= 0 else " - i") + str(abs(self.z[1]))

    def __repr__(self):
        return str(self)

    def add(self, other):
        self.z = (self.z[0] + other.z[0], self.z[1] + other.z[1])
        return self

    def multiply(self, other):
        self.z = (self.z[0] * other.z[0] - self.z[1] * other.z[1], self.z[1] * other.z[0] + self.z[0] * other.z[1])
        return self

    def divide(self, other):
        self.z = ((self.z[0] * other.z[0] + self.z[1] * other.z[1]) / (other.z[0] ** 2 + other.z[1] ** 2),
                  (self.z[1] * other.z[0] - self.z[0] * other.z[1]) / (other.z[0] ** 2 + other.z[1] ** 2))
        return self


if __name__ == "__main__":
    z = Complex(3, 5)
    w = Complex(1, -2)

    print(z.add(w))
    print(z.multiply(w))
    print(z.divide(w))
