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
        face_vert_idx.append(tuple(np.sort([vert for vert in sorted_vert])))

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
        edge_vert_idx.append(tuple(np.sort([edge.origin.index, edge.target.index])))

    vertices_from_vertices = []
    vert_vert_idx = []
    for vertex in M.vertices():

        if vertex.isboundary():
            boundary_vert = []
            for hedge in vertex.halfedges():
                if hedge.isboundary():
                    if hedge.origin.index != vertex.index:
                        boundary_vert.append(hedge.origin)
                    else:
                        boundary_vert.append(hedge.target)
                if hedge.pair.isboundary():
                    if hedge.origin.index != vertex.index:
                        boundary_vert.append(hedge.origin)
                    else:
                        boundary_vert.append(hedge.target)

            points = [boundary_vert[0].point, vertex.point, boundary_vert[1].point]
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
    outer_edges = set()
    for face in M.faces():
        if face.valence != 4:
            raise ValueError("non rectangle mesh given")

        # get indices
        ab, bc, cd, da = face.halfedge, face.halfedge.next, face.halfedge.next.next, face.halfedge.prev
        a_idx, b_idx, c_idx, d_idx = ab.origin.index, bc.origin.index, cd.origin.index, da.origin.index

        ab_idx = edge_vert_idx.index(tuple(np.sort([a_idx, b_idx])))
        bc_idx = edge_vert_idx.index(tuple(np.sort([b_idx, c_idx])))
        cd_idx = edge_vert_idx.index(tuple(np.sort([c_idx, d_idx])))
        da_idx = edge_vert_idx.index(tuple(np.sort([d_idx, a_idx])))

        abcd_idx = face_vert_idx.index(tuple(np.sort([a_idx, b_idx, c_idx, d_idx])))

        # adjust indices because vertices are concatenated
        ab_idx += len(vertices_from_vertices)
        bc_idx += len(vertices_from_vertices)
        cd_idx += len(vertices_from_vertices)
        da_idx += len(vertices_from_vertices)
        abcd_idx += len(vertices_from_vertices) + len(vertices_from_edges)

        # add the four new rectangles
        rectangles.append((a_idx, ab_idx, abcd_idx, da_idx))
        rectangles.append((b_idx, bc_idx, abcd_idx, ab_idx))
        rectangles.append((c_idx, cd_idx, abcd_idx, bc_idx))
        rectangles.append((d_idx, da_idx, abcd_idx, cd_idx))

    vertices = np.concatenate((vertices_from_vertices, vertices_from_edges, vertices_from_faces))
    return Mesh(vertices, rectangles)


if __name__ == '__main__':
    k = 1   # number of times catmull-clark is applied to the mesh, try something like 3

    # simple test mesh
    vertices = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 2, 1], [1, 2, 1], [2, 0, -1], [2, 1, -1]]
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