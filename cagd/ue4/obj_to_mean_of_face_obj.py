import os
import sys

sys.path.insert(0, os.path.abspath('../.'))

import geopy.obj as obj
from geopy.mesh import Mesh, Vertex

if __name__ == '__main__':
    v, f = obj.read('bunny.obj', 'v', 'f')
    M = Mesh(v, f)

    for vertex in M.vertices():
        mean = [0, 0, 0]
        for n in vertex.vertices():
            neighbor = M.vertex_list()[n.index]
            for l in range(3):
                mean[l] = mean[l] + neighbor[l]

        for l in range(3):
            M.vertex_list()[vertex.index][l] = mean[l]/vertex.degree

    M.write('out.obj')