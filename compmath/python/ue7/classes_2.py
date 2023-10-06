import numpy as np


class Vector:
    def add(self, z1, z2):
        if len(z1) != len(z2):
            raise ValueError("length of list must match")
        return list(z1[i] + z2[i] for i in range(len(z1)))

    def scalar(self, a, z1):
        return list(a * e for e in z1)


class VectorPlus(Vector):
    def vector_proc(self, z1, z2):
        return [z1[(i + 1) % len(z1)] * z2[(i + 2) % len(z2)] - z2[(i + 1) % len(z2)] * z1[(i + 2) % len(z1)] for i in
                range(len(z1))]
        # return np.cross(np.array(z1), np.array(z2))

    def tensor(self, z1, z2):
        return [[z1_el * z2_el for z2_el in z2] for z1_el in z1]


if __name__ == "__main__":
    v = VectorPlus()

    print(v.add([1, 2, 3], [1, 3, 5]))
    print(v.scalar(42, [1, 3, 5]))
    print(v.vector_proc([1, 2, 3], [3, 4, 5]))
    print(v.tensor([1, 2, 3], [3, 4, 5]))
