import os
import sys

sys.path.insert(0, os.path.abspath('../.'))

import geopy.obj as obj
from geopy.mesh import Mesh
import geopy.vis as vis

if __name__ == '__main__':
    bunny_v, bunny_f = obj.read('bunny.obj', 'v', 'f')

    M = Mesh(bunny_v, bunny_f)

    for h in M.halfedges():
        print(h)

    mesh_vis = vis.mesh(M)
    mesh_vis.GetProperty().EdgeVisibilityOn()
    mesh_vis.GetProperty().SetLineWidth(2.0)
    mesh_vis.GetProperty().SetOpacity(0.5)

    vis.show()
