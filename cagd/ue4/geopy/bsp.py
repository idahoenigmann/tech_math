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

""" Binary space partioning.

Spatial searching, range queries and closest point projection for point clouds
and triangle meshes. Based on kD-trees and boundary volume hierarchies.
"""

import io
import time
import heapq
import itertools

import numpy as np
import scipy.linalg


class Point:
    """ A point in n-dimensional space.

    This class provides interface methods that make points useable with
    BSP trees. Those methods can also be used as convenience functions to
    handle typical point queries.
    """

    def __init__(self, coords):
        """ Initialize from point coordinates.

        Parameters
        ----------
        coords : array_like, shape (n,), n > 1
            Point coordinates. When passed as ndarray the data buffer is
            re-used.
        """
        # Should not be changed from outside this class. This will not create
        # a copy if coords refers to a row in an ndarray.
        self._point = np.asarray(coords)

        # Precompute attributes for faster access. As soon as _point is
        # changed (explicitly or implicitly) all attributes become invalid.
        self._update_dim()
        self._update_center()
        self._update_bbox()

    @property
    def dim(self):
        """ Ambient space dimension.

        Returns
        -------
        int
            Number of coordinate dimensions.
        """
        return self._dim

    @property
    def center(self):
        """ Get barycenter.

        Returns
        -------
        ndarray
            Barycenter.
        """
        return self._center

    @property
    def bbox(self):
        """ Axis aligned bounding box.

        Returns
        -------
        bb_min : ndarray
            Lower left bounding box corner.
        bb_max : ndarray
            Upper right bounding box corner.
        """
        return self._bbox

    def project(self, x):
        """ Closest point projection.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        ndarray
            Closest point.
        float
            Squared distance to closest point.
        """
        v = x-self._point
        return self._point, np.dot(v, v)

    def dist_sqrd(self, x):
        """ Squared distance function.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        float
            Squared distance of the query point ``x`` to this point.
        """
        return self.project(x)[1]

    def contained_in(self, x, rsqrd):
        """ Containment test.

        Test whether this point is contained in a given sphere.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Sphere center.
        rsqrd : float
            Squared radius of the sphere.

        Returns
        -------
        bool
            :obj:`True` if this point is inside or on the boundary of
            the given sphere.
        """
        v = x-self._point
        return np.dot(v, v) <= rsqrd

    def _update_dim(self):
        self._dim = self._point.size

    def _update_center(self):
        self._center = self._point

    def _update_bbox(self):
        self._bbox = self._point, self._point


class Edge:
    """ (Oriented) line segment in n-dimensional space.

    This class provides interface methods that make line segments useable
    with BVH-trees. Those methods can also be used as convenience functions
    to handle typical line segment queries.
    """

    def __init__(self, a, b):
        """ Initialize line segment.

        Parameters
        ----------
        a : array_like, shape (n,)
            Segment start point.
        b : array_like, shape (n,)
            Segment end point.
        """
        self._a = np.asarray(a)
        self._b = np.asarray(b)

        # Precompute attributes for faster access. Attributes become invalid
        # when vertex coordinates change!
        self._update_dim()
        self._update_center()
        self._update_bbox()

        self._v = b-a
        self._len = np.linalg.norm(self._v)
        self._v /= self._len

    @property
    def dim(self):
        """ Ambient space dimension.

        Returns
        -------
        int
            Number of coordinate dimensions.
        """
        return self._dim

    @property
    def center(self):
        """ Get barycenter.

        Returns
        -------
        ndarray
            Segment midpoint.
        """
        return self._center

    @property
    def bbox(self):
        """ Axis aligned bounding box.

        Returns
        -------
        bb_min : ndarray
            Lower left bounding box corner.
        bb_max : ndarray
            Upper right bounding box corner.
        """
        return self._bbox

    def project(self, x):
        """ Closest point projection.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        ndarray
            Closest point coordinates.
        float
            Squared distance to closest point.
        """
        # Compute the length of the vector x-a when projected onto the
        # normalized direction vector v of the segment.
        proj_len = np.dot(self._v, x-self._a)

        if proj_len <= 0.0:
            p = self._a
        elif proj_len >= self._len:
            p = self._b
        else:
            p = self._a + proj_len*self._v

        v = x-p
        return p, np.dot(v, v)

    def dist_sqrd(self, x):
        """ Squared distance function.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        float
            Squared distance to the line segment.
        """
        return self.project(x)[1]

    def contained_in(self, x, rsqrd):
        """ Containment test.

        Test whether this line segment is contained in a given sphere.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Sphere center.
        rsqrd : float
            Squared radius of the sphere.

        Returns
        -------
        bool
            :obj:`True` if this triangle is inside the given sphere.
        """
        # Each row holds a difference vector. Compute the element wise
        # product, then sum each row.
        v = np.array([x-self._a, x-self._b])
        return np.all(np.sum(v*v, axis=-1) <= rsqrd)

    def _update_dim(self):
        self._dim = self._a.size

    def _update_center(self):
        self._center = 0.5*(self._a + self._b)

    def _update_bbox(self):
        self._bbox = (np.min([self._a, self._b], axis=0),
                      np.max([self._a, self._b], axis=0))


