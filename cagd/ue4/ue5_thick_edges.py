import numpy as np
import geopy.vis as vis
from geopy.mesh import Mesh
import geopy.obj as obj


def thick_edges(mesh, width=0.1, depth=0.2):
    vertices_upper = []
    vertices_lower = []

    vertices_lower_idx = dict()
    vertices_upper_idx = dict()
    for v in mesh.vertices():
        vertices_lower_idx[v] = dict()
        vertices_upper_idx[v] = dict()

    faces = []
    for face in mesh.faces():
        for vertex in face.vertices():
            # move vertex towards middle of face
            x, y = [v.point for v in vertex.vertices() if face in v.faces()]
            x, y = np.array(x), np.array(y)
            vector_a = (x - vertex.point) / np.linalg.norm(x - vertex.point)
            vector_b = (y - vertex.point) / np.linalg.norm(y - vertex.point)
            new_vector = vertex.point + width * (vector_a + vector_b)
            vertices_upper.append(new_vector)
            vertices_upper_idx[vertex][face] = len(vertices_upper) - 1

            # add vertex for indentation
            k = vertex.valence
            vectors = [(np.array(v.point) - vertex.point) for v in vertex.vertices()]
            normal_vec_sum = np.zeros(3)
            for i in range(0, k):
                normal_vec = np.cross(vectors[i], vectors[(i+1) % k])
                normal_vec = normal_vec / np.linalg.norm(normal_vec)
                normal_vec_sum += normal_vec
            normal_vec = 1/k * normal_vec_sum
            normal_vec = normal_vec / np.linalg.norm(normal_vec)

            vertices_lower.append(new_vector - depth * normal_vec)
            vertices_lower_idx[vertex][face] = len(vertices_lower) - 1

        faces.append([len(vertices_upper) - i for i in range(face.valence, 0, -1)])

    offset = len(vertices_lower)

    for vertex in mesh.vertices():
        if not vertex.isboundary():
            new_face = [idx + offset for idx in vertices_lower_idx[vertex].values()]
            new_face.reverse()
            faces.append(new_face)

    for edge in mesh.edges():
        if not edge.isboundary() and not edge.pair.isboundary():
            f1, f2 = edge.face, edge.pair.face
            p1, p2 = edge.origin, edge.target
            faces.append([vertices_lower_idx[p1][f1] + offset, vertices_lower_idx[p1][f2] + offset,
                          vertices_lower_idx[p2][f2] + offset, vertices_lower_idx[p2][f1] + offset])
            faces.append([vertices_upper_idx[p1][f1], vertices_lower_idx[p1][f1] + offset,
                          vertices_lower_idx[p2][f1] + offset, vertices_upper_idx[p2][f1]])
            faces.append([vertices_upper_idx[p2][f2], vertices_lower_idx[p2][f2] + offset,
                          vertices_lower_idx[p1][f2] + offset, vertices_upper_idx[p1][f2]])

    return Mesh(np.concatenate([vertices_upper, vertices_lower]), faces)


if __name__ == '__main__':
    # not finished
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
        vertices = np.array(vertices)[:, :3]

    M = Mesh(vertices, faces)

    output_M = thick_edges(M)

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
