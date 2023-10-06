class Vector():
    v = []

    def __init__(self, v):
        self.v = v

    def __str__(self):
        return str(self.v)

    def norm(self, p):
        return (sum(abs(e) ** p for e in self.v)) ** (1/p)

    def sum(self):
        return sum(e for e in self.v)

    def ncount(self):
        return len(self.v)

    def __add__(self, other):
        return Vector([self.v[i] + other.v[i] for i in range(min(self.ncount(), other.ncount()))])

    def __sub__(self, other):
        return Vector([self.v[i] - other.v[i] for i in range(min(self.ncount(), other.ncount()))])


if __name__ == "__main__":
    a = Vector([1, 2, 3, 4])
    b = Vector([2, 3, 4, 5])

    print(a.norm(2))
    print(a.sum())
    print(a.ncount())

    print(a + b)
    print(a - b)