class Triangle:
    """ Triangle in 2 or 3-dimensional Euclidean space.

    This class provides interface methods that makes triangles useable with
    BVH-trees. Those methods can also be used as convenience functions to
    handle typical triangle queries.
    """

    def __init__(self, a, b, c, **kwargs):
        """ Triangle spanned by three points.

        Triangle vertices are assumed to be in general position. Vertex
        coordinates are re-used when passed as :class:`~numpy.ndarray`.

        Parameters
        ----------
        a : array_like, shape (n,), n = 2, 3
            Triangle vertex.
        b : array_like, shape (n,), n = 2, 3
            Triangle vertex.
        c : array_like, shape (n,), n = 2, 3
            Triangle vertex.

        Keyword Arguments
        -----------------
        solver : str
            Affects the ``_project()`` method which is used for internal
            testing and debugging. Possible values: 'lu', and 'pinv'.

        Raises
        ------
        ValueError
            If vertex coordinates are neither 2 nor 3 dimensional.
        """
        self._a = np.asarray(a)
        self._b = np.asarray(b)
        self._c = np.asarray(c)

        try:
            self._solver = kwargs['solver']
        except KeyError:
            self._solver = None

        # Precompute attributes for faster access. All attributes become
        # invalid when vertex coordinates change!
        self._update_dim()
        self._update_center()
        self._update_bbox()

        u = b - a
        v = c - a

        # Compute triangle area and normal vector (only in 3-space). Also
        # initialize a local coordinate system matrix.
        if self._dim == 2:
            # For triangles in the plane self._A has a sign that give the
            # triangle's orientation.
            self._area = 0.5*np.linalg.det([u, v])
            self._A = np.column_stack((u, v))
        elif self._dim == 3:
            self._normal = np.cross(u, v)
            self._area = 0.5*np.linalg.norm(self._normal)
            self._normal /= 2.0*self._area
            self._A = np.column_stack((u, v, self._normal))
        else:
            raise ValueError()

        # Check for geometrically almost degenerate triangle when the area
        # of numerically zero.
        if np.abs(self._area) < 1e-15:
            raise RuntimeError('Triangle area < machine epsilon!')

        # Precompute/pre-factorize the linear system that is solved
        # within the _project() method.
        if self._solver == 'lu':
            self._lu, self._pivot = scipy.linalg.lu_factor(self._A)
        elif self._solver == 'pinv':
            self._A = np.linalg.pinv(self._A)

    @property
    def dim(self):
        return self._dim

    @property
    def center(self):
        return self._center

    @property
    def bbox(self):
        return self._bbox

    def project(self, x):
        """ Closest point projection.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        ndarray
            Closest point in the triangle.
        float
            Squared distance to closest point.
        """
        # Consider the function f(s,t) = (s(b-a) + t(c-a) + (p-a))^2. It
        # describes the squared distance of points (parametrized by (s,t))
        # in the plane of the triangle spanned by a, b, and c to the query
        # point p. Find a minimzer of f inside the triangle, i.e., find
        # (s,t) with s, t >= 0 and s+t <= 1 that minimizes f.
        #
        # Using e0 = b-a, e1 = c-a and aij = <ei,ej>, bi = <ei,(a-p)>,
        # and c = <(a-p),(a-p)> the function f becomes
        #
        #   f = s^2*a00 + 2st*a01 + t^2*a11 + 2s*b0 + 2t*b1 + c.
        #
        # The optimality condition grad f(s,t) = 0 yields
        #
        #   2s*a00 + 2t*a01 = 0     resp.   s*det = a01*b1 - a11*b0
        #   2s*a01 + 2t*a11 = 0             t*det = a01*b0 - a00*b1
        #
        # with det = a00*a11 - a01^2. The corresponding values of (s,t)
        # give the coordinates of the point in the plane of abc closest to p.

        # Initialize all variables as described above.
        e0 = self._b - self._a
        e1 = self._c - self._a
        vec = self._a - x

        a00 = np.dot(e0, e0)
        a01 = np.dot(e0, e1)
        a11 = np.dot(e1, e1)
        b0 = np.dot(e0, vec)
        b1 = np.dot(e1, vec)
        c = np.dot(vec, vec)

        # Squared area of the parallelogram spanned by e0 and e1. Can be
        # zero for degenerate triangles. Can be negative for numerical
        # reasons. Force it to be positive.
        det = a00*a11 - a01*a01
        if det < 0.0: det = 0.0

        # Compute (s,t) from the optimality conditions. Strictly speaking
        # we compute (s*det, t*det). Division is performed later.
        s = a01*b1 - a11*b0
        t = a01*b0 - a00*b1

        #        \ 2 t
        #         \  ^                      s+t <= 1    s < 0   t < 0
        #          \ |                  0:      x         -       -
        #           \|                  1:      -         -       -
        #            *                  2:      -         x       -
        #            |\                 3:      x         x       -
        #            | \                4:      x         x       x
        #       3    |0 \    1          5:      x         -       x
        #            |   \              6:      -         -       x
        #        ----*----*----> s
        #            |     \
        #       4    |  5   \   6
        #
        # For each region we evaluate the gradient of f at the corner(s)
        # that meet(s) the region. The product of grad f with the edge
        # direction tells us whether the edge is a descent direction or not.

        # In the following let g(s,t) denote the value of 1/2 grad f(s,t):
        #
        #   g(s,t) = (s*a00 + t*a01 + b0,
        #             t*a11 + s*a01 + b1)

        if s + t <= det:
            if s < 0.0:
                if t < 0.0:
                    # REGION 4: Minimizer can be on the line s=0 or t=0.
                    if b0 < 0.0:
                        t = 0.0
                        # Test edge direction of t=0: (1,0).g(0,0) = b0
                        if -b0 < a00:
                            s = -b0/a00
                            d_sqrd = s*b0 + c
                        else:
                            s = 1.0
                            d_sqrd = a00 + 2.0*b0 + c
                    else:
                        s = 0.0
                        # Test edge direction of s=0: (0,1).g(0,0) = b1
                        if b1 >= 0.0:
                            t = 0.0
                            d_sqrd = c
                        elif -b1 < a11:
                            t = -b1/a11
                            d_sqrd = t*b1 + c
                        else:
                            t = 1.0
                            d_sqrd = a11 + 2.0*b1 + c
                else:
                    # REGION 3: Minimizer has to be on the line s=0.
                    s = 0.0
                    # Check if the minimum occurs at a vertex or in the
                    # interior of the edge.
                    if b1 >= 0.0:
                        t = 0.0
                        d_sqrd = c
                    elif a11 <= -b1:
                        t = 1.0
                        d_sqrd = a11 + 2.0*b1 + c
                    else:
                        t = -b1/a11
                        d_sqrd = t*b1 + c
            elif t < 0.0:
                # REGION 5: The minimizer has to be on the line t=0.
                t = 0.0
                # Check if the minimum occurs at a vertex of in the
                # interior of the edge.
                if b0 >= 0.0:
                    s = 0.0
                    d_sqrd = c
                elif a00 <= -b0:
                    s = 1.0
                    d_sqrd = a00 + 2.0*b0 + c
                else:
                    s = -b0/a00
                    d_sqrd = s*b0 + c
            else:
                # REGION 0: Compute the (s,t) coordinates by finally
                # deviding by the determinant and evalute the squared
                # distance function.
                s /= det
                t /= det
                d_sqrd = (s * (s*a00 + t*a01 + 2.0*b0) +
                          t * (t*a11 + s*a01 + 2.0*b1) + c)
        else:
            if s < 0.0:
                # REGION 2: The minimizer has be on one of the lines s=0
                # or s+t=1 or their intersection.
                g0 = a01 + b0               # grad component g0 = g_0(0,1)
                g1 = a11 + b1               # grad component g1 = g_1(0,1)

                # Check if the direction (1,-1), i.e, direction of s+t=1,
                # is a descent direction by checking the descent condition
                # (1,-1).g(0,1) = g0-g1 < 0.
                if g0 < g1:
                    numer = g1 - g0
                    denom = a00 - 2.0*a01 + a11

                    if numer >= denom:
                        s = 1.0
                        t = 0.0
                        d_sqrd = a00 + 2.0*b0 + c
                    else:
                        s = numer/denom
                        t = 1.0 - s
                        d_sqrd = (s * (s*a00 + t*a01 + 2.0*b0) +
                                  t * (s*a01 + t*a11 + 2.0*b1) + c)
                else:
                    # The minimizer is contained in the line s=0. Check if
                    # it is an interior point or a vertex.
                    s = 0.0
                    # Descent condition: (0,-1).g(0,1) = -g1 < 0
                    if g1 <= 0.0:
                        t = 1.0
                        d_sqrd = a11 + 2.0*b1 + c
                    elif b1 >= 0.0:
                        t = 0.0
                        d_sqrd = c
                    else:
                        t = -b1/a11
                        d_sqrd = t*b1 + c
            elif t < 0.0:
                # REGION 6: The minimizer has to be on one of the lines t=0
                # or s+1=1 or their intersection.
                g0 = a00 + b0               # grad component g0 = g_0(1,0)
                g1 = a01 + b1               # grad component g1 = g_1(1,0)

                # Check if the direction (-1,1), i.e, direction of s+t=1,
                # is a descent direction by checking the descent condition
                # (-1,1).g(1,0) = g1-g0 < 0.
                if g1 < g0:
                    numer = g0 - g1
                    denom = a00 - 2.0*a01 + a11

                    if numer >= denom:
                        t = 1.0
                        s = 0.0
                        d_sqrd = a11 + 2.0*b1 +c
                    else:
                        t = numer/denom
                        s = 1.0 - t
                        d_sqrd = (s * (s*a00 + t*a01 + 2.0*b0) +
                                  t * (s*a01 + t*a11 + 2.0*b1) + c)
                else:
                    # The minimizer is contained in the line t=0. Check if
                    # it is an interior point or a vertex.
                    t = 0.0
                    # Descent condition: (-1,0).g(0,1) = -g0 < 0
                    if g0 <= 0.0:
                        s = 1.0
                        d_sqrd = a00 + 2.0*b0 + c
                    elif b0 >= 0.0:
                        s = 0.0
                        d_sqrd = c
                    else:
                        s = -b0/a00
                        d_sqrd = s*b0 + c
            else:
                # REGION 1: Minimizer has to be on s+t=1. Check if it is
                # a vertex or an interior point.
                numer = a11 + b1 - a01 - b0

                if numer <= 0.0:
                    s = 0.0
                    t = 1.0
                    d_sqrd = a11 + 2.0*b1 + c
                else:
                    denom = a00 - 2.0*a01 + a11

                    if numer >= denom:
                        s = 1.0
                        t = 0.0
                        d_sqrd = a00 + 2.0*b0 + c
                    else:
                        s = numer/denom
                        t = 1.0 - s
                        d_sqrd = (s * (s*a00 + t*a01 + 2.0*b0) +
                                  t * (s*a01 + t*a11 + 2.0*b1) + c)

        # Can happen due to numerical round-off error. Force the squared
        # distance to be positive.
        if d_sqrd < 0.0: d_sqrd = 0.0

        # Return the closest point and the squared distance to it.
        return self._a + s*e0 + t*e1, d_sqrd

    def _project(self, x):
        """ Closest point projection (internal method).

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        ndarray
            Closest point.
        float
            Squared distance to the closest point.
        """
        # Position vector of x relative to triangle origin.
        ax = x-self._a

        # Solve the linear syste Ay = ax to get coordinates of x with
        # respect to the local frame (a; b-a, c-a, n).
        if self._solver == 'lu':
            alpha = scipy.linalg.lu_solve((self._lu, self._pivot), ax)
        elif self._solver == 'pinv':
            alpha= self._A @ ax
        else:
            alpha = np.linalg.solve(self._A, ax)

        # Barycentric coordinates of the point in the plane spanned by abc
        # closest to the query point x.
        alpha = (1.0-alpha[0]-alpha[1], alpha[0], alpha[1])

        if alpha[0] >= 0.0 and alpha[1] >= 0.0 and alpha[2] >= 0.0:
            # Closest point p to x is contained inside the triangle.
            p = alpha[0]*self._a + alpha[1]*self._b + alpha[2]*self._c
            v = x-p
            return p, np.dot(v, v)
        else:
            # Closest point has to be on one of the edges, can also be a
            # vertex. Test all edges.
            p, d_sqrd = Edge(self._b, self._c).project(x)
            q, e_sqrd = Edge(self._c, self._a).project(x)
            if e_sqrd < d_sqrd:
                p, d_sqrd = q, e_sqrd

            q, e_sqrd = Edge(self._a, self._b).project(x)
            if e_sqrd < d_sqrd:
                p, d_sqrd = q, e_sqrd

            return p, d_sqrd

    def _coords(self, x):
        """ Barycentric coordinates.

        Parameters
        ----------
        x : ndarray
            Query point coordinates.

        Returns
        -------
        ndarray
            Barycentric coordinates of the point that is closest to the query
            point in the plane spanned by the triangle.
        """
        # Difference vector relative to the triangle origin.
        ax = x-self._a

        # Solve the linear syste Ay = ax to get coordinates of x with
        # respect to the local frame (a, b-a, c-a, n).
        if self._solver == 'lu':
            alpha = scipy.linalg.lu_solve((self._lu, self._pivot), ax)
        elif self._solver == 'pinv':
            alpha = self._A @ ax
        else:
            alpha = np.linalg.solve(self._A, ax)

        # Barycentric coordinates of the point in the plane spanned by abc
        # closest to the query point x.
        return np.array([1.0-alpha[0]-alpha[1], alpha[0], alpha[1]])

    def dist_sqrd(self, x):
        """ Squared distance function.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Query point.

        Returns
        -------
        float
            Squared distance of the query point ``x`` to this triangle.
        """
        return self.project(x)[1]

    def contained_in(self, x, rsqrd):
        """ Containment test.

        Test whether this triangle is contained in a given sphere.

        Parameters
        ----------
        x : ~numpy.ndarray, shape (n,)
            Sphere center.
        rsqrd : float
            Squared radius of the sphere.

        Returns
        -------
        bool
            :obj:`True` if this triangle is inside the given sphere.
        """
        # Each row holds a difference vector. Compute the element wise
        # product, then sum each row.
        v = np.array([x-self._a, x-self._b, x-self._c])
        return np.all(np.sum(v*v, axis=-1) <= rsqrd)

    def _update_dim(self):
        self._dim = self._a.size

    def _update_center(self):
        self._center = (self._a + self._b + self._c)/3.0

    def _update_bbox(self):
        self._bbox = (np.min([self._a, self._b, self._c], axis=0),
                      np.max([self._a, self._b, self._c], axis=0))


