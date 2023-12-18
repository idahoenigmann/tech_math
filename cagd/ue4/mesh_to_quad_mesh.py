import numpy as np
import geopy.vis as vis
from geopy.mesh import Mesh
import geopy.obj as obj


def to_quad_mesh(M):
    vertices_from_points = [v.point for v in M.vertices()]
    vert_point_idx = [v.index for v in M.vertices()]

    vertices_from_edges = []
    vert_edge_idx = []
    for edge in M.edges():
        vertices_from_edges.append(np.mean([edge.origin.point, edge.target.point], axis=0))
        vert_edge_idx.append(tuple(np.sort([edge.origin.index, edge.target.index])))

    vertices_from_faces = []
    vert_face_idx = []
    for face in M.faces():
        vertices_from_faces.append(np.mean([v.point for v in face.vertices()], axis=0))
        vert_face_idx.append(tuple(np.sort([v.index for v in face.vertices()])))

    faces = []
    for face in M.faces():
        verts = [v.index for v in face.vertices()]
        face_idx = vert_face_idx.index(tuple(np.sort(verts))) + len(vertices_from_points) + len(vertices_from_edges)
        for idx in range(len(verts)):
            point_idx = vert_point_idx.index(verts[idx])
            prev_edge_idx = vert_edge_idx.index(tuple(np.sort([verts[(idx - 1) % len(verts)], verts[idx]])))
            next_edge_idx = vert_edge_idx.index(tuple(np.sort([verts[idx], verts[(idx + 1) % len(verts)]])))

            prev_edge_idx += len(vertices_from_points)
            next_edge_idx += len(vertices_from_points)

            faces.append([point_idx, next_edge_idx, face_idx, prev_edge_idx])

    return Mesh(np.concatenate([vertices_from_points, vertices_from_edges, vertices_from_faces]), faces)


if __name__ == '__main__':
    if True:
        # simple test mesh
        n = 5
        vertices = [[np.sin(x * 2 * np.pi / n), np.cos(x * 2 * np.pi / n), 0] for x in range(n)]
        faces = [[x for x in range(n)]]
        vertices.append([2, 1, 1])
        faces.append([2, 1, n])
        faces.append([1, 0, n])
    else:
        vertices, faces = obj.read('humanoid_tri.obj', 'v', 'f')

    M = Mesh(vertices, faces)

    output_M = to_quad_mesh(M)

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