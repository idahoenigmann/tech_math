import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath('../.'))

import geopy.obj as obj
from geopy.mesh import Mesh, Vertex
import geopy.vis as vis

if __name__ == '__main__':
    v, f = obj.read('humanoid_tri.obj', 'v', 'f')
    M = Mesh(v, f)
    M_org = M.copy()

    for vertex in M_org.vertices():
        neighbor_lst = [n.point for n in vertex.vertices()]
        mean = np.mean(neighbor_lst, axis=0)
        M.vertex(vertex.index).point = mean

    M.write('out.obj')

    mesh_vis = vis.mesh(M_org, color=(1, 0, 0))
    mesh_vis.GetProperty().EdgeVisibilityOn()
    mesh_vis.GetProperty().SetLineWidth(2.0)
    mesh_vis.GetProperty().SetOpacity(0.5)
    mesh_vis = vis.mesh(M, color=(0, 1, 0))
    mesh_vis.GetProperty().EdgeVisibilityOn()
    mesh_vis.GetProperty().SetLineWidth(2.0)
    mesh_vis.GetProperty().SetOpacity(0.5)

    vis.show()