class Icosphere:
    """ Icosahedron and geodesic sphere.

    See https://en.wikipedia.org/wiki/Regular_icosahedron.
    """

    def __init__(self, radius=1.0, depth=0):
        """ Initialize geodesic sphere.

        Parameters
        ----------
        radius : float, optional
            Radius of the shphere. Always centered at the origin.
        depth : int, optional
            Subdivision depth, 0 corresponds to an Icosahedron.
        """
        phi = 0.5 * (1.0 + np.sqrt(5.0))
        r = np.sqrt(1.0 + phi*phi)
        a = radius/r
        b = radius*(phi/r)

        self.V = np.array([[-a, 0., b], [a, 0., b], [-a, 0., -b], [a, 0., -b],
                           [0., b, a], [0., b, -a], [0., -b, a], [0., -b, -a],
                           [b, a, 0.], [-b, a, 0.], [b, -a, 0.], [-b, -a, 0.]],
                           dtype=float)
        self.F = np.array([[0, 4, 1], [0, 9, 4], [9, 5, 4], [4, 5, 8],
                           [4, 8, 1], [8, 10, 1], [8, 3, 10], [5, 3, 8],
                           [5, 2, 3], [2, 7, 3], [7, 10, 3], [7, 6, 10],
                           [7, 11, 6], [11, 0, 6], [0, 1, 6], [6, 1, 10],
                           [9, 0, 11], [9, 11, 2], [9, 2, 5], [7, 2, 11]],
                           dtype=int)
        self.radius = radius
        self.subdivide(depth)

    def subdivide(self, depth=1):
        """ Subdivision.

        Only move/scale the coordinate attribute V once the desired level
        of subdivision is reached!

        Parameters
        ----------
        depth : int, optional
            Apply the given number of subdivision steps.
        """
        if depth > 0:
            edge_to_idx = {}
            F_new = np.empty((0, 3), dtype=int)

            for t in self.F:
                for i in range(3):
                    edge = (t[i], t[(i+1)%3])

                    if (edge[1], edge[0]) in edge_to_idx:
                        idx = edge_to_idx[(edge[1], edge[0])]
                        edge_to_idx[edge] = idx
                    else:
                        idx = len(self.V)
                        edge_to_idx[edge] = idx
                        v = 0.5 * (self.V[edge[0]]+self.V[edge[1]])
                        v *= self.radius/np.linalg.norm(v)
                        self.V = np.vstack((self.V, v))

                e0 = (t[0], t[1])
                e1 = (t[1], t[2])
                e2 = (t[2], t[0])

                tris = np.array(
                    [[t[0], edge_to_idx[e0], edge_to_idx[e2]],
                    [t[1], edge_to_idx[e1], edge_to_idx[e0]],
                    [t[2], edge_to_idx[e2], edge_to_idx[e1]],
                    [edge_to_idx[e0], edge_to_idx[e1], edge_to_idx[e2]]],
                    dtype=int)

                F_new = np.vstack((F_new, tris))

            self.F = F_new
            self.subdivide(depth-1)


