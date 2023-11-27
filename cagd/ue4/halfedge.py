import os
import sys

sys.path.insert(0, os.path.abspath('../.'))

import geopy.obj as obj
from geopy.mesh import Mesh

if __name__ == '__main__':
    bunny_v, bunny_f = obj.read('bunny.obj', 'v', 'f')

    M = Mesh(bunny_v, bunny_f)

    for h in M.halfedges():
        print(h)
