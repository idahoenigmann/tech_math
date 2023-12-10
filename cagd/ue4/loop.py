import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import geopy.obj as obj
from geopy.mesh import Mesh, Vertex
import geopy.vis as vis
from geopy.mesh import Mesh


def loop(M):
    vertices_from_vertex = []
    for vertex in M.vertices():
        neighbor_lst = [n.point for n in vertex.vertices()]
        neighbor_lst.append(vertex.point)
        n = vertex.degree
        c = 1/n*(5/8-(3/8+1/4*np.cos(2*np.pi/n)**2))
        weights = [c for _ in range(n)]
        weights.append(1 - n*c)

        vertices_from_vertex.append(np.average(neighbor_lst, axis=0, weights=weights))

    vertices_from_edge = []
    for edge in M.edges():
        if edge.isboundary():
            vertices_from_edge.append(np.mean([edge.origin.point, edge.target.point], axis=0))
        else:
            points = [edge.origin.point, edge.target.point, edge.next.target.point,
                      edge.pair.next.target.point]
            vertices_from_edge.append(np.average(points, axis=0, weights=[3/8, 3/8, 1/8, 1/8]))

    vertices = np.concatenate((vertices_from_vertex, vertices_from_edge))
    triangles = [] # TODO
    return Mesh(vertices, triangles)


if __name__ == '__main__':
    vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 1], [1, 2, 1]]
    triangles = [[0, 1, 2], [3, 2, 1], [2, 3, 4]]

    M = Mesh(vertices, triangles)

    output_M = loop(M)

    mesh = vis.mesh(M, color=(1, 0, 0))
    mesh.GetProperty().EdgeVisibilityOn()
    mesh.GetProperty().SetLineWidth(2.0)
    mesh.GetProperty().SetOpacity(0.5)
    mesh = vis.mesh(output_M, color=(0, 1, 0))
    mesh.GetProperty().EdgeVisibilityOn()
    mesh.GetProperty().SetLineWidth(2.0)
    mesh.GetProperty().SetOpacity(0.5)
    vis.show()