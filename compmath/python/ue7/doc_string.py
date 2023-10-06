class Complex:
    """Stores a complex number, allows addition, multiplication and division by other complex number"""
    z = (0, 0)

    def __init__(self, z1_, z2_):
        self.z = (z1_, z2_)

    def __str__(self):
        return str(self.z[0]) + (" + i" if self.z[1] >= 0 else " - i") + str(abs(self.z[1]))

    def __repr__(self):
        return str(self)

    def add(self, other):
        """changes self by adding a different complex number"""
        self.z = (self.z[0] + other.z[0], self.z[1] + other.z[1])
        return self

    def multiply(self, other):
        """changes self by multiplication with a different complex number"""
        self.z = (self.z[0] * other.z[0] - self.z[1] * other.z[1], self.z[1] * other.z[0] + self.z[0] * other.z[1])
        return self

    def divide(self, other):
        """changes self by division by a different complex number"""
        self.z = ((self.z[0] * other.z[0] + self.z[1] * other.z[1]) / (other.z[0] ** 2 + other.z[1] ** 2),
                  (self.z[1] * other.z[0] - self.z[0] * other.z[1]) / (other.z[0] ** 2 + other.z[1] ** 2))
        return self


class Vector:
    """collection of vector functions"""
    def add(self, z1, z2):
        """addition of two vectors"""
        if len(z1) != len(z2):
            raise ValueError("length of list must match")
        return list(z1[i] + z2[i] for i in range(len(z1)))

    def scalar(self, a, z1):
        """multiplication of a vector with a number"""
        return list(a * e for e in z1)


class VectorPlus(Vector):
    """extendes vector by addition vector functions"""
    def vector_proc(self, z1, z2):
        """vector product"""
        return [z1[(i + 1) % len(z1)] * z2[(i + 2) % len(z2)] - z2[(i + 1) % len(z2)] * z1[(i + 2) % len(z1)] for i in
                range(len(z1))]
        # return np.cross(np.array(z1), np.array(z2))

    def tensor(self, z1, z2):
        """tensor product"""
        return [[z1_el * z2_el for z2_el in z2] for z1_el in z1]

if __name__ == "__main__":
    print(Complex.__doc__)
    print(Complex.add.__doc__)
    print(Complex.multiply.__doc__)

    print("\n")
    print(Vector.__doc__)
    print(VectorPlus.__doc__)
