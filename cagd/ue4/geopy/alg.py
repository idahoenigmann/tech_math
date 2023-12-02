# Copyright 2021, Martin Kilian
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Basic algorithms in mesh processing.
"""

import numpy as np
import scipy.sparse
import scipy.sparse.linalg

from geopy.heap import PriorityQueue


def dijkstra(M, i):
    """ Dijkstra's algorithm.

    Compute the shortest path from a single source vertex to all other
    vertices of a mesh.

    Parameters
    ----------
    M : Mesh
        A mesh.
    i : int
        Index of the source vertex.

    Returns
    -------
    D : list[float]
        The distance of the source to vertex :math:`v_j` is stored as ``D[j]``.
    P : list[int]
        The index of the predecessor vertex of :math:`v_j` on a shortest
        path from the source vertex to :math:`v_j` is stored as P[j].


    The case ``P[j] == -1`` occurs when :math:`v_j` is not reachable from the
    source vertex. The predecessor of the source is always undefined.
    The :download:`script <../../examples/mesh_dist.py>` below shows a color
    coding of the distance of each vertex to the source marked with a white
    sphere.

    .. literalinclude:: ../../examples/mesh_dist.py
       :lines: 8-

    .. image:: ../figures/dijkstra_alpha.png
       :width: 75 %
       :align: center
    """
    # Initialize the list of distances. All distances are unkown except the
    # distance from the source to itself.
    D = M.num_vertices() * [np.inf]
    D[i] = 0.0

    # The indices of predecessor vertices on a shortest path to the source.
    P = M.num_vertices() * [-1]

    # Seed the priority queue with the source vertex. Priorities are distance
    # values. Smaller distance means higher priority.
    Q = PriorityQueue('minheap')
    Q.push(i, D[i])

    while Q:
        # The vertex in the queue with the shortest distance to the source
        # vertex. This vertex will never be added to the queue again!
        v = M.vertex(Q.pop())

        for w in v.vertices():
            # Distance of w to v when moving along the edge vw.
            d = np.linalg.norm(w.point-v.point)

            # Update distance value and predecessor if the path from s to w
            # via v and the edge vw is shorter than the current shortest
            # path from s to w (which may even be undefined at this point).
            if D[v.index] + d < D[w.index]:
                D[w.index] = D[v.index] + d
                P[w.index] = v.index
                Q.push(w.index, D[w.index])

    return D, P


def tutte(M, normalize=False):
    """ Tutte embedding.

    Straight line embedding of a triangle mesh of disk topology.

    Parameters
    ----------
    M : Mesh
        A triangle mesh of disk topology.
    normalize : bool
        Normalize the computed coordinates to the range :math:`[0,1]^2`.

    Raises
    ------
    ValueError
        If the mesh is not of disk topology.

    Returns
    -------
    ndarray
        The i-th row of the returned matrix holds the :math:`(u, v)`
        coordinates of vertex :math:`v_i`.


    Using Tutte's embedding for parametrization and texture mapping usually
    induces large metric distortion, especially in high curvature regions.

    .. literalinclude:: ../../examples/mesh_tutte.py
       :lines: 8-

    .. image:: ../figures/tutte_alpha.png
       :width: 100 %
       :align: center
    """
    # Get boundary loop of the mesh. If there is more than one component
    # we cannot proceed.
    C = M.boundary()

    # There has to be exactly one boundary component. There should also be
    # a test for triangular faces...
    if len(C) != 1:
        msg = ("tutte(): expected a mesh with a single boundary " +
               "component, got " + len(C) + ".")
        raise ValueError(msg)

    # Extract the indices of vertices of the boundary component C. Each
    # such vertex gets it uv coordinates assigned directly.
    C = C[0]
    n = len(C)
    i = [v.index for v in C]
    t = np.linspace(0.0, 2.0*np.pi, n, endpoint=False)

    # Map the boundary loop of M to a regular n-gon with n the number of
    # boundary vertices.
    VT = np.zeros((M.num_vertices(), 2))
    VT[i, :] = np.stack((np.cos(t), np.sin(t)), axis=-1)

    # Assign consecutive indices to all interior vertices to map them to
    # matrix entries.
    P = [v for v in M.vertices() if not v.isboundary()]
    idx = {P[i]: i for i in range(len(P))}

    # Initialize the matrix and the right hand side of the linear system.
    A = scipy.sparse.identity(len(P), dtype=float, format='lil')
    b = np.zeros((len(P), 2), dtype=float)

    # Fill all matrix and right hand side entries. Boundary vertices are
    # fixed to form a convex polygon.
    for v in M.vertices():
        if not v.isboundary():
            # Condition: an interior vertex is the barycenter of its
            # neighbors. Could also use any type of convex combination.
            f = 1.0/v.degree

            for w in v.vertices():
                if w.isboundary():
                    b[idx[v]] += f * VT[w.index, :]
                else:
                    A[idx[v], idx[w]] = -f

    # Convert A to compressed sparse row format. Solve the linear system and
    # assign the computes coordinates.
    A = A.tocsr()
    VT[[p.index for p in P], :] = scipy.sparse.linalg.spsolve(A, b)

    # Normalize the computed coordiantes to the range [0,1] x [0,1]
    if normalize:
        bb_min, bb_max = VT.min(axis=0), VT.max(axis=0)
        VT += bb_min
        VT[:, 0] /= bb_max[0]-bb_min[0]
        VT[:, 1] /= bb_max[1]-bb_min[1]

    return VT
