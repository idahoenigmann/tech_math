from csv import reader

import numpy as np


def calc_centre_of_mass(face):
    centre_of_mass = np.zeros(len(vertices[face[0] - 1]))
    total_mass = 0

    if len(face) == 1:
        return vertices[face[0] - 1]
    elif len(face) == 2:
        return (vertices[face[0] - 1] + vertices[face[1] - 1])/2

    for i in range(1, len(face) - 1):
        A = vertices[face[0] - 1]
        B = vertices[face[i] - 1]
        C = vertices[face[i + 1] - 1]

        mass = np.dot(B - A, C - A) / 2
        total_mass += mass
        curr_centre_of_mass = (A + B + C) / 3
        centre_of_mass += curr_centre_of_mass * mass

    return centre_of_mass / total_mass


if __name__ == "__main__":
    vertices = []
    faces = []

    with open('file.obj') as file:
        csv_reader = reader(file, delimiter=" ")

        for line in csv_reader:
            if line[0] == "v":
                vertices.append(np.asarray(line[1:]).astype(float))
            elif line[0] == "f":
                faces.append(np.asarray(line[1:]).astype(int))

    print(vertices, end="\n\n")

    for face in faces:
        print(face)
        print(calc_centre_of_mass(face), end="\n\n")