class Node:
    """ Generic node of a BSP tree.

    Items stored in the data field need to provide ``dim``, ``center``, and
    ``bbox`` properties as well as methods ``project()``, ``contained_in()``,
    and ``dist_sqrd()``. See :class:`Triangle` for an example.

    Note
    ----
    BSP tree nodes are low-level objects that should not be created manually.
    They are created automatically when building a search tree for a given set
    of geometric objects. To this end :class:`BHVTree` provides several generic
    initializers such as :meth:`~BVHTree.from_points` and others.
    """

    def __init__(self, lo, hi, dim, val, bb_min, bb_max, data=None):
        """ Constructor.

        The first four arguments are meaningless for leaf nodes and should
        be set to :py:obj:`None` in this case. Bounding box corners always
        need to hold valid values.

        Parameters
        ----------
        lo : Node
            Root of left subtree.
        hi : Node
            Root of right subtree.
        dim : int
            Discriminator dimension.
        val : float
            Discriminator value.
        bb_min : ~numpy.ndarray
            Lower left corner of the node's bounding box.
        bb_max : ~numpy.ndarray
            Upper right corner of the node's bounding box.
        data
            A collection of data items. Supposed to be :obj:`None` for
            interior nodes.


        Discriminator value ``val`` and discriminator dimension ``dim`` split
        ambient space into two half-spaces
        :math:`\{ x | x_{\\textrm{dim}} \leq \\textrm{val}\}` and
        :math:`\{ x | x_{\\textrm{dim}} > \\textrm{val}\}`.

        ``bb_min`` and ``bb_max`` are supposed to hold the lower left and
        upper right corner of a tight bounding box that contains all data
        items stored in the subtree with root ``node``.
        """
        self._lo = lo                       # left subtree root
        self._hi = hi                       # right subtree root
        self._dim = dim                     # splitting dimension
        self._val = val                     # splitting value
        self._bb_min = bb_min               # bounding box lower left
        self._bb_max = bb_max               # bounding box upper right
        self._data = data                   # some geometric shapes

    @property
    def lo(self):
        """ Root of left subtree.

        Returns
        -------
        Node
            The root node of the left subtree, can be :obj:`None`.
        """
        return self._lo

    @property
    def hi(self):
        """ Root of right subtree.

        Returns
        -------
        Node
            The root node of the right subtree, can be :obj:`None`.
        """
        return self._hi

    @property
    def dim(self):
        """ Discriminator dimension.

        Returns
        -------
        int
            Together with the value provided by :py:attr:`val` it defines
            a hyperplane :math:`x_{\\textrm{dim}} = \\textrm{val}`.
            :obj:`None` for leaf nodes.
        """
        return self._dim

    @property
    def val(self):
        """ Discriminator value.

        Returns
        -------
        float
            Together with the value provided by :py:attr:`dim` it defines
            a hyperplane :math:`x_{\\textrm{dim}} = \\textrm{val}`.
            :obj:`None` for leaf nodes.
        """
        return self._val

    @property
    def bb_min(self):
        """ Bounding box vertex.

        Returns
        -------
        ndarray
            Bounding box vertex holding the minimal value for each
            coordinate dimension.
        """
        return self._bb_min

    @property
    def bb_max(self):
        """ Bounding box vertex.

        Returns
        -------
        ndarray
            Bounding box vertex holding the maximal value for each
            coordinate dimension.
        """
        return self._bb_max

    @property
    def data(self):
        """ Node data.

        Returns
        -------
        list[int]
            Numerical identifiers of data items associated with this node.
            :obj:`None` for interior nodes.
        """
        return self._data

    def isleaf(self):
        """ Leaf node check.

        Returns
        -------
        bool
            :obj:`True` if the node is a leaf node.
        """
        return self._data is not None


class KDTree:
    """ Point based kD-tree.
    """

    def __init__(self, P, leafsize=2, median_split=True):
        """
        """
        t_start = time.time()

        self.points = np.asarray(P)
        self.leafsize = leafsize
        self.median_split = median_split
        self.root = self._build(list(range(len(self.points))))

        t_end = time.time()

        print('--- kD-Tree Summary ---')
        print('', len(self.points), 'points')
        print('', 'bounding box:', self.root.bb_min, self.root.bb_max)
        print('', 'build time:', t_end-t_start, 'seconds')
        print()

    def project(self, x):
        """ Project a point onto the data set.
        """
        self.query(x)
        return self.nn_idx

    def query(self, x):
        """
        """
        # Store the query point in an instance variable and start the
        # recursive search process.
        self.x = np.asarray(x)
        self.nn_d_sqrd = np.inf
        self.nn_idx = -1
        self._search(self.root)

    def _search(self, node):
        """
        """
        if node.data:
            for i in node.data:
                v = self.x - self.points[i]
                d = np.dot(v, v)

                if d < self.nn_d_sqrd:
                    self.nn_d_sqrd = d
                    self.nn_idx = i
        else:
            if self.x[node.dim] <= node.val:
                self._search(node.lo)
                if self._overlaps(node.hi): self._search(node.hi)
            else:
                self._search(node.hi)
                if self._overlaps(node.lo): self._search(node.lo)

    def _overlaps(self, node):
        """
        """
        n = self.x.size                     # number of data dimensions
        d = 0.0                             # squared distance

        for i in range(n):
            if self.x[i] > node.bb_max[i]:
                v = self.x[i]-node.bb_max[i]
                d += v*v

            if self.x[i] < node.bb_min[i]:
                v = self.x[i]-node.bb_min[i]
                d += v*v

        return d < self.nn_d_sqrd

    def _build(self, I):
        """ Build subtree of data given by the index set I.
        """
        bb_min = np.min(self.points[I], 0)
        bb_max = np.max(self.points[I], 0)

        # did we reach the bucket size? we allow at most two points in the
        # same bucket (leaf node).
        if len(I) < self.leafsize:
            return Node(None, None, None, None, I, bb_min, bb_max)
        else:
            L, H, dim, val = self._partition(I)
            lo = self._build(L)
            hi = self._build(H)

            return Node(lo, hi, dim, val, None, bb_min, bb_max)

    def _partition(self, I):
        """
        """
        # Extract the points from P that correspond to given I then sort
        # each column individually.
        Q = self.points[I, :]
        S = np.sort(Q, axis=0)

        # Split the dimension of largest spread in data values. Split
        # occures either along the mean (default) or median value.
        spread = S[-1]-S[0]
        dim = np.argmax(spread)
        val = 0.5 * (S[0, dim]+S[-1, dim])

        if self.median_split:               # split at median value?
            idx = len(S)//2 - 1
            val = S[idx, dim]

        L = []                              # lo son (left of val)
        H = []                              # hi son (right of val)

        # Partition the data such that all data points in dimension dim
        # are either less or greater than the value val
        for i in I:
            if self.points[i, dim] <= val:
                L.append(i)
            else:
                H.append(i)

        assert len(L) and len(L) < len(I)
        assert len(H) and len(H) < len(I)

        return L, H, dim, val

    def print(self):
        """
        Textual representation of the tree
        """
        self.print_node(self.root, 0)

    def print_node(self, node, level):
        """
        """
        space = ' ' * int(level)

        # print information on the bounding box
        print(space, node.bb_min)
        print(space, node.bb_max)

        # print the data or recurse
        if node.data:
            print(space, 'data:', node.data)
        else:
            self.print_node(node.lo, level+4)
            self.print_node(node.hi, level+4)


class BVHTree:
    """ Bounding Volume Hierarchy tree.

    `Overview <https://en.wikipedia.org/wiki/Bounding_volume_hierarchy>`_ of
    bounding volume hierarchy trees and possible variations.
    """

    def __init__(self, items, leafsize=8, mediansplit=True, debug=False):
        """ BVH tree initializer.

        Parameters
        ----------
        items : iterable
            Input shapes. Changes to data items will invalidate the tree.
        leafsize : int
            The maximum number of data items stored in a leaf node.
        mediansplit : bool
            Whether to use the median split heuristic or not.
        debug : bool
            Generate tree traversal information during search queries.

        Raises
        ------
        ValueError
            If data items dimensions are not consistent.


        Items need to provide ``dim``, ``center``, and ``bbox`` properties
        as well as methods ``project()``, ``dist_sqrd()``, and
        ``contained_in()``, see e.g. :class:`Triangle` for details.

        For convenience the methods :meth:`from_points`, :meth:`from_trimesh`,
        and :meth:`from_trimesh_edges` are provided for initialization from a
        point cloud and a triangle mesh.
        """
        self._t_start = time.time()         # start the timer ...

        # Store a reference to the original data items. Internally we refer
        # to items by their position in the items container.
        self._items = items
        self._leafsize = leafsize
        self._mediansplit = mediansplit
        self._dim = items[0].dim

        # The dimension should be consistenst across all provided data items.
        # The computed list of indices should be empty.
        idx = [i for i, item in enumerate(items) if item.dim != self._dim]

        if idx:
            msg = '__init__(): data item dimensions are inconsistent!'
            raise ValueError(msg)

        # Build the tree. When done leaf node data containers hold indices
        # of data items.
        self._root = self._build(list(range(len(items))))

        # Use the _debug setter to initialize related attributes correctly.
        self.debug = debug

        self._t_end = time.time()           # ... stop the timer.

    def __str__(self):
        """ Info string.

        Returns
        -------
        str
            High level information about the build process and resulting
            size of the tree.
        """
        rep  = f'BVHTree      : {len(self._items)} items stored\n'
        rep += f'dimension    : {self._dim}\n'
        rep += f'leaf size    : {self._leafsize}\n'
        rep += f'bounding box : {self._root.bb_min}, {self._root.bb_max}\n'
        rep += f'build time   : {self._t_end-self._t_start} seconds'

        return rep

    def __repr__(self):
        """ Tree representation.

        Useful for non-graphical debugging on small data sets.

        Returns
        -------
        str
            Graph like representation of the tree.
        """
        file = io.StringIO()
        self._print(file)
        str = file.getvalue()
        file.close
        return str

    @staticmethod
    def from_points(P, **kwargs):
        """ BVH tree from a point cloud.

        Parameters
        ----------
        P : array_like, shape (n,), n > 1
            Input point set.

        Keyword Arguments
        -----------------
        leafsize : int
            The maximum number of data items stored in a leaf node.
        mediansplit : bool
            Whether to use the median split heuristic or not.
        debug : bool
            Generate tree traversal information during search queries.
        """
        points = [Point(p) for p in P]
        return BVHTree(points, **kwargs)

    @staticmethod
    def from_trimesh_edges(M, **kwargs):
        """ BVH tree from a triangle mesh.

        Builds a BVH tree using the edges of a mesh as data items.

        Parameters
        ----------
        M
            A triangle mesh.

        Keyword Arguments
        -----------------
        leafsize : int
            The maximum number of data items stored in a leaf node.
        mediansplit : bool
            Whether to use the median split heuristic or not.
        debug : bool
            Generate tree traversal information during search queries.

        Raises
        ------
        ValueError
            If ``M`` is not of the correct type.


        There are no topological restrictions on the triangle mesh ``M``.
        The face set can be an arbitrary soup of triangles. It can be given
        as a halfedge mesh or and indexed mesh, i.e., as a pair (V, F).
        """
        raise NotImplementedError()

    @staticmethod
    def from_trimesh(M, **kwargs):
        """ BVH tree from a triangle mesh.

        Builds a BVH tree using the triangular faces of a mesh as data items.

        Parameters
        ----------
        M
            A triangle mesh.

        Keyword Arguments
        -----------------
        leafsize : int
            The maximum number of data items stored in a leaf node.
        mediansplit : bool
            Whether to use the median split heuristic or not.
        debug : bool
            Generate tree traversal information during search queries.

        Raises
        ------
        ValueError
            If ``M`` is not of the correct type.


        There are no topological restrictions on the triangle mesh ``M``.
        The face set can be an arbitrary soup of triangles. It can be given
        as a halfedge mesh or and indexed mesh, i.e., as a pair (V, F).
        """
        try:
            # Raises AttributeError if M is not derived from a halfedge
            # based mesh representation.
            M.num_faces()
        except AttributeError:
            try:
                # Try if M is given as an indexed mesh. If this is also
                # not the case we cannot proceed.
                V = M[0]
                F = M[1]
            except (TypeError, IndexError):
                msg = 'from_trimesh(): cannot interpret M as a mesh!'
                raise ValueError(msg)
            else:
                tris = [Triangle(V[f[0]], V[f[1]], V[f[2]]) for f in F]
        else:
            tris = [Triangle(*[v.point for v in f.vertices()])
                    for f in M.faces()]

        return BVHTree(tris, **kwargs)

    @property
    def root(self):
        """ Root node.

        Returns
        -------
        node : Node
            The root node of the tree.
        """
        return self._root

    @property
    def items(self):
        """ Tree items.

        Returns
        -------
        items
            Data items as specified during tree construction.
        """
        return self._items

    @property
    def dim(self):
        """ Data dimension.

        Returns
        -------
        dim : int
            Ambient space dimension in which the data items live.
        """
        return self._dim

    @property
    def bbox(self):
        """ Bounding box.

        Returns
        -------
        bb_min : ndarray
            Lower left bounding box corner.
        bb_max : ndarray
            Upper right bounding box corner.
        """
        return self._root._bb_min, self._root._bb_max

    @property
    def debug(self):
        """ Get and set debug flag.

        In debug mode additional tree traveral information is generated and
        stored for later inspection. Debug mode can be turned on and off in
        between search queries. The generated data can be inspected via the
        properties :py:attr:`visited_nodes`, :py:attr:`visited_leafs`, and
        :py:attr:`visited_items`.

        Returns
        -------
        bool
            :py:obj:`True` is debug mode is enabled.
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        """ Debug flag setter method.
        """
        # Set _debug flag and initialize the corresponding attributes
        # accordingly.
        self._debug = bool(value)

        if self._debug:
            self._visited_nodes = []        # nodes in visited order
            self._visited_leafs = []        # leafs in visited order
            self._visited_items = []        # items in visited order
        else:
            self._visited_nodes = None
            self._visited_leafs = None
            self._visited_items = None

    @property
    def visited_nodes(self):
        """ Visited nodes in latest tree traversal.

        Returns
        -------
        list[Node]
            List of visited nodes in the order they appeared during the
            last search query. :obj:`None` if the debug flag was set to
            :obj:`False`.
        """
        return self._visited_nodes

    @property
    def visited_leafs(self):
        """ Visited leaf nodes in latest tree traversal.

        Returns
        -------
        list[Node]
            List of visited leaf nodes in the order they appeared during
            the last search query. :obj:`None` if the debug flag was set
            to :obj:`False`.
        """
        return self._visited_leafs

    @property
    def visited_items(self):
        """ Visited items during search.

        Returns
        -------
        list[int]
            List of item identifiers that have been visited during the
            latest tree traversal. :obj:`None` if the debug flag was
            set to :obj:`None`.
        """
        return self._visited_items

    def project(self, x):
        """ Closest point projection.

        Given :math:`m` data items :math:`D_i` the main purpose of this
        function is to compute the coordinates of the point
        :math:`\mathbf{p}` such that

        .. math::

             \mathbf{p} = \\arg \min
             \{ \|\mathbf{p} - \mathbf{x}\|\ |\ \mathbf{p} \in D_i
             ,\ i = 1, \dots, m\}

        Parameters
        ----------
        x : array_like
            Query point coordinates.

        Returns
        -------
        idx : int
            Identifier of closest data item.
        p : ndarray
            Closest point coordinates.
        dsqrd : float
            Squared distance.
        """
        self.query(x)
        return self._nn_idx[0], self._nn_prj_x[0], self._nn_d_sqrd[0]

    def intersect(self, x, v):
        """ Ray intersection.

        Computes the coordinates of intersection points along the ray emanating
        from :math:`\mathbf{x}` in direction of :math:`\mathbf{v}` with all
        data items.

        Parameters
        ----------
        x : array_like
            Coordinates of ray origin.
        v : array_like
            Ray direction vector.

        Returns
        -------
        idx : list[int]
            Identifiers of intersected data items.
        t : list[float]
            Scalar :math:`t_j` with :math:`t_j < t_{j+1}` such that
            :math:`\mathbf{p}_j = \mathbf{x} + t_j \mathbf{v}` is the
            :math:`j`-th intersection point of the ray with the data set.
        dsqrd : list[float]
            Squared distances to ray origin.
        """
        raise NotImplementedError()

    def query(self, x, k=1):
        """ k-nearest neighbor search query.

        Computes the identifiers of the k closest data items. The closest
        point coordinates and squared distances are also computed.

        Parameters
        ----------
        x : array_like
            Query point coordinates.
        k : int
            The k in k-nearest neighbor search.

        Returns
        -------
        idx : list[int]
            Identifiers of the k closest data items.
        coord : list[ndarray]
            Corresponding closest points coordinates.
        dsqrd : list[float]
            Squared distances to corresponding data items.


        The returned lists are sorted by increasing distance to the query
        point ``x``. The i-th element of each list corresponds to the
        i-nearest data item found.

        Note
        ----
        For point data items the returned coordinates are the same as the
        coordinates of the point data item. For more complex data items like
        triangles ``coord[i]`` corresponds to the closest point inside the
        i-nearest triangle to the query point. ``idx[i]`` is the identifier
        of this triangle.
        """
        if self._debug:
            self._visited_nodes = []        # nodes in visited order
            self._visited_leafs = []        # leafs in visited order
            self._visited_items = []        # items in visited order

        # Priority queue based implementation that can find the k-nearest
        # neighbors to the query point. The heapq algorithm turns a list of
        # items into a list that satisfies the minheap property.
        self._knn = []

        # Initialization: heap elements are triples (-d_sqrd, idx, coord).
        # Consequently heap[0] will be the k-closest item discovered so far.
        for i in range(k):
            heapq.heappush(self._knn, (-np.inf, -(i+1), None))

        # Store the query point in an instance variable and start the
        # recursive search process.
        self._x = np.asarray(x)
        self._search(self._root)

        # The seach result can now be read off from the self._knn. We store
        # the result in three separate lists.
        self._nn_d_sqrd = []
        self._nn_idx = []
        self._nn_prj_x = []

        while self._knn:
            # If k is larger than the number of data items there are still
            # inf values on the heap. Those need to be popped first.
            item = heapq.heappop(self._knn)

            if np.isfinite(item[0]):
                self._nn_d_sqrd.append(-item[0])
                self._nn_idx.append(item[1])
                self._nn_prj_x.append(item[2])

        # Order needs to be reversed since the items were popped from the
        # heap in the order k-closest, (k-1)-closest etc.
        self._nn_d_sqrd.reverse()
        self._nn_idx.reverse()
        self._nn_prj_x.reverse()

        return self._nn_idx, self._nn_prj_x, self._nn_d_sqrd

    def range_query(self, x, d):
        """ Range query.

        Find all data items of distance less than or equal to a prescribed
        distance from the query point.

        Parameters
        ----------
        x : array_like
            Query point coordinates
        d : float
            Distance value.

        Returns
        -------
        idx : list[int]
            Item identifiers.
        coord : list[ndarray]
            Closest point coordinates.
        dsqrd : list[float]
            Squared distances to the query point.


        The returned lists are sorted by increasing distance to the query
        point ``x``. The i-th element of each list corresponds to the
        i-nearest data item found.
        """
        if self._debug:
            self._visited_nodes = []        # nodes in visited order
            self._visited_leafs = []        # leafs in visited order
            self._visited_items = []        # items in visited order

        # All data items within the given distance are reported in ascending
        # distance in the heap instance attribute _knn.
        self._knn = []
        self._x = np.asarray(x)
        self._range_search(self._root, d*d)

        # The search result can now be read off from self._knn. We store the
        # result in three separate lists.
        self._nn_d_sqrd = []
        self._nn_idx = []
        self._nn_prj_x = []

        while self._knn:
            item = heapq.heappop(self._knn)
            self._nn_d_sqrd.append(-item[0])
            self._nn_idx.append(item[1])
            self._nn_prj_x.append(item[2])

        return self._nn_idx, self._nn_prj_x, self._nn_d_sqrd

    def nodes(self):
        """ Node iterator.

        In order traversal of all nodes of the tree.

        Yields
        ------
        Node
            A node of the tree.
        """
        stack = []
        stack.append(self._root)

        while stack:
            node = stack.pop()
            yield node

            if node._hi is not None: stack.append(node._hi)
            if node._lo is not None: stack.append(node._lo)

    def leaf_nodes(self):
        """ Leaf node iterator.

        In order traversal of all leaf nodes of the tree.

        Yields
        ------
        Node
            A leaf node of the tree.
        """
        # Yield does not make sense in recusive function calls. The yielded
        # item will never reach the caller. Instead we use a stack to model
        # the call frames in a recursive function call.
        stack = []
        stack.append(self._root)

        while stack:
            node = stack.pop()

            if node.isleaf():
                yield node

            if node._hi is not None: stack.append(node._hi)
            if node._lo is not None: stack.append(node._lo)

    def _search(self, node):
        """ Tree search.

        Recursively searches the tree rooted at a given node. Results and
        state of the search are tracked via instance variables.

        Parameters
        ----------
        node : Node
            Subtree root node.
        """
        if node is None:
            return

        if self._debug:
            self._visited_nodes.append(node)

        if node.isleaf():
            if self._debug:
                self._visited_leafs.append(node)

            # Check if the currently discovered k-closest point can be
            # improved by any item stored in the current leaf node's data.
            for i in node.data:
                prj, d_sqrd = self._items[i].project(self._x)

                # Compare different ways of computing closest points for
                # triangles, including computation time.
                # if isinstance(self._items[i], Triangle):
                #     t_prj_s = time.time()
                #     prj, d_sqrd = self._items[i].project(self._x)
                #     t_prj_e = time.time()

                #     t_qrj_s = time.time()
                #     qrj, e_sqrd = self._items[i]._project(self._x)
                #     t_qrj_e = time.time()

                #     t_prj_d = t_prj_e-t_prj_s
                #     t_qrj_d = t_qrj_e-t_qrj_s

                #     print(f'absolute: {t_prj_d} vs {t_qrj_d}, ' +
                #           f'ratio: {t_qrj_d/t_prj_d}')

                #     if (np.abs(d_sqrd-e_sqrd) > 1e-12
                #             or np.linalg.norm(prj-qrj) > 1e-12):
                #         print('prj_x  :', prj, ' -- ', qrj)
                #         print('d_sqrd :', d_sqrd, ' -- ', e_sqrd)
                #         raise RuntimeError()

                # Update the heap that holds information about the
                # k-nearest neighbors.
                if d_sqrd < -self._knn[0][0]:
                    heapq.heapreplace(self._knn, (-d_sqrd, i, prj))

                if self._debug:
                    self._visited_items.append(i)
        else:
            if self._x[node._dim] <= node._val:
                self._search(node._lo)
                if self._ball_overlaps(node._hi, -self._knn[0][0]):
                    self._search(node._hi)
            else:
                self._search(node._hi)
                if self._ball_overlaps(node._lo, -self._knn[0][0]):
                    self._search(node._lo)

    def _range_search(self, node, rsqrd):
        """ Range search.

        Parameters
        ----------
        node : Node
            Subtree root node.
        rsqrd : float
            Squared radius of a ball centerd at the query point.
        """
        if node is None:
            return

        # For a leaf node all items of that leaf inside the ball have to
        # be reported. If a node's bounding box is contained in this ball
        # the whole subtree can be reported immediately without checking.
        if node.isleaf():
            self._report(node, rsqrd)
        elif self._ball_contains(node, rsqrd):
            self._report(node, rsqrd)
        else:
            # _report takes care of adding nodes to the visited nodes list.
            # This is the only place where _range_search has to do this.
            if self._debug:
                self._visited_nodes.append(node)

            if self._ball_overlaps(node._lo, rsqrd):
                self._range_search(node._lo, rsqrd)

            if self._ball_overlaps(node._hi, rsqrd):
                self._range_search(node._hi, rsqrd)

    def _report(self, node, rsqrd):
        """ Report data items.

        Reports all data items of a subtree that are within a ball of
        given radius centered at the query point. Items are reported by
        putting them into the _knn heap instance attribute.

        Parameters
        ----------
        node : Node
            Subtree root node.
        rsqrd : float
            Squared radius of the ball.
        """
        if node is None:
            return

        if self._debug:
            self._visited_nodes.append(node)

        if node.isleaf():
            if self._debug:
                self._visited_leafs.append(node)

            # Report all data items of the leaf that are inside the query
            # ball by putting them in the _knn heap attribute.
            for i in node._data:
                if self._items[i].contained_in(self._x, rsqrd):
                    prj, dsqrd = self._items[i].project(self._x)
                    heapq.heappush(self._knn, (dsqrd, i, prj))

                if self._debug:
                    self._visited_items.append(i)
        else:
            self._report(node._lo, rsqrd)
            self._report(node._hi, rsqrd)

    def _ball_overlaps(self, node, rsqrd):
        """ Overlap test.

        Check if a ball of given radius centered at the query point
        overlaps with the bounding box of a node.

        Parameters
        ----------
        node : Node
            Subtree root node.
        rsqrd : float
            Squared radius of the ball.

        Returns
        -------
        bool
            :obj:`True` if the ball overlaps the node's bounding box.
        """
        if node is None: return False

        # Initialize squared distance to the interior of the bounding
        # box. Updated via the Pythagorean theorem.
        dsqrd = 0.0

        for i in range(self._dim):
            # Distances to bounding box faces only contribute if query
            # point self._x is on the outside.
            if self._x[i] > node.bb_max[i]:
                d = self._x[i]-node.bb_max[i]
                dsqrd += d*d

            if self._x[i] < node.bb_min[i]:
                d = self._x[i]-node.bb_min[i]
                dsqrd += d*d

        # Touching the bounding box does not count as overlap...
        return dsqrd < rsqrd

    def _ball_contains(self, node, rsqrd):
        """ Containment check.

        Check if a ball of given radius centered at the query point
        completely contains a node's bounding box.

        Parameters
        ----------
        node : Node
            Subtree root node.
        rsqrd : float
            Squared radius of the ball.

        Returns
        -------
        bool
            :obj:`True` if the ball contains the node's bounding box.
        """
        if node is None: return False

        # The bounding box vertices as rows in a matrix of shape (2, dim)
        bbox = np.stack((node.bb_min, node.bb_max))

        # Generate a matrix of shape (2^dim, dim) whose rows are difference
        # vectors of bounding box vertices and the center of the sphere.
        idx = [(0,1)]*self._dim
        j = [d for d in range(self._dim)]
        C = np.array([bbox[i,j]-self._x for i in itertools.product(*idx)])

        # The given node is contained in the sphere if all bounding box
        # corners are inside.
        if np.any(np.sum(C*C, axis=-1) > rsqrd): return False

        # The entire bounding box is contained in the query sphere.
        return True

    def _build(self, I):
        """ Build tree.

        Parameters
        ----------
        I : list[int]
            Numerical identifiers of data items.

        Returns
        -------
        Node
            Subtree root node.
        """
        bb = self._bounding_box(I)

        if len(I) <= self._leafsize:
            return Node(None, None, None, None, bb[0], bb[1], I)
        else:
            L, H, dim, val = self._partition(I)
            lo = self._build(L)
            hi = self._build(H)

            return Node(lo, hi, dim, val, bb[0], bb[1], None)

    def _partition(self, I):
        """ Partition data items.

        Parameters
        ----------
        I : list[int]
            Numerical identifiers of data items.

        Returns
        -------
        L : list[int]
            Identifiers of data items that go to the left.
        H : list[int]
            Identifiers of data items that go to the right.
        dim : int
            Splitting dimension.
        val : float
            Discriminator value.
        """
        # Get the geometric center of each shape. Put them as rows of a
        # matrix, then sort columns of this matrix individually.
        C = [self._items[i].center for i in I]
        S = np.sort(C, axis=0)

        # Split the dimension of largest spread in data values. Split
        # occures either along the mean (default) or median value.
        spread = S[-1]-S[0]
        dim = np.argmax(spread)
        val = 0.5 * (S[0, dim]+S[-1, dim])

        if self._mediansplit:              # split at median value?
            idx = len(S)//2 - 1
            val = S[idx, dim]

        L = []                              # lo son (left of val)
        H = []                              # hi son (right of val)

        for i in I:
            # Distribute items. Only depends on the center value in the
            # chosen dimension.
            if self._items[i].center[dim] <= val:
                L.append(i)
            else:
                H.append(i)

        assert len(L) and len(L) < len(I)
        assert len(H) and len(H) < len(I)

        return L, H, dim, val

    def _bounding_box(self, I):
        """ Bounding box.

        Parameters
        ----------
        I : list[int]
            Numerical identifiers of data items.

        Returns
        -------
        ndarray
            Lower left corner of bounding box.
        ndarray
            Upper right corner of bounding box.
        """
        bb = np.asarray([self._items[i].bbox for i in I])
        return np.min(bb[:,0,:], axis=0), np.max(bb[:,1,:], axis=0)

    def _print(self, file):
        """ Graph like tree output.

        Recursively traverses the whole tree starting from the root
        node. Prints information according to node type.
        """
        self._print_node(file, self.root, 0)

    def _print_node(self, file, node, level):
        """ Formatted node output (recursive).

        Helper function used in :meth:`_print`. Prints information
        according to node type.

        Parameters
        ----------
        node : Node
            The node to print.
        level : int
            Depth of the node in the tree.
        """
        # Identation according to the depth/level of the node. All nodes
        # have a bounding box, print its vertices.
        space = ' ' * int(level)
        file.write(f'{space} bbox : {node.bb_min}, {node.bb_max}\n')

        # Print node type specific information. Recurse on the left and
        # right subtrees.
        if node.isleaf():
            file.write(f'{space} data: {node.data}\n')
        else:
            file.write(f'{space} dim : {node.dim}\n')
            file.write(f'{space} val : {node.val}\n')

            if node.lo is not None: self._print_node(file, node.lo, level+4)
            if node.hi is not None: self._print_node(file, node.hi, level+4)
