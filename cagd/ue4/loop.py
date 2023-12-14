import numpy as np
import geopy.vis as vis
from geopy.mesh import Mesh
import geopy.obj as obj


def loop(M):
    # calculate new vertices from existing vertices
    vertices_from_vertex = []
    vertex_indices = []
    for vertex in M.vertices():
        neighbor_lst = [n.point for n in vertex.vertices()]
        neighbor_lst.append(vertex.point)
        n = vertex.degree
        c = 1/n*(5/8-(3/8+1/4*np.cos(2*np.pi/n)**2))
        weights = [c for _ in range(n)]
        weights.append(1 - n*c)

        vertices_from_vertex.append(np.average(neighbor_lst, axis=0, weights=weights))
        vertex_indices.append(vertex.index)

    # calculate new vertices from existing edges
    vertices_from_edge = []
    edge_indices = []
    for edge in M.edges():
        if edge.isboundary() or edge.pair.isboundary():
            vertices_from_edge.append(np.mean([edge.origin.point, edge.target.point], axis=0))
        else:
            points = [edge.origin.point, edge.target.point, edge.next.target.point,
                      edge.pair.next.target.point]
            vertices_from_edge.append(np.average(points, axis=0, weights=[3/8, 3/8, 1/8, 1/8]))
        edge_indices.append((edge.origin.index, edge.target.index))

    # divide each triangle into four new ones
    triangles = []
    for face in M.faces():
        # get indices
        ab, bc, ca = face.halfedge, face.halfedge.next, face.halfedge.prev
        a, b, c = ab.origin, bc.origin, ca.origin

        a_idx, b_idx, c_idx = a.index, b.index, c.index

        # get indices of edges, they might be oriented in to opposite direction
        try:
            ab_idx = edge_indices.index((a_idx, b_idx))
        except ValueError:
            ab_idx = edge_indices.index((b_idx, a_idx))
        try:
            bc_idx = edge_indices.index((b_idx, c_idx))
        except ValueError:
            bc_idx = edge_indices.index((c_idx, b_idx))
        try:
            ca_idx = edge_indices.index((c_idx, a_idx))
        except ValueError:
            ca_idx = edge_indices.index((a_idx, c_idx))

        # as the list of vertices is concatinated later we update the indices here
        ab_idx += len(vertices_from_vertex)
        bc_idx += len(vertices_from_vertex)
        ca_idx += len(vertices_from_vertex)

        # the four triangles
        triangles.append((ab_idx, bc_idx, ca_idx))
        triangles.append((a_idx, ab_idx, ca_idx))
        triangles.append((b_idx, bc_idx, ab_idx))
        triangles.append((c_idx, ca_idx, bc_idx))

    vertices = np.concatenate((vertices_from_vertex, vertices_from_edge))
    return Mesh(vertices, triangles)


if __name__ == '__main__':
    k = 3   # number of times loop is applied to the mesh, try something like 3

    if False:
        # simple test mesh
        vertices = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 1], [1, 2, 1]]
        triangles = [[0, 1, 2], [3, 2, 1], [2, 3, 4]]
    else:
        # human looking mesh
        vertices, triangles = obj.read('humanoid_tri.obj', 'v', 'f')

    M = Mesh(vertices, triangles)

    output_M = loop(M)
    for _ in range(k - 1):
        output_M = loop(output_M)

    # visualize input and result
    mesh = vis.mesh(M, color=(1, 0, 0))
    mesh.GetProperty().EdgeVisibilityOn()
    mesh.GetProperty().SetLineWidth(2.0)
    mesh.GetProperty().SetOpacity(0.5)
    mesh = vis.mesh(output_M, color=(0, 1, 0))
    mesh.GetProperty().EdgeVisibilityOn()
    mesh.GetProperty().SetLineWidth(2.0)
    mesh.GetProperty().SetOpacity(0.5)
    vis.show()