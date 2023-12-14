import numpy as np
import geopy.vis as vis
from geopy.mesh import Mesh
import geopy.obj as obj


def catmull_clark(M):
    vertices_from_faces = []
    face_vert_idx = []
    for face in M.faces():
        vertices_from_faces.append(np.mean([vert.point for vert in face.vertices()], axis=0))
        sorted_vert = np.sort([vert.index for vert in face.vertices()])
        face_vert_idx.append(tuple(vert for vert in sorted_vert))

    vertices_from_edges = []
    edge_vert_idx = []
    for edge in M.edges():
        if edge.isboundary() or edge.pair.isboundary():
            vertices_from_edges.append(np.mean([edge.origin.point, edge.target.point], axis=0))
        else:
            points = [edge.prev.origin.point, edge.next.target.point,
                      edge.origin.point, edge.target.point,
                      edge.pair.next.target.point, edge.pair.prev.origin.point]
            vertices_from_edges.append(np.average(points, axis=0, weights=[1/16, 1/16, 3/8, 3/8, 1/16, 1/16]))
        edge_vert_idx.append((edge.origin.index, edge.target.index))

    vertices_from_vertices = []
    vert_vert_idx = []
    for vertex in M.vertices():
        if vertex.halfedge.isboundary() or vertex.halfedge.pair.isboundary():
            points = [vertex.halfedge.prev.origin.point, vertex.point, vertex.halfedge.target.point]
            vertices_from_vertices.append(np.average(points, weights=[1/8, 3/4, 1/8], axis=0))
        else:
            point = [vertex.point]
            neighbor_points = [n.point for n in vertex.vertices()]
            neighbor_neighbor_points = [n.halfedge.target.point for n in vertex.vertices()]
            k = vertex.degree
            weights = np.concatenate(([1-7/(4*k)], [3/(2*k*k) for _ in range(k)],
                                     [1/(4*k*k) for _ in range(len(neighbor_neighbor_points))]))
            vertices_from_vertices.append(np.average(np.concatenate((point, neighbor_points, neighbor_neighbor_points)),
                                                     weights=weights, axis=0))
        vert_vert_idx.append(vertex.index)

    rectangles = []
    for face in M.faces():
        # get indices
        ab, bc, cd, da = face.halfedge, face.halfedge.next, face.halfedge.next.next, face.halfedge.prev
        a_idx, b_idx, c_idx, d_idx = ab.origin.index, bc.origin.index, cd.origin.index, da.origin.index

        try:
            ab_idx = edge_vert_idx.index((a_idx, b_idx))
        except ValueError:
            ab_idx = edge_vert_idx.index((b_idx, a_idx))
        try:
            bc_idx = edge_vert_idx.index((b_idx, c_idx))
        except ValueError:
            bc_idx = edge_vert_idx.index((c_idx, b_idx))
        try:
            cd_idx = edge_vert_idx.index((c_idx, d_idx))
        except ValueError:
            cd_idx = edge_vert_idx.index((d_idx, c_idx))
        try:
            da_idx = edge_vert_idx.index((d_idx, a_idx))
        except ValueError:
            da_idx = edge_vert_idx.index((a_idx, d_idx))

        abcd_idx = face_vert_idx.index(tuple(np.sort([a_idx, b_idx, c_idx, d_idx])))

        # add the four new rectangles
        # adjust indices because vertices are concatenated
        adj_for_edge = len(vertices_from_faces)
        adj_for_vert = adj_for_edge + len(vertices_from_edges)
        rectangles.append((a_idx + adj_for_vert, ab_idx + adj_for_edge, abcd_idx, da_idx + adj_for_edge))
        rectangles.append((b_idx + adj_for_vert, ab_idx + adj_for_edge, abcd_idx, bc_idx + adj_for_edge))
        rectangles.append((c_idx + adj_for_vert, cd_idx + adj_for_edge, abcd_idx, bc_idx + adj_for_edge))
        rectangles.append((d_idx + adj_for_vert, cd_idx + adj_for_edge, abcd_idx, da_idx + adj_for_edge))

        # TODO order edges to create orientable surface

    vertices = np.concatenate((vertices_from_faces, vertices_from_edges, vertices_from_vertices))
    return Mesh(vertices, rectangles)


if __name__ == '__main__':
    k = 1   # number of times catmull-clark is applied to the mesh, try something like 3

    # simple test mesh
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 2, -1], [1, 2, -1], [2, 0, 1], [2, 1, 1]]
    rectangles = [[0, 1, 2, 3], [5, 4, 3, 2], [2, 1, 6, 7]]

    M = Mesh(vertices, rectangles)

    output_M = catmull_clark(M)
    for _ in range(k - 1):
        output_M = catmull_clark(output_M)

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