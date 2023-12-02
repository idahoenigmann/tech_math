# Copyright 2022, Martin Kilian
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

""" Halfedge data structure for orientable 2-manifold meshes.

An orientable 2-manifold mesh is described by maintaining three containers
-- holding :py:class:`Vertex`, :py:class:`Halfedge`, and :py:class:`Face`
objects -- and the relations between them. Those containers and the
respective relations are managed by the :py:class:`Mesh` class.
"""

import geopy.obj as obj


class Vertex:
    """ Vertex base class.

    Typical usage does not require explicit construction of :py:class:`Vertex`
    objects. The preferred way to generate vertices of a mesh and assign
    coordinates is to use the :py:meth:`~Mesh.add_vertex` method:

    .. literalinclude:: ../../examples/mesh_triangle.py
       :lines: 8-14
    """

    def __init__(self, point, he=None):
        """ Vertex initialization.

        Parameters
        ----------
        point :
            Vertex coordinates.
        he : Halfedge, optional
            A halfedge with this vertex as its origin.


        After creation vertex coordinates can be queried and modified via
        the :attr:`point` attribute of a :class:`Vertex` object.

        There is no restriction on the data type used to describe vertex
        coordinates. To describe an abstract vertex without any position a
        unique integer can be used.

        Note
        ----
        To facilitate computation coordinates of type :class:`~numpy.ndarray`
        and shape (n, ) are recommended for a mesh embedded in
        :math:`\mathbb{R}^n`.
        """
        self.point = point                  # coordinates/identifier
        self._halfedge = he                 # outgoing halfedge attribute
        self._idx = -1                      # vertex index
        self._deleted = False               # deleted flag

    def __repr__(self):
        """ Object representation.

        Returns
        -------
        str
            String description of a vertex.
        """
        return f'v {self.index}: {self.point} of type {type(self.point)}'

    def __str__(self):
        """ String representation.

        Returns
        -------
        str
            String description of a vertex.
        """
        return f'v {self.point}'

    @property
    def halfedge(self):
        """ Outgoing halfedge.

        A halfedge that starts at the given vertex.

        Returns
        -------
        Halfedge
            Outgoing halfedge or :obj:`None` when the vertex is isolated.
        """
        return self._halfedge

    @property
    def index(self):
        """ Vertex index.

        Returns
        -------
        int
            Current position of the vertex in the list of all vertices.
            A negative index signales that the vertex is not part of a mesh.

        Warning
        -------
        The vertex index is not a persistent vertex identifier! Vertex
        indices change when the vertex container of a mesh is reorganized.
        """
        return self._idx

    @property
    def degree(self):
        """ Vertex degree.

        Returns
        -------
        int
            Number of adjacent vertices.

        Note
        ----
        A degree zero vertex is unused/isolated, i.e., it is not connected
        to any other mesh items.
        """
        # Isolated/unused/deleted vertices are not connected to any
        # edges/faces of the mesh.
        if not self._halfedge: return 0

        # Note: dangling vertices, i.e., endpoints of dangling edges are
        # the only vertices with valence 1. A vertex should only be in this
        # state during mesh construction!
        deg = 0
        h = self._halfedge

        while True:
            deg += 1
            h = h._pair._next
            if h is self._halfedge: return deg

    @property
    def valence(self):
        """ Same as vertex degree.
        """
        return self.degree

    def halfedges(self):
        """ Incident halfedge iterator.

        Generator function for counterclockwise (i.e., positive) iteration
        over the outgoing halfedges incident with a vertex.

        Yields
        ------
        Halfedge
            Outgoing halfedge.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # isolated vertex

        while True:
            yield h
            h = h._prev._pair               # next iterate
            if h is self._halfedge: break   # termination condition

    def halfedges_cw(self):
        """ Incident halfedge iterator.

        Generator function for clockwise (i.e., negative) iteration over
        the outgoing halfedges incident with a vertex.

        Yields
        ------
        Halfedge
            Outgoing halfedge.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # isolated vertex

        while True:
            yield h
            h = h._pair._next               # next iterate
            if h is self._halfedge: break   # termination condition

    def vertices(self):
        """ Adjacent vertex iterator.

        Generator function for counterclockwise (i.e., positve) iteration
        over adjacent vertices.

        Yields
        ------
        Vertex
            Adjacent vertex.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # isolated vertex

        while True:
            yield h._target
            h = h._prev._pair               # next iterate
            if h is self._halfedge: break   # termination condition

    def faces(self):
        """ Incident face iterator.

        Generator function for counterclockwise (i.e., positve) iteration
        over incident faces.

        Yields
        ------
        Face
            Incident face.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # empty face

        while True:
            if h._face: yield h._face
            h = h._prev._pair               # next iterate
            if h is self._halfedge: break   # termination condition

    def isdeleted(self):
        """ Vertex status.

        Returns
        -------
        bool
            :py:obj:`True` if deleted.

        Warning
        -------
        Deleted vertices are removed from a mesh when calling
        :meth:`~Mesh.clean`. This will invalidate previously obtained vertex
        indices!
        """
        return self._deleted

    def isisolated(self):
        """ Isolated vertex test.

        Same as :meth:`isunused`.

        Returns
        -------
        bool
            :obj:`True` if the vertex is not connected to any other
            mesh items.
        """
        return not bool(self._halfedge)

    def isunused(self):
        """ Unused vertex test.

        Same as :meth:`issolated`.

        Returns
        -------
        bool
            :obj:`True` if the vertex is not connected to any other
            mesh items.
        """
        return self.isisolated()

    def isboundary(self):
        """ Boundary vertex test.

        Isolated vertices are considered boundary vertices -- they form
        their own connected component.

        Returns
        -------
        bool
            :obj:`True` if the vertex is isolated or incident with a
            boundary halfedge.
        """
        h = self._halfedge
        if not h: return True

        while True:
            if h.isboundary(): return True
            h = h._prev._pair
            if h is self._halfedge: break

        return False


class Halfedge:
    """
    Halfedge base class.

    Halfedges store references to their vertices, the successor, predecessor,
    and twin halfedge as well as the incident face. A closed loop of halfedges
    defines a face and its orientation. Successor and predecessor refer to
    the next and previous halfedge in such a loop.

    .. image:: ../figures/halfedge_attr.png
       :width: 35 %
       :align: center
    """

    def __init__(self, v, w, next=None, prev=None, pair=None, face=None):
        """ Halfedge initialization.

        Parameters
        ----------
        v : Vertex
            Origin of the halfedge.
        w : Vertex
            Target of the halfedge.
        next : Halfedge, optional
            The successor halfedge.
        prev : Halfedge, optional
            The previous halfedge.
        pair : Halfedge, optional
            The opposite halfedge.
        face : Halfedge, optional
            The incident face.

        Note
        ----
        :py:class:`Halfedge` objects are automatically generated and have all
        attributes initialized when adding a face via :py:meth:`~Mesh.add_face`.
        """
        self._origin = v                    # origin vertex
        self._target = w                    # target vertex
        self._next = next                   # successor halfedge
        self._prev = prev                   # previous halfedge
        self._pair = pair                   # opposite halfedge
        self._face = face                   # incident face
        self._deleted = False               # halfedge status

    def __repr__(self):
        """ Object representation.

        Returns
        -------
        str
            String description of a halfedge.
        """
        return f'h [{repr(self.origin)}\n   {repr(self.target)}]'

    def __str__(self):
        """ String representation.

        Returns
        -------
        str
            String description of a halfedge.
        """
        return f'h {[self.origin.index, self.target.index]}'

    def __contains__(self, v):
        """ Vertex containment test.

        Parameters
        ----------
        v : Vertex
            A vertex to be tested for incidence with the halfedge.

        Returns
        -------
        bool
            :obj:`True` if the given vertex is one of the halfedge's
            endpoints.
        """
        return (v is self._origin) or (v is self._target)

    @property
    def origin(self):
        """ Origin vertex.

        Returns
        -------
        Vertex
            Halfedge origin vertex.
        """
        return self._origin

    @property
    def target(self):
        """ Target vertex.

        Returns
        -------
        Vertex
            Halfedge target vertex.
        """
        return self._target

    @property
    def next(self):
        """ Successor halfedge.

        Returns
        -------
        Halfedge
            Next halfedge in face defining halfedge loop.
        """
        return self._next

    @property
    def prev(self):
        """ Predecessor halfedge.

        Returns
        -------
        Halfedge
            Previous halfedge in face defining halfedge loop.
        """
        return self._prev

    @property
    def pair(self):
        """ Opposite halfedge.

        Returns
        -------
        Halfedge
            Halfedge pointing in the opposite direction.
        """
        return self._pair

    @property
    def face(self):
        """ The incident face.

        Returns
        -------
        Face
            The face to left of the halfedge or :py:obj:`None` in case of
            a boundary halfedge.
        """
        return self._face

    def isdeleted(self):
        """ Halfedge status.

        Returns
        -------
        bool
            :py:obj:`True` if deleted.
        """
        return self._deleted

    def isboundary(self):
        """ Boundary halfedge test.

        Returns
        -------
        bool
            :py:obj:`True` if the incident face is not defined.
        """
        return not bool(self._face)


class Face:
    """
    Face base class.

    The preferred way of generating faces of a mesh is by using the
    :meth:`~Mesh.add_face` method:

    .. literalinclude:: ../../examples/mesh_triangle.py
       :lines: 8-
    """

    def __init__(self, he=None):
        """ Face initialization.

        Parameters
        ----------
        he : Halfedge, optional
            An incident halfedge.
        """
        self._halfedge = he                 # incident halfedge
        self._idx = -1                      # face index
        self._deleted = False               # face status

    def __repr__(self):
        """ Object representation.

        Returns
        -------
        str
            String description of a face.
        """
        srep = 'f ['

        for i, v in enumerate(self.vertices()):
            if i == 0: srep += repr(v)
            if i > 0: srep += f'\n   {repr(v)}'

        return srep + ']'

    def __str__(self):
        """ String representation.

        Returns
        -------
        str
            String description of a face.
        """
        return f'f {[v.index for v in self.vertices()]}'

    def __contains__(self, v):
        """ Vertex containment test.

        Parameters
        ----------
        v : Vertex
            Vertex to be tested for incidence with the face.

        Returns
        -------
        bool
            :py:obj:`True` if the given vertex belongs to the face.
        """
        return v in self.vertices()

    @property
    def halfedge(self):
        """ Incident halfedge.

        Returns
        -------
        Halfedge
            A halfedge incident with the given face, :py:obj:`None` for an
            empty face.
        """
        return self._halfedge

    @property
    def index(self):
        """ Face index.

        Returns
        -------
        int
            Current position of the face in the list of all faces. Negative
            values are returned for faces that are not part of a mesh.

        Warning
        -------
        The face index is not a persistent face identifier! Face indices
        change when the face container of a mesh is reorganized.
        """
        return self._idx

    @property
    def valence(self):
        """ Face valence.

        Returns
        -------
        int
            The number of vertices of a face.
        """
        # Deleted/empty faces have valence 0 by definition.
        if not self._halfedge: return 0

        # The standard case of a non-empty face, valence = number of
        # adjacent vertices/edges.
        val = 0
        h = self._halfedge

        while True:
            val += 1
            h = h._next
            if h is self._halfedge: return val

    def halfedges(self):
        """ Halfedge iterator.

        Generator function to traverse the face defining loop of halfedges.

        Yields
        ------
        Halfedge
            Halfedge of the face.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # empty face

        while True:
            yield h
            h = h._next                     # next iterate
            if h is self._halfedge: break   # termination condition

    def halfedges_cw(self):
        """ Halfedge Iterator.

        Clockwise traversal of the outer halfedge loop of a face.

        Yields
        ------
        Halfedge
            Twin halfedge of face halfedge.
        """
        if not self._halfedge: return       # empty face test
        h = self._halfedge._prev            # initialize iteration

        while True:
            yield h._pair
            h = h._prev                     # next iterate
            if h is self._halfedge._prev:   # termination condition
                break

    def vertices(self):
        """ Vertex iterator.

        Generator function to visit all vertices of the face in a
        counterclockwise traversal.

        Yields
        ------
        Vertex
            A vertex of the face.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # empty face test

        while True:
            yield h._origin
            h = h._next                     # next iterate
            if h is self._halfedge: break   # termination condition

    def vertices_cw(self):
        """ Vertex iterator.

        Generator function to visit all vertices of the face in a clockwise
        traversal.

        Yields
        ------
        Vertex
            A vertex of the face.
        """
        if not self._halfedge: return       # empty face test
        h = self._halfedge._prev            # initialize iteration

        while True:
            yield h._origin
            h = h._prev                     # next iterate
            if h is self._halfedge._prev:   # termination condition
                break

    def faces(self, vertex_link=False):
        """ Adjacent face iterator.

        Generator function to visit the faces that share an edge with
        this face. Traversal happens in counterclockwise order.

        Parameters
        ----------
        vertex_link : bool, optional
            Set to :py:obj:`True` to also visit the faces that only share a
            vertex with this face. Those faces are interleaved in the traversal
            of the faces that share an edge.
        """
        h = self._halfedge                  # initialize iteration
        if not h: return                    # empty face

        if vertex_link:
            # Iterate over the incoming halfedges of vertices and yield the
            # adjacent face of such edges.
            h = h._pair._prev
            while True:
                if h._face:
                    yield h._face
                h = h._pair._prev
                if h._pair is self._halfedge:
                    break
                # We have reached a halfedge of the center face. Continue
                # with the incoming edges of the other vertex of the edge.
                if h._pair._face is self:
                    h = h._prev
        else:
            # Traverse all halfedges of the given face, yield the adjacent
            # face of its pair.
            while True:
                if h._pair._face:
                    yield h._pair._face
                h = h._next
                if h is self._halfedge:
                    break

    def isdeleted(self):
        """ Face status.

        Returns
        -------
        bool
            :py:obj:`True` when deleted.

        Warning
        -------
        Deleted faces are removed from the mesh when calling
        :meth:`~Mesh.clean`. This will invalidate previously obtained face
        indices.
        """
        return self._deleted

    def isempty(self):
        """ Empty face test.

        Empty faces typically result from deletion operations. A face is
        empty if its halfedge attribute is not defined.

        Returns
        -------
        bool
            :py:obj:`True` if this face does not have a valid halfedge
            assigned.
        """
        return not bool(self._halfedge)

    def isboundary(self, vertex_condition=False):
        """ Boundary test.

        A face is defined to be a boundary face if one of its edges is a
        boundary edge. An edge is a boundary edge if one of its defining
        halfedges is a boundary halfedge.

        Parameters
        ----------
        vertex_condition : bool, optional
            Set to :py:obj:`True` to replace *edge* with *vertex* in the
            defintion of a boundary face.

        Note
        ----
        Unlike isolated vertices, empty faces are degenerate objects. They
        are not reported as boundary faces!
        """
        if vertex_condition:
            for v in self.vertices():
                if v.isboundary(): return True
        else:
            for h in self.halfedges():
                if h._pair.isboundary(): return True

        return False


class Mesh:
    """ Mesh base class.

    The combinatorics of a mesh can be built iteratively by adding vertices
    and faces, reading from a file, or by converting an indexed mesh to its
    halfedge representation.
    """

    def __init__(self, V=[], F=[]):
        """ Halfedge mesh initialization.

        Parameters
        ----------
        V : list, optional
            Sequence of vertex coordinates.
        F : list, optional
            Sequence of face definitions.

        Raises
        ------
        NonManifoldError
            If trying to initialize from non-manifold data.


        A face definition, i.e., an item of ``F`` is supposed to be
        syntactically equivalent to ``list[int]`` or ``list[(int, int, int)]``.

        If ``F`` is non-empty, ``V`` needs to hold an appropriate number of
        vertex coordinates. If both are not specified an empty mesh is created.

        The item ``V[i]`` is bound to the :py:attr:`point` attribute of the
        i-th mesh vertex. Vertex coordinates have to be copied explicitly if
        this is the desired behavior.
        """
        self._verts = []                    # contiguous list of all vertices
        self._halfs = dict()                # maps pairs (v, w) to halfedges
        self._faces = []                    # contiguous list of all faces

        # Add all vertices to the mesh structure. There is no implicit
        # duplication of vertex coordinates.
        for v in V:
            self.add_vertex(v)

        # Add all faces to the mesh. A vertex that does not get a valid
        # outgoing edge assigned during this process is disconnected from all
        # faces. We refer to such vertices as unused or isolated.
        for f in F:
            try:
                face = [v[0] for v in f]    # in case we are given v/vt/vn
            except TypeError:
                face = [v for v in f]

            # Add the face. Texture and normal information provided in an
            # OBJ file is currently lost in this process.
            self.add_face(face)

    def __repr__(self):
        """ Object representation.

        Returns
        -------
        str
            String description of a mesh.
        """
        srep = str()

        for i in range(len(self._verts)):
            if i > 0: srep += '\n'
            srep += repr(self._verts[i])

        for f in  self.faces():
            srep += f'\n{repr(f)}'

        return srep

    def __str__(self):
        """ String representation.

        Returns
        -------
        str
            String description of a mesh.
        """
        srep = str()

        for i in range(len(self._verts)):
            srep += f'{self._verts[i]}\n'

        for f in  self.faces():
            srep += f'{f}\n'

        num_isolated = 0                    # isolated vertex counter
        num_empty = 0                       # empty face counter

        for v in self.vertices():
            if v.isisolated(): num_isolated += 1

        for f in self.faces():
            if f.isempty(): num_empty += 1

        srep += f'{len(self._verts)} vertices, {num_isolated} isolated\n'
        srep += f'{len(self._faces)} faces, {num_empty} empty\n'
        srep += f'{len(self.boundary())} boundary component(s)'

        return srep

    def add_vertex(self, point):
        """ Create and add new vertex.

        Parameters
        ----------
        point
            Vertex coordinates.

        Returns
        -------
        Vertex
            The newly created :class:`Vertex` object.

        Note
        ----
        The ``point`` argument is assigned to, accessible, and modifiable via
        the :py:attr:`point` attribute of the returned vertex.
        """
        v = Vertex(point)                   # create instance
        v._idx = len(self._verts)           # set vertex index
        self._verts.append(v)               # add to vertex container
        return v                            # return new vertex instance

    def add_face(self, vids):
        """ Create and add new face.

        Parameters
        ----------
        vids : list[int] or list[Vertex]
            A sequence of vertices or vertex indices.

        Raises
        ------
        NonManifoldError
            If topological problems occur.
        IndexError
            If the given indices are out of bounds.

        Returns
        -------
        Face
            The newly created :py:class:`Face` object.

        Note
        ----
        Vertex indices have to refer to existing vertices, i.e., those
        created with :py:meth:`add_vertex`.
        """
        # Number of vertices of the face, same as the number of edges
        # bounding the face.
        n = len(vids)

        # Empty faces are not allowed when using this interface method.
        if n == 0:
            msg = ('add_face(): empty faces may not be added to a mesh ' +
                   'with this method!')
            raise NonManifoldError(msg)

        face = Face()                       # new face object, empty
        face._idx = len(self._faces)        # set hidden face identifier
        edge_loop = []                      # halfedge loop around f

        try:
            # Add/process edges of the given face. Initalize as many vertex,
            # halfedge and face attributes as possible.
            for k in range(n):
                v = vids[k]                 # origin vertex
                w = vids[(k+1)%n]           # target vertex

                # Translate to vertices if the caller used integers
                # instead of vertex objects to define a face.
                if isinstance(v, int): v = self._verts[v]
                if isinstance(w, int): w = self._verts[w]

                # Add the halfedge from v to w. Only h._pair is set if the
                # pair is already mapped. This allows for easy recovery.
                h = self._add_halfedge(v, w)
                edge_loop.append(h)

        except NonManifoldError:
            # Face could not be added! Recovery: remove all previously added
            # halfedges of this face.
            for h in edge_loop:
                del self._halfs[(h._origin, h._target)]

            # Get rid of the face instance and re-raise the exception.
            del face
            raise

        # Proceed with linking mesh items together: fully establish pair
        # relations, set face attribute...
        for h in edge_loop:
            h._face = face
            h._origin._halfedge = h
            if h._pair: h._pair._pair = h

        self._faces.append(face)            # add face
        face._halfedge = edge_loop[0]       # set incident halfedge

        # Take care of next and prev halfedge pointer around the inner
        # edge loop of the face.
        for i in range(n):
            j = (i+1)%n
            edge_loop[i]._next = edge_loop[j]
            edge_loop[j]._prev = edge_loop[i]

        # Add boundary halfedges for newly introduced boundary edges.
        # Also populate the edge set of the mesh.
        for h in edge_loop:
            if not h._pair:
                hbar = self._add_halfedge(h._target, h._origin)
                h._pair = hbar

        # The interior edge loop of a face is already complete. We need to
        # take care of the outer loop. To do this we rely on the correctly
        # set pair pointers and prev/next pointers of the inner loop.
        for h in edge_loop:
            ph = None                       # previous halfedge, if any
            hh = h                          # initialize iteration

            # Rotate the edge h = (v, w) as long as possible clockwise
            # around its origion v until we reach the boundary. There is
            # nothing to do if we circulate back to h itself.
            while True:
                if not hh._pair._face:
                    ph = hh._pair
                    break

                hh = hh._pair._next
                if hh is h: break

            hh = h                          # reset iteration variable

            # If ph was set, the halfedge h is now rotated counterclockwise
            # about its origin v until we reach the same boundary.
            while ph:
                hh = hh._prev._pair

                # This branch should never be taken. No recovery from
                # this problem.
                if hh is h:
                    msg = ('add_face(): vertex #' + str(h._origin._idx) +
                           ' is a non-manifold vertex!')
                    raise NonManifoldError(msg)

                # We reached the boundary again. Link the halfedges.
                if not hh._face:
                    hh._prev = ph
                    ph._next = hh
                    break

        return face

    def del_face(self, face):
        """ Delete face.

        Parameters
        ----------
        face : Face
            The face to be deleted.

        Note
        ----
        The deleted face is not removed from the mesh immediately. Instead its
        :attr:`~Face.deleted` status is set to :obj:`True` its
        :attr:`~Face.halfedge` attribute it set to :py:obj:`None` -- making it
        an empty face. Faces marked for deletion are removed from the mesh
        when calling :py:meth:`clean`.

        Warning
        -------
        Deleting a face of a manifold mesh can result in non-manifold mesh
        topology. No test is performed to prevent this.
        """
        # Mark the face as deleted.
        face._deleted = True

        # Get halfedges bordering the face. Nothing to do for an empty face.
        edge_loop = [h for h in face.halfedges()]

        # Boundary halfedges incident with the deleted face serve no longer
        # serve any propose. They are deleted from the halfedge container.
        for h in edge_loop:
            if not h._pair._face:
                self._del_halfedge(h)
            else:
                h._face = None

        # In addition to being marked as deleted the face also becomes an
        # empty face.
        face._halfedge = None

    def copy(self, V=None):
        """ Mesh copy.

        Duplicates the mesh combinatorics and vertex coordinates. Alternatively
        a new set of vertex coordinates can be specified.

        Parameters
        ----------
        V : array_like, optional
            Vertex coordinates.

        Raises
        ------
        AttributeError
            If the data type used to describe vertex coordinates does not
            provide a ``copy()`` attribute. Does not apply if ``V`` is provided.
        ValueError
            If ``V`` is given but does not hold enough coordinate values.

        Returns
        -------
        Mesh
            Copy of the mesh.

        Note
        ----
        Isolated vertices and empty faces are copied. Remove those mesh
        items by calling :py:meth:`clean`.

        Warning
        -------
        All user defined attributes of the mesh are not copied! You need to
        write custom code to copy those attributes after copying the mesh.
        """
        if V is not None and len(V) != len(self._verts):
            msg = ('copy(): the given number of vertex coordinates ' +
                   'does not match!')
            raise ValueError(msg)

        M = Mesh()
        M._clone_connectivity_from(self, V)
        return M

    def clean(self):
        """ Garbage collection.

        Removes all deleted mesh items as well as unused vertices and
        empty faces.
        """
        # Update vertex container to skips all unused vertices, also update
        # all vertex indices.
        self._verts[:] = [v for v in self._verts
                          if not v.deleted and not v.isisolated()]
        for i, v in enumerate(self._verts): v._idx = i

        # Remove deleted halfedges from the halfedge container.
        keys = [k for k, h in self._halfs.items() if h.deleted]
        for key in keys: del self._halfs[key]

        # Update face container to skip all empty and deleted faces.
        self._faces[:] = [f for f in self._faces
                          if not f.deleted and not f.isempty()]
        for i, f in enumerate(self._faces): f._idx = i

    def clear(self):
        """ Clear all mesh items.
        """
        self._verts.clear()
        self._halfs.clear()
        self._faces.clear()

    def vertex(self, i):
        """ Map integer to vertex.

        Parameters
        ----------
        i : int
            Vertex index.

        Raises
        ------
        IndexError
            If ``i`` cannot be mapped to a vertex.

        Returns
        -------
        Vertex
            Vertex object with given index.

        Note
        ----
        Negative indices as customary used with the :class:`list` data type
        can be used.
        """
        return self._verts[i]

    def vertices(self, skip_deleted=False, skip_isolated=False):
        """ Vertex iterator.

        Generator function for vertex iteration. Vertices are visited in the
        order they were added to the mesh.

        Parameters
        ----------
        skip_deleted : bool
            Set to :py:obj:`True` to skip deleted vertices.
        skip_isolated : bool
            Set to :py:obj:`True` to skip isolated vertices.

        Yields
        ------
        Vertex
            Mesh vertex.
        """
        for v in self._verts:
            skip = False

            # Check if any vertex skipping conditions are met. Set the
            # skip flag accordingly.
            if skip_isolated and not v._halfedge: skip = True
            if skip_deleted and v.deleted: skip = True

            # Yield the vertex if none of the skipping conditions hold.
            if not skip: yield v

    def halfedge(self, v, w):
        """ Map vertex pair to halfedge.

        Parameters
        ----------
        v : Vertex
            A mesh vertex.
        w : Vertex
            A mesh vertex.

        Raises
        ------
        KeyError
            If the given pair cannot be mapped to a halfedge.

        Returns
        -------
        Halfedge
            The halfedge that joins vertices v and w.
        """
        return self._halfs[(v,w)]

    def halfedges(self, skip_deleted=False):
        """ Halfedge iterator.

        Generator function for halfedge iteration.

        Yields
        ------
        Halfedge
            A halfedge of the mesh.
        """
        for h in self._halfs.values():
            if not (skip_deleted and h._deleted):
                yield h

    def edges(self, skip_deleted=False):
        """ Edge iterator.

        Yields
        ------
        Halfedge
            A halfedge of the mesh.
        """
        visited = set()                     # empty set of visited edges

        for h in self._halfs.values():
            if h._pair not in visited:
                visited.add(h)
                if not (skip_deleted and h._deleted):
                    yield h

    def face(self, i):
        """ Map integer to face.

        Parameters
        ----------
        i : int
            Face index.

        Raises
        ------
        KeyError
            If ``i`` cannot be mapped to a face.

        Returns
        -------
        Face
            Face with given index.

        Note
        ----
        Negative indices as customary used with the :class:`list` data type
        can also be used.
        """
        return self._faces[i]

    def faces(self, skip_deleted=False, skip_empty=False):
        """ Face iterator.

        Parameters
        ----------
        skip_deleted : bool
            Set to :py:obj:`True` to skip deleted faces.
        skip_empty : bool
            Set to :py:obj:`True` to skip empty faces.

        Yields
        -----
        Face
            A face of the mesh.
        """
        for f in self._faces:
            skip = False

            # Check if any face skipping conditions are met and set the
            # skip flag accordingly.
            if skip_deleted and f._deleted: skip = True
            if skip_empty and not f._halfedge: skip = True

            # Yield the face if none of the skipping conditions hold.
            if not skip: yield f

    def boundary(self, ccw=True):
        """ Extract boundary components.

        By default the boundary vertices are returned in counterclockwise
        orientation, i.e., positively oriented with respect to the mesh
        orientation.

        Parameters
        ----------
        ccw : bool
            Pass :obj:`False` to reverse the orientation of boundary loops.

        Returns
        -------
        list[list[Vertex]]
            Boundary components.
        """
        all_bnd_comps = []                  # output argument
        visited_edges = set()               # keep track of visited edges

        for h in self.halfedges():
            # Find a boundary halfedge that has not been visited before.
            # The corresponding boundary component has not been traced yet.
            if h.isboundary() and h not in visited_edges:
                bnd_comp = []               # start a new boundary comp.
                hh = h                      # starting with halfedge h

                # Sanity check. Should be removed later or turned off by
                # running Python with the '-O' command line option.
                assert h._pair not in visited_edges

                # The current halfedge h belongs to an undiscovered boundary
                # component. We follow the .prev/.next pointers until we
                # reach h again.
                while True:
                    bnd_comp.append(hh.target)
                    visited_edges.add(hh)

                    if ccw: hh = hh.prev    # boundary in positive orientation
                    else:   hh = hh.next    # boundary in negative orientation

                    if hh is h:             # termination condition
                        break
                    else:
                        # There is topological problem if hh or its pair
                        # have been visited before!
                        assert hh not in visited_edges
                        assert hh._pair not in visited_edges

                all_bnd_comps.append(bnd_comp)

        return all_bnd_comps

    def num_vertices(self):
        """ Number of vertices.

        Returns
        -------
        int
            The number of mesh vertices.

        Note
        ----
        The vertex count includes all isolated vertices and vertices that
        are marked for deletion.
        """
        return len(self._verts)

    def num_faces(self):
        """ Number of faces.

        Returns
        -------
        int
            The number of mesh faces.

        Note
        ----
        The face count includes all empty faces and face that are marked
        for deletion.
        """
        return len(self._faces)

    def vertex_list(self):
        """ Vertex coordinates.

        Generates a contiguous list of all vertex :attr:`~Vertex.point`
        attributes.

        Returns
        -------
        V : list
            List of all vertex coordinates.

        Note
        ----
        The data type of ``V[i]`` is the same that was used when adding the
        vertex.
        """
        return [v.point for v in self._verts]

    def face_list(self):
        """ Face definitions.

        Each face definition is a list of integers (possibly of different
        length if the faces are not all of the same valence).

        Returns
        -------
        F : list[list[int]]
            The list of face definitions.
        """
        return [[v._idx for v in f.vertices()] for f in self.faces()]

    def indexed_mesh(self):
        """ Indexed mesh representation.

        Returns
        -------
        V : list
            List of all vertex coordinates.
        F : list[list[int]]
            List of all face definitions.
        """
        return self.vertex_list(), self.face_list()

    @classmethod
    def read(cls, filename):
        """ Read mesh from OBJ file.

        Parameters
        ----------
        filename : str
            Name of an OBJ file.

        Raises
        ------
        RuntimeError
            If there were problems parsing the given OBJ file.
        NonManifoldError
            If conversion to the halfedge based mesh representation failed.

        Returns
        -------
        Mesh
            Halfedge based mesh representation.
        """
        # At some point the additional arguments 'vt' and 'vn' should also be
        # allowed to support reading of texture coordinates and normals!
        V, F = obj.read(filename, 'v', 'f')
        return cls(V, F)

    def write(self, filename):
        """ Write mesh to OBJ file.

        Parameters
        ----------
        filename : str
            Name of target OBJ file.
        """
        obj.write(filename, v=self.vertex_list(), f=self.face_list())

    def _clone_connectivity_from(self, other, V=None):
        """ Clone mesh connnectivity.

        Parameters
        ----------
        other : Mesh
            Template mesh connectivity.
        V : array_like, optional
            Vertex coordinates.

        Raises
        ------
        AttributeError
            If vertices of the template mesh do not provide ``copy()``.
        ValueError
            If vertex coordinates are provided but their number is not equal
            to the number of vertices of ``other``.
        """
        self._verts.clear()                 # contiguous list of all vertices
        self._halfs.clear()                 # maps pairs (v, w) to halfedges
        self._faces.clear()                 # contiguous list of all faces

        # Build maps that assigns to each vertex/halfedge of the original mesh
        # its corresponding copy in the new mesh.
        vmap = dict()
        hmap = dict()
        fmap = dict()

        # 1st pass over vertices: duplicate vertices. The halfedge pointer is
        # set in a second pass after halfedges have been duplicated.
        if V is not None:
            # If alternative coordinates are given their number needs to
            # match the number of vertices of other.
            if len(V) != len(other._verts):
                msg = ('_clone_connectivity_from(): the number of given ' +
                       'vertex coordinates does not match!')
                raise ValueError(msg)

            for v, w in zip(other._verts, V):
                v_new = self.add_vertex(w)
                vmap[v] = v_new
        else:
            # Copy vertex coordinates using values from other. The .copy()
            # statement may raise an AttributeError.
            for v in other._verts:
                v_new = self.add_vertex(v.point.copy())
                vmap[v] = v_new

        # 1st pass over halfedges. We need to have vertices available to
        # generate halfedges.
        for (v, w), h in other._halfs.items():
            v_new = vmap[v]
            w_new = vmap[w]
            h_new = Halfedge(v_new, w_new)
            hmap[h] = h_new
            self._halfs[(v_new, w_new)] = h_new

        # 2nd pass over vertices: can set halfedge attribute now.
        for v in other._verts:
            v_new = vmap[v]
            v_new._halfedge = hmap[v._halfedge] if v._halfedge else None

        # Copy the faces. Only one pass needed, requires valid halfedge map.
        for f in other._faces:
            f_new = Face()
            f_new._halfedge = hmap[f._halfedge] if f._halfedge else None
            fmap[f] = f_new
            self._faces.append(f_new)

        # 2nd pass over halfedges. Can set all remaining attributes since
        # faces and the halfedge map are available.
        for h in other._halfs.values():
            h_new = hmap[h]
            h_new._next = hmap[h._next]
            h_new._prev = hmap[h._prev]
            h_new._pair = hmap[h._pair]
            h_new._face = fmap[h._face] if h._face else None

    def _add_halfedge(self, v, w):
        """ Add new halfedge.

        Generates a new halfedge and sets its :py:attr:`origin` and
        :py:attr:`target` attributes. The :py:attr:`pair` attribute of the
        generated halfedge is set if the opposite halfedge is already mapped.

        Parameters
        ----------
        v : Vertex
            Origin vertex of the halfedge.
        w : Vertex
            Target vertex of the halfedge

        Raises
        ------
        NonManifoldError
            If there are topological issues when adding the halfedge.

        Returns
        -------
        Halfedge
            Halfedge pointing from ``v`` to ``w``.

        Warning
        -------
        This is a low-level interface function that should **not** be called
        directly from application code.
        """
        # Topologically degenerate non-manifold edge?
        if v is w:
            msg = ('_add_halfedge(): topologically degenerate edge ' +
                   str((v._idx, w._idx)) + ' found, identical vertices!')
            raise NonManifoldError(msg)

        # If the edge (v, w) is already mapped we have a problem unless
        # it is mapped as a boundary halfedge.
        if (v, w) in self._halfs:
            h = self._halfs[(v, w)]

            # If the face of h is valid, the caller tries to create a
            # non-manifold edge!
            if h._face:
                msg = ('_add_halfedge(): edge ' + str((v._idx, w._idx)) +
                       ' is non-manifold!')
                raise NonManifoldError(msg)
        else:
            # Generate a new halfedge and add it to the existing halfedges
            h = Halfedge(v, w)
            self._halfs[(v, w)] = h

            # Check if the pair is mapped and set the pair pointer
            if (w, v) in self._halfs:
                h._pair = self._halfs[(w, v)]

        return h

    def _del_halfedge(self, halfedge):
        """ Delete halfedge and merge incident faces.

        Removes an edge and merges its incident faces. This may create
        'dangling edges', i.e., halfedges with ``h.pair == h.next``.

        Parameters
        ----------
        halfedge : Halfedge
            The halfedge that spans the edge to be deleted.

        Returns
        -------
        bool
            :py:obj:`True` if ``halfedge`` was successfully deleted.

        Raises
        ------
        KeyError
            If there was a problem removing the halfedge from the
            halfedge container.
        NonManifoldError
            If halfedge deletion leads to invalid combinatorics.

        Warning
        -------
        This is a low-level interface function that should **not** be called
        directly from application code.
        """
        # If halfedge is a boundary halfedge we replace it with halfedge.pair
        # if this is not boundary.
        if halfedge._pair._face and not halfedge._face:
            halfedge = halfedge._pair

        # If the face of the pair is valid it may not point to halfedge.pair
        # or halfedge as its incident halfedge.
        if halfedge._pair._face:
            h = halfedge._pair._face._halfedge
            while h is halfedge or h is halfedge._pair:
                h = h._next
                if h is halfedge._pair._face._halfedge: break

            # Could not find an alternative incident halfedge. No recovery
            # from this problem!
            if h is halfedge or h is halfedge.pair:
                msg = ('_del_halfedge(): halfedge connectivity could not ' +
                       ' be sanitized before edge deletion!')
                raise NonManifoldError(msg)
            else:
                halfedge._pair._face._halfedge = h

        # Make sure that the deleted halfedge is not stored as the outgoing
        # halfedge of its origin.
        v = halfedge._origin
        h = v._halfedge
        while h is halfedge:
            h = h._pair._next
            if h is v._halfedge: break

        # If no alternative outgoing halfedge could be found, vertex v is a
        # dangling vertex and becomes unused after the halfedge is removed.
        v._halfedge = h
        if v._halfedge is halfedge: v._halfedge = None

        # Perform the same steps for halfedge.pair since this will also
        # get removed.
        w = halfedge._pair._origin
        h = w._halfedge
        while h is halfedge._pair:
            h = h._pair._next
            if h is w._halfedge: break

        w._halfedge = h
        if w._halfedge is halfedge._pair: w._halfedge = None

        # Now the two faces indicent with halfedge get merged. If they are
        # already equal the deleted halfedge is a dangling edge.
        if not halfedge._pair._face is halfedge._face:
            halfedge._face._halfedge = None
            f = halfedge._pair._face
            h = halfedge
            while True:
                h._face = f
                h = h._next
                if h is halfedge: break

        # The halfedge gets disconnected from all other mesh items.
        halfedge._prev._next = halfedge._pair._next
        halfedge._pair._next._prev = halfedge._prev
        halfedge._next._prev = halfedge._pair._prev
        halfedge._pair._prev._next = halfedge._next

        # Finally remove halfedge and its twin from the list of halfedges.
        del self._halfs[(halfedge._origin, halfedge._target)]
        del self._halfs[(halfedge._target, halfedge._origin)]


class NonManifoldError(Exception):
    """ Exception base class.

    Raised if an operation results in a topological configuration that
    violates the manifold condition.
    """
