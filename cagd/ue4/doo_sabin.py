import numpy as np
import geopy.vis as vis
from geopy.mesh import Mesh


def doo_sabin(M):
    vertices = []
    vertices_idx = []
    for face in M.faces():
        k = face.valence
        face_vertices = [e for e in face.vertices()]
        face_idx = tuple(np.sort([e.index for e in face.vertices()]))
        for idx in range(k):
            weights = [(3 + 2*np.cos(2*np.pi*j/k))/(4*k) for j in range(1, k)]
            weights.append(1/4 + 5/(4*k))
            points = [face_vertices[(j + idx + 1) % k].point for j in range(k)]
            vertices.append(np.average(points, axis=0, weights=weights))
            vertices_idx.append((face_idx, face_vertices[idx].index))

    faces = []
    for vertex in M.vertices():
        if not vertex.isboundary():
            faces_idx = [tuple(np.sort([e.index for e in f.vertices()])) for f in vertex.faces()]
            faces.append([vertices_idx.index(tuple((f_idx, vertex.index))) for f_idx in faces_idx])

    for edge in M.edges():
        if not edge.isboundary() and not edge.pair.isboundary():
            f1_idx = tuple(np.sort([e.index for e in edge.face.vertices()]))
            f2_idx = tuple(np.sort([e.index for e in edge.pair.face.vertices()]))
            v1_idx, v2_idx = edge.origin.index, edge.target.index
            points = [(f1_idx, v1_idx), (f2_idx, v1_idx), (f2_idx, v2_idx), (f1_idx, v2_idx)]
            faces.append([vertices_idx.index(point) for point in points])

    for face in M.faces():
        face_idx = tuple(np.sort([e.index for e in face.vertices()]))
        new_face = [vertices_idx.index((face_idx, v.index)) for v in face.vertices()]

        faces.append(new_face)

    return Mesh(vertices, faces)


if __name__ == '__main__':
    k = 1   # number of times doo-sabin is applied to the mesh, try something like 3

    # simple test mesh
    n = 5
    vertices = [[np.sin(x * 2 * np.pi / n), np.cos(x * 2 * np.pi / n), 0] for x in range(n)]
    faces = [[x for x in range(n)]]
    vertices.append([2, 1, 1])
    faces.append([2, 1, n])
    faces.append([1, 0, n])

    M = Mesh(vertices, faces)

    output_M = doo_sabin(M)
    for _ in range(k - 1):
        output_M = doo_sabin(output_M)

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