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

""" Wavefront OBJ input/output.

Basic read and write operations for OBJ files. Supports meshes and a subset
of **cstype** statements. Complete specifications can be found in the
`Advanced Visualizer Manual`.
"""

import io
import warnings

import numpy as np


class CSType:
    """ Wrapper class for **cstype** statements.

    Represents a subset of the freeform curve and surface statements found in
    the Alias/Wavefront OBJ specification, see
    `here <https://en.wikipedia.org/wiki/Wavefront_.obj_file>`_ or
    `Appendix B <http://fegemo.github.io/cefet-cg/attachments/obj-spec.pdf>`_
    of the `Advanced Visualizer Manual` for details. This class serves as a
    link between Wavefront OBJ files and application code. Supports import and
    export of curves and surfaces in Bézier and B-spline representation.


    The preferred way of initializing :py:class:`CSType` objects is by
    using the :py:meth:`read` or the :py:meth:`bezier` and :py:meth:`bspline`
    member functions. The script

    .. literalinclude:: ../../examples/cstype_io.py
       :lines: 8-

    results in the following output:

    .. code-block:: none

       v 0.0 0.0 0.0
       v 1.0 0.0 1.0
       v 1.0 1.0 2.0
       v 0.0 1.0 3.0
       v 0.0 0.0 4.0
       cstype bspline
       deg 3
       curv 0.0 2.0 -5 -4 -3 -2 -1
       parm u 0.0 0.0 0.0 0.0 1.0 2.0 2.0 2.0 2.0
       end
    """

    def __init__(self, cstype, *args):
        """ Constructor.

        Creates an empty freeform curve/surface of a given type.

        Parameters
        ----------
        cstype : string
            A string description of the curve/surface type. Has to be
            ``'bezier'`` or ``'bspline'``.
        *args
            Variable length argument list. Pass ``'rational'`` or ``'rat'``
            to indicates that the last entry of control point coordinates
            serves as a weight.

        Raises
        ------
        ValueError
            If invalid values for ``cstype`` are given.

        Note
        ----
        Control points of rational curves and surface are of the form
        :math:`(x, y, z, w)` where :math:`(x, y, z)` are Euclidian coordinates
        and :math:`w` acts as a weight. The Wavefront OBJ specification
        does not prohibit the use of negative or zero weights.
        """
        # Check provided input arguments and raise ValueError if there are
        # invalid values.
        if not cstype in {'bezier', 'bspline'}:
            msg = ("CSType init(): cstype argument needs to be 'bezier' " +
                   "or 'bspline'! " + cstype + " was given.")
            raise ValueError(msg)

        self._type = cstype             # 'bezier' or 'bspline'
        self._deg = None                # (deg_u, deg_v) tuple

        # Should the last control point coordinate be treated as a weight?
        self._rat = 'rational' in args or 'rat' in args

        # When initialized by the read() function the indices correspond
        # to absolute vertex indices of vertices read from the same file.
        self._vid = None

        # Initially holds a list of vertex coordinates when populated using
        # read(), then reshaped to an array of the correct dimensions using
        # the function _generate_cparray().
        self._cps = None

        self._rangeu = None             # (u_start, u_end) for visualization
        self._rangev = None             # (v_start, v_end) for visualization
        self._parmu = None              # (a_0, ..., a_k) knots in u direction
        self._parmv = None              # (b_0, ..., b_l) knots in v direction

    def __str__(self):
        """ Object output with :py:func:`print`.

        Returns
        -------
        str : str
            String representation of the object.
        """
        file = io.StringIO()
        self.write(file)
        str = file.getvalue()
        file.close()
        return str

    @staticmethod
    def bezier(b, *args):
        """ Initialize Bézier curve/surface.

        Initializes a Bézier curve/surface from its control point array.

        Parameters
        ----------
        b : ~numpy.ndarray, shape (n+1, d)
            Control points of a Bézier curve/surface. For a surface
            shape should be (m+1, n+1, d), see below for more details.
        *args
            Variable length argument list. Pass ``'func'`` to disambiguate the
            case of curves and functional surfaces. Pass ``'rational'`` or
            ``'rat'`` to indicate that the last of the d coordinate entries of
            each control point is a weight.

        Returns
        -------
        CSType
            Corresponding Bézier curve/surface representation.


        **Curves:** Let :math:`n \geq 0`. Control points :math:`\mathbf{b}_0,
        \dots, \mathbf{b}_{n} \in \mathbb{R}^d` define a Bézier curve

        .. math::

            \mathbf{b}(u) = \sum_{i=0}^{n} \mathbf{b}_i B_i^n(u)

        of degree :math:`n` over the interval :math:`[0, 1]`. The control
        points can be passed by packing them into an array ``b`` of shape
        (n+1, d).


        **Surfaces:** Let :math:`m \geq 0` and :math:`n \geq 0`. A tensor
        product Bézier surface of degree :math:`(m, n)` is defined as

        .. math::

            \mathbf{b}(u,v) = \sum_{i=0}^{m} \sum_{j=0}^{n} \mathbf{b}_{ij}
            B_i^m(u) B_j^n(v).

        Control points should be passed as an array ``b`` of shape
        (m+1, n+1, d).

        Note
        ----
        If we are given weights as last component of control points, a
        corresponding rational curve is defined according to

        .. math::

            \mathbf{b}(u) = \\frac{\sum_{i=0}^{n} w_i\mathbf{a}_i B_i^n(u)}
                            {\sum_{i=0}^{n} w_i B_i^n(u)}, \qquad
                            \mathbf{b}_i = (\mathbf{a}_i, w_i)

        and analogously for surfaces.
        """
        cs = CSType('bezier', *args)

        if b.ndim == 1:
            cs._deg = (len(b)-1,)
            cs._vid = [i for i in range(len(b))]
            cs._cps = np.asarray(b)
            cs._rangeu = (0.0, 1.0)
            cs._parmu = (0.0, 1.0)
        elif b.ndim == 3 or (b.ndim == 2 and 'func' in args):
            cs._deg = (b.shape[0]-1, b.shape[1]-1)
            cs._vid = [i for i in range(b.shape[0]*b.shape[1])]
            cs._cps = np.asarray(b)
            cs._rangeu = (0.0, 1.0)
            cs._rangev = (0.0, 1.0)
            cs._parmu = (0.0, 1.0)
            cs._parmv = (0.0, 1.0)
        elif b.ndim == 2:
            cs._deg = (len(b)-1,)
            cs._vid = [i for i in range(len(b))]
            cs._cps = np.asarray(b)
            cs._rangeu = (0.0, 1.0)
            cs._parmu = (0.0, 1.0)
        else:
            msg = ("bezier(): cannot handle control point array of " +
                   "shape " + str(b.shape))
            raise ValueError(msg)

        return cs

    @staticmethod
    def bspline(t, c, k, *args):
        """ Initialize B-spline curve/surface.

        Initializes a B-spline curve/surface using a (t, c, k) triple
        as in :py:class:`scipy.interpolate.BSpline`.

        Parameters
        ----------
        t : ~numpy.ndarray, shape (2k+n+2,)
            Knot vector of a curve. For a surface a pair of knot vectors
            with shapes (2k+m+2,) and (2l+n+2,) have to be specified.
        c : ~numpy.ndarray, shape (k+n+1, d)
            Control point array. For a surface an array of shape
            (k+m+1, l+n+1, d) is required.
        k : int
            The degree of the curve. For a surface a pair (k, l) of integers
            is required.
        *args
            Variable length argument list. Pass ``'rational'`` to indicate
            that the last of the d coordinate entries of each control point
            is a weight.

        Raises
        ------
        ValueError
            If the values and size given for degree, knots, and control
            points are inconsistent.

        Returns
        -------
        CSType
            Corresponding B-spline curve/surface representation.


        **Curves:** Let :math:`n \geq 0`. Control points :math:`\mathbf{c}_0,
        \dots, \mathbf{c}_{k+n} \in \mathbb{R}^d` and knots :math:`t_0, \dots,
        t_{2k+n+1} \in \mathbb{R}` such that :math:`t_i \leq t_{i+1}` define
        a B-spline curve

        .. math::

            \mathbf{c}(t) = \sum_{i=0}^{n+k} \mathbf{c}_i N_i^k(t)

        of degree :math:`k` over the interval :math:`[t_k, t_{k+n+1})` if
        :math:`t_i < t_{i+k+1}` for :math:`i \in \{0, \dots, n+k\}`. Those
        values can be passed as arguments by packing the control points into
        an array ``c`` of shape (k+n+2, d) and knots as an array ``t`` of
        shape (2k+n+2,) or as ``list[float]``.

        .. literalinclude:: ../../examples/cstype_io.py
           :lines: 8-21


        The curve :math:`\mathbf{c}` is polynomial over each non empty interval
        :math:`[t_j, t_{j+1})` for :math:`j = k, \dots, k+n`. The integer
        :math:`n` determines the number of polynomial segments of
        :math:`\mathbf{c}`.


        **Surfaces:** Let :math:`m \geq 0` and :math:`n \geq 0`. A tensor
        product B-spline surface of degree
        :math:`(k, l)` over the knot sequences :math:`u_0, \dots, u_{2k+n+1}`
        and :math:`v_0, \dots, v_{2l+m+1}` is defined as

        .. math::

            \mathbf{s}(u,v) = \sum_{i=0}^{m+k} \sum_{j=0}^{n+l} \mathbf{c}_{ij}
            N_i^k(u) N_j^l(v).

        The control points can be stored in an array of shape (k+m+1, l+n+1, d).
        Knot vectors can be passed as a pair of 1-dimensional arrays or a
        pair of ``list[float]``.
        """
        # Create empty CSType object. Attributes are filled using tck.
        cs = CSType('bspline', *args)

        # A curve is defined if k is a single integer. If the condition
        # len(t) = len(c) + k + 1 fails an Exception is triggered.
        if isinstance(k, int):
            if k < 0 or len(t) != len(c) + k + 1:
                msg = ('bspline(): inconsistent degree and shapes of ' +
                       'knot vector and control point array!')
                raise ValueError(msg)

            cs._deg = (k,)
            cs._vid = [i for i in range(len(c))]
            cs._cps = np.asarray(c)
            cs._rangeu = (t[k], t[-k-1])
            cs._parmu = tuple(t)

        # Surface definition. Degree and shape of knots and control points
        # need to be consistent in both dimensions.
        elif len(k) == 2:
            if (k[0] < 0 or len(t[0]) != c.shape[0] + k[0] + 1
                    or k[1] < 0 or len(t[1]) != c.shape[1] + k[1] + 1):
                msg = ('bspline(): inconsistent degree and shapes of ' +
                       'knot vectors and control point array!')
                raise ValueError(msg)

            cs._deg = (k[0], k[1])
            cs._vid = [i for i in range(np.shape(c)[0]*np.shape(c)[1])]
            cs._cps = np.asarray(c)
            cs._rangeu = (t[0][k[0]], t[0][-k[0]-1])
            cs._rangev = (t[1][k[1]], t[1][-k[1]-1])
            cs._parmu = tuple([u for u in t[0]])
            cs._parmv = tuple([v for v in t[1]])

        # Things don't match up...
        else:
            msg = ("bspline(): degree 'k' needs to be an integer " +
                   "value or a pair of integers!")
            raise ValueError(msg)

        # Return the generated curve/surface representation.
        return cs

    @property
    def knots(self):
        """ Get knot vector(s).

        Returns knot vectors in u and v direction for surfaces or a single knot
        vector for curves.

        Returns
        -------
        u : tuple[float]
            Knots in u-direction.
        v : tuple[float]
            Knots in v-direction. Not present for curves.
        """
        if len(self._deg) == 2:
            return self._parmu, self._parmv
        else:
            return self._parmu

    @property
    def cparray(self):
        """ Get control point array.

        Returns
        -------
        c : ~numpy.ndarray
            Control point array.
        """
        return self._cps

    @property
    def degree(self):
        """ Get curve/surface degree.

        Returns
        -------
        k : int
            Degree in u-direction.
        l : int
            Degree in v-direction. Not present for curves.
        """
        if len(self._deg) == 2:
            return self._deg[0], self._deg[1]
        else:
            return self._deg[0]

    @property
    def range(self):
        """ Get basic curve/surface interval.

        Returns
        -------
        u : tuple[float]
            Domain in u-direction.
        v : tuple[float]
            Domain in v-direction. Not present for curves.
        """
        if len(self._deg) == 2:
            return self._rangeu, self._rangev
        else:
            return self._rangeu

    def write(self, file):
        """ Export to Wavefront OBJ file.

        Parameters
        ----------
        file : str or file-like object
            Writes the objects OBJ representation to the given file.
        """
        # Open a new file or overwrite an existing file of the given name.
        # If a file object is given we use it directly.
        if isinstance(file, str):
            out = open(file, 'w')
        else:
            out = file

        # Write all vertex coordinates as a block of 'v' statements. We use
        # relative indices to refer to those vertices later.
        if self._cps.ndim == 1:
            ncps = self._cps.shape[0]
            for c in self._cps:
                out.write('v ' + str(c) + '\n')
        elif self._cps.ndim == 2 and len(self._deg) == 2:
            ncps = self._cps.shape[0]*self._cps.shape[1]
            for j in range(self._cps.shape[1]):
                for i in range(self._cps.shape[0]):
                    out.write('v ')
                    out.write(str(self._cps[i,j]))
                    out.write('\n')
        elif self._cps.ndim == 2:
            ncps = self._cps.shape[0]
            for c in self._cps:
                out.write('v ')
                for x in c:
                    out.write(str(x) + ' ')
                out.write('\n')
        elif self._cps.ndim == 3:
            ncps = self._cps.shape[0]*self._cps.shape[1]
            for j in range(self._cps.shape[1]):
                for i in range(self._cps.shape[0]):
                    out.write('v ')
                    for x in self._cps[i,j]:
                        out.write(str(x) + ' ')
                    out.write('\n')
        else:
            msg = "CSType.write(): cannot interpret control point array!"
            raise RuntimeError(msg)

        # Write the cstype header.
        out.write('cstype ')
        if self._rat:
            out.write('rat ')
        out.write(self._type + '\n')

        # Write the deg part of the cstype definition.
        out.write('deg ')
        out.write(str(self._deg[0]))
        if len(self._deg) == 2:
            out.write(' ' + str(self._deg[1]))
        out.write('\n')

        # Write the parameter range of the curve/surface in each parameter
        # direction.
        if len(self._deg) == 2:
            out.write('surf ')
            out.write(str(self._rangeu[0]) + ' ' + str(self._rangeu[1]) + ' ')
            out.write(str(self._rangev[0]) + ' ' + str(self._rangev[1]) + ' ')
        else:
            out.write('curv ')
            out.write(str(self._rangeu[0]) + ' ' + str(self._rangeu[1]) + ' ')

        # On the same line all control point indices are listed. We use
        # relative, i.e., negative indices instead of global indices.
        for vid in self._vid:
            out.write(str(vid-ncps) + ' ')
        out.write('\n')

        # Write knots in u-direction. Has to be defined always!
        out.write('parm u ')
        for u in self._parmu:
            out.write(str(u) + ' ')
        out.write('\n')

        # For a surface also write the knots in v-direction.
        if self._parmv and len(self._parmv):
            out.write('parm v ')
            for v in self._parmv:
                out.write(str(v) + ' ')
            out.write('\n')

        # Terminate cstype statement with end
        out.write('end')

        # Close the file if we were the ones to open it.
        if isinstance(file, str): out.close()

    def issurface(self):
        """ Curve/surface check.

        Returns
        -------
        bool
            :py:obj:`True` if the object describes a surface.
        """
        return len(self._deg) == 2

    def isrational(self):
        """ Check for weights.

        Returns
        -------
        bool
            :py:obj:`True` if the objects describes a rational curve/surface.
        """
        return self._rat

    def _generate_cparray(self):
        """ Generate control point array.

        Reshapes a sequence of control points as read from an OBJ file
        into an array. Inverse to :py:meth:`_flatten_cparray`.

        Note
        ----
        This function should only be called once to reshape the control
        point list read from an OBJ file into an array. Do not call directly
        from application code!
        """
        k = self._deg                       # curve or surface degree

        # The surface case, control point array C has 3 axis. Is there a
        # problem with functional surfaces?
        if len(k) == 2:
            if self.type == 'bspline':
                # Control point indices in u-diretion: 0, 1, ..., n[0]
                # and 0, 1, ..., n[1] in v-direction
                n = (len(self._parmu)-k[0]-2, len(self._parmv)-k[1]-2)
            elif self.type == 'bezier':
                # For a Bezier curve/surface control points are numbered
                # 0, 1, ..., k[0] in u-direction, etc.
                n = (k[0], k[1])

            # Order of control polygon vertices for deg (3, 2) surface:
            # b00 b01 b02   0 4 8
            # b10 b11 b12 = 1 5 9
            # b20 b21 b22   2 6 10
            # b30 b31 b32   3 7 11
            if self._cps.ndim == 2:
                c = np.reshape(self._cps, (n[1]+1, n[0]+1))
                self._cps = np.tranpose(c)
            else:
                d = self._cps.shape[-1]
                c = np.reshape(self._cps, (n[1]+1, n[0]+1, d))
                self._cps = np.transpose(c, (1,0,2))

            self._vid = [i for i in range((n[0]+1)*(n[1]+1))]
        else:
            self._vid = [i for i in range(len(self._cps))]

    def _flatten_cparray(self):
        """ Flatten the control point array of surface.

        Has no effect on the shape of the control point array when called
        for a curve. This is the inverse of :py:meth:`_generate_cparray`.

        Returns
        -------
        V : ~numpy.ndarray
            Linear sequence of control points. Corresponds to OBJ specification
            of flat arrays when used as surface control points.
        """
        if len(self._deg) == 2:
            if self._cps.ndim == 2:
                V = np.transpose(self._cps)
                V = np.ravel(V)
            else:
                V = np.transpose(self._cps, (1,0,2))
                V = np.ravel(V)
                V = np.reshape(V, (-1, self._cps.shape[-1]))
        else:
            V = np.array(self._cps)

        return V


def read(filename, *args):
    """ Parse OBJ file.

    Read contents of an OBJ file and return object definitions like vertices,
    faces, texture coordinates, normals, and curve/surface statements.

    Parameters
    ----------
    filename : str
        Name of an OBJ file.
    *args
        Variable length argument list. Defines the statements to be read and
        the order in which they are returned. See below for details.

    Raises
    ------
    OSError
        If the file could not be opened.
    RuntimeError
        If there were problems parsing the given OBJ file.

    Returns
    -------
    V : list[ndarray]
        List of vertex definitions. Requires ``'v'`` as argument.
    F : list
        List of face definitions. Requires ``'f'`` as argument.
    VT : list[ndarray]
        List of texture coordinates. Requires ``'vt'`` as argument.
    VN : list[ndarray]
        List of vertex normals. Requires ``'vn'`` as argument.
    CS : list[CSType]
        A list of objects initialized from **cstype** statements. Requires
        ``'cstype'`` as argument.


    The following script reads vertex coordinates and face definitions from
    an OBJ file. The extracted data is returned in the same order as specified:

    .. literalinclude:: ../../examples/dragon_read.py
       :lines: 9-11

    When reading texture and/or normal data a face definition is of
    type ``list[(int, int, int)]`` instead of ``list[int]``. The first component of
    each triple refers to the vertex index, the second to the texture coordinate
    index and the last to the normal index. Requesting data that is not present
    in a file will result in :py:obj:`None` entries. Face definitions of this
    kind can easily be split into three separate lists if preferred:

    .. code-block:: python

        # unzip: split F into three separate liste
        FI = [[v[0] for v in f] for f in F]
        FT = [[v[1] for v in f] for f in F]
        FN = [[v[2] for v in f] for f in F]

        # inverse operation: zip three separate lists
        F = [[v for v in zip(f[0], f[1], f[2])] for f in zip(FI, FT, FN)]


    All vertex/texture/normal indices used in the definition of faces or when
    specifying control points of curves/surfaces refer to the returned list of
    vertex/texture/normal coordinates. Indexing is 0-based.

    Vertex coordinates are either 3 or 4-dimensional. Based on the context a
    triple can refer to :math:`(x, y, z)` coordinates in 3-space or extended
    coordinates :math:`(u, v, w)` in the plane -- :math:`w` acts as a weight in
    this case. A quadrupel :math:`(x, y, z, w)` refers to extended coordinates
    in 3-space. The Wavefront OBJ format does not prohibit the use of negative
    or even zero weights.

    Texture coordinates can be 1, 2 or even 3-dimensional. In the 3-dimensional
    case the last coordinates is not a weight but a depth value for volumetric
    textures -- its default is 0.0 as opposed to 1.0 for weights.
    """

    def split(vdef):
        """ Helper function to parse vertex definitions.

        Parameters
        ----------
        vdef : str
            A v/vt/vn string representing a vertex definition as encountered
            when reading 'f' statements. Relative indices, i.e., negative
            integers are allowed.

        Raises
        ------
        ValueError
            If the string could not be parsed.

        Returns
        -------
        v : int
            Absolute index into vertex list.
        vt : int
            Absolute index into texture vertex list. Can be :py:obj:`None` if
            not part of the input string.
        vn : int
            Absolute index into vertex normal list. Can be :py:obj:`None` if
            not part of the input string.
        """
        # Default values in case the given string does not provide all values.
        vid, tid, nid = None, None, None

        if '//' in vdef:
            # A v//vn statement if split by // into exactly two parts.
            iuvn = vdef.split('//')
            if len(iuvn) == 2:
                vid = int(iuvn[0])
                nid = int(iuvn[1])
            else:
                msg = 'split(): invalid v//vn definition: ' + vdef
                raise ValueError(msg)
        elif '/' in vdef:
            # A v/vt or v/vt/vn statement depending on how many parts
            # it gets split into by the / separator.
            iuvn = vdef.split('/')
            if len(iuvn) == 2:
                vid = int(iuvn[0])
                tid = int(iuvn[1])
            elif len(iuvn) == 3:
                vid = int(iuvn[0])
                tid = int(iuvn[1])
                nid = int(iuvn[2])
            else:
                msg = 'split(): invalid v/vt/vn or v/vt definition: ' + vdef
                raise ValueError(msg)
        else:
            # Base case, only v given. This will raise ValueError if vdef
            # cannot be converted to an integer value.
            vid = int(vdef)

        # Produce absolute indices. Adjust variable offset and handle relative
        # (i.e., negative) identifiers. To this end we access the variables V,
        # VT and VN of the enclosing scope.
        if vid < 0: vid = len(V)+vid
        else: vid = vid-1

        # The variables read_vt and read_vn are set in the enclosing scope and
        # define local behavior. If the caller does not want textures or normal
        # related data the corresponding values are set to None even if they
        # are present in the file.
        if tid is not None and read_vt:
            if tid < 0: tid = len(VT)+tid
            else: tid = tid-1
        else:
            tid = None

        if nid is not None and read_vn:
            if nid < 0: nid = len(VN)+nid
            else: nid = nid-1
        else:
            nid = None

        return vid, tid, nid

    # Try to open the given file in read mode. Raises OSError on failure.
    file = open(filename, 'r')

    # Vertex coordinates are either 3 or 4 dimensional (x, y, z [, w]). All
    # 'curv', 'surf', 'p', 'l', and 'f' statements always refer to this list.
    V = []
    F = []                              # face definitions
    VT = []                             # texture coordinates (u [, v, w])
    VN = []                             # normals, always (x, y, z)
    CS = []                             # curve/surface definitions

    # Only read texture coordinates and normals if requested by the caller.
    # This modifies the behavior of the split() helper method.
    read_vt = 'vt' in args
    read_vn = 'vn' in args

    # Current (active) curve/surface definition. It stays active until an
    # 'end' statement is encountered or an unsupported token is read.
    current_cst = None
    line_number = 0                     # used for error reporting

    for line in file:
        # Split current line at whitespace characters, results in a list of
        # strings that we refer to as tokens.
        tokens = line.split()
        line_number += 1

        # There may be empty lines, skip them.
        if not len(tokens): continue

        # Vertex definition: vertex coordinates can have 3 or 4 coordinate
        # values, additional dimensions trigger an exception.
        if tokens[0].strip() == 'v':
            if len(tokens) == 5:
                x = float(tokens[1].strip())
                y = float(tokens[2].strip())
                z = float(tokens[3].strip())
                w = float(tokens[4].strip())
                V.append(np.asarray([x, y ,z, w], dtype=float))
            elif len(tokens) == 4:
                x = float(tokens[1].strip())
                y = float(tokens[2].strip())
                z = float(tokens[3].strip())
                V.append(np.asarray([x, y ,z], dtype=float))
            else:
                msg = ('read(): ' + str(line_number) + ': invalid vertex ' +
                       'definition: ' + line)
                raise RuntimeError(msg)

        # Texture vertex: can have 1 up to 3 coordinate values. Additional
        # trailing dimensions trigger an exception.
        elif tokens[0].strip() == 'vt' and read_vt:
            if len(tokens) == 4:
                u = float(tokens[1].strip())
                v = float(tokens[2].strip())
                w = float(tokens[3].strip())
                VT.append(np.asarray([u, v, w], dtype=float))
            elif len(tokens) == 3:
                u = float(tokens[1].strip())
                v = float(tokens[2].strip())
                VT.append(np.asarray([u, v], dtype=float))
            elif len(tokens) == 2:
                u = float(tokens[1].strip())
                VT.append(np.asarray([u], dtype=float))
            else:
                msg = ('read(): ' + str(line_number) + ': invalid texture ' +
                       'vertex definition: ' + line)
                raise RuntimeError(msg)

        # Vertex normal defintion, has to be three-dimensional. Vectors
        # are not required to be normalized!
        elif tokens[0].strip() == 'vn' and read_vn:
            if len(tokens) == 4:
                x = float(tokens[1].strip())
                y = float(tokens[2].strip())
                z = float(tokens[3].strip())
                VN.append(np.asarray([x, y, z], dtype=float))
            else:
                msg = ('read(): ' + str(line_number) + ': invalid vertex ' +
                       'normal definition: ' + line)
                raise RuntimeError(msg)

        # Parameter space vertex definition (u [, v, w]). Used with curv2,
        # not supported, yet.
        elif tokens[0].strip() == 'vp':
            print('read(): ' + str(line_number) + ': skipping parameter ' +
                  'space vertex definition: ' + line)

        # Face definition: a token can contain '/' to separate vertex
        # index from texture and normal index, see the split() method.
        elif tokens[0].strip() == 'f':
            face = []
            # The try block catches exceptions raised by the split function.
            # If an exception is raised the face could not be parsed and
            # the contents of face have to be discarded.
            try:
                for i in range(1, len(tokens)):
                    face.append(split(tokens[i].strip()))
            except ValueError:
                msg = ('read(): ' + str(line_number) + ': could not ' +
                       'parse: ' + line)
                raise RuntimeError(msg)

            # Reaching this point means that all components of a face
            # definition were successfully read. The face can still have
            # too few vertices to qualify as a face.
            if len(face) < 3:
                msg = ('read(): ' + str(line_number) + ': skipping ' +
                       'degenerate face: ' + line)
                warnings.warn(msg, RuntimeWarning)
            else:
                # The elements of face are set by the split function which
                # always returns a triple (v, vt, vn). All or only a subset
                # of those values are returned.
                if read_vt and read_vn:
                    F.append(face)
                elif read_vt:
                    F.append([(v[0], v[1]) for v in face])
                elif read_vn:
                    F.append([(v[0], None, v[2]) for v in face])
                else:
                    F.append([v[0] for v in face])

        # Curve/surface definition: the definition/object stays active
        # (has a non None value) until an 'end' statement is encountered.
        elif tokens[0].strip() == 'cstype':
            # There is a problem with the file if a cstype definition is
            # found before the previous active one was properly terminated.
            if current_cst is not None:
                msg = ("read(): " + str(line_number) + ": expected 'end' " +
                       "statement, got: " + line)
                raise RuntimeError(msg)

            # If none of the two branches is executed current_cst retains
            # its None value. CSType creation may raise a ValueError.
            if len(tokens) == 2:
                current_cst = CSType(tokens[1].strip())
            elif len(tokens) == 3:
                current_cst = CSType(tokens[2].strip(), tokens[1].strip())

        # Curve/surface degree specification: either one or two integers
        # are excepted.
        elif tokens[0].strip() == 'deg' and current_cst:
            if len(tokens) == 2:
                current_cst._deg = (int(tokens[1].strip()), )
            elif len(tokens) == 3:
                current_cst._deg = (int(tokens[1].strip()),
                                    int(tokens[2].strip()))
            else:
                msg = ("read(): " + str(line_number) + ": invalid: " + line)
                raise RuntimeError(msg)

        # Surface definition: the first 4 floats after 'surf' define the
        # u and v intervals over which the surface should be visualized.
        elif tokens[0].strip() == 'surf' and current_cst:
            if len(tokens) > 5:
                current_cst._rangeu = (float(tokens[1].strip()),
                                       float(tokens[2].strip()))
                current_cst._rangev = (float(tokens[3].strip()),
                                       float(tokens[4].strip()))
                current_cst._vid = []

                # All remaining values are vertex indices of surface
                # control points.
                for i in range(5, len(tokens)):
                    vid, tid, nid = split(tokens[i].strip())
                    current_cst._vid.append(vid)
            else:
                msg = ("read(): " + str(line_number) + ": not enough " +
                       "values provided: " + line)
                raise RuntimeError(msg)

        # Curve definition: the first 2 floats after 'curv' define the
        # u interval over which the curve should be visualized.
        elif tokens[0].strip() == 'curv' and current_cst:
            if len(tokens) > 3:
                current_cst._rangeu = (float(tokens[1].strip()),
                                       float(tokens[2].strip()))
                current_cst._vid = []

                # All remaining values are vertex indices of curve
                # control points.
                for i in range(3, len(tokens)):
                    vid, tid, nid = split(tokens[i].strip())
                    current_cst._vid.append(vid)
            else:
                msg = ("read(): " + str(line_number) + ": not enough " +
                       "values provided: " + line)
                raise RuntimeError(msg)

        # Discard the current cstype since curv2 statements are not yet
        # supported.
        elif tokens[0].strip() == 'curv2' and current_cst:
            current_cst = None
            msg = ('read(): ' + str(line_number) + ': skipping special ' +
                   'curve definition: ' + line)
            warnings.warn(msg, RuntimeWarning)

        # Knot vector definition(s): knot values in u direction, have to
        # be there for curves and surfaces.
        elif tokens[0].strip() == 'parm' and current_cst:
            if len(tokens) > 3:
                if tokens[1].strip() == 'u':
                    parmu = []
                    for i in range(2, len(tokens)):
                        parmu.append(float(tokens[i].strip()))
                    current_cst._parmu = tuple(parmu)
                elif tokens[1].strip() == 'v':
                    parmv = []
                    for i in range(2, len(tokens)):
                        parmv.append(float(tokens[i].strip()))
                    current_cst._parmv = tuple(parmv)

        # End of cstype definition. Add the active CSType object to the
        # list of all curves and surfaces.
        elif tokens[0].strip() == 'end' and current_cst:
            CS.append(current_cst)
            current_cst = None

        # Point definition: multiple points can be specified within a
        # single statement on the same line begining with 'p'
        elif tokens[0].strip() == 'p':
            print('read(): ' + str(line_number) + ': skipping point ' +
                  'definition: ' + line)

        # Polyline definition: a polyline is defined by a sequence of
        # geometric vertices. Definitions in the form v/vt are allowed.
        elif tokens[0].strip() == 'l':
            print('read(): ' + str(line_number) + ': skipping polyline ' +
                  'definition: ' + line)

        # Skip all comments in the file.
        elif tokens[0].strip() == '#':
            pass

        # All other statements that are not handled so far...
        else:
            pass

    file.close()

    # Extract the control points of a curve/surface from the list of all
    # geometric vertices and convert to an array of appropriate dimensinos.
    for cs in CS:
        cs._cps = np.array([V[i] for i in cs._vid])
        cs._generate_cparray()

    # Default order of returned arguments and the corresponding list of
    # values to be returned.
    types = ['v', 'f', 'vt', 'vn', 'cstype']
    rdefs = [V, F, VT, VN, CS]

    # Desired order of returned values as a permutation applied to rdefs.
    rvali = [types.index(type) for type in args if type in types]

    # If there is only one requested return value we do not return a one
    # element tuple but the one value itself.
    if len(rvali) == 1: return rdefs[rvali[0]]

    # If no return value is requested this will return an empty tuple.
    return tuple(rdefs[i] for i in rvali)


def write(filename, **kwargs):
    """ Write mesh data to OBJ file.

    Parameters
    ----------
    filename : str
        Name of output file.

    Keyword Arguments
    -----------------
    v : array_like
        Vertex coordinates.
    f : array_like
        Face definitions.
    vt : array_like
        Texture coordinates.
    vn : array_like
        Vertex normals.


    If normals and/or texture coordinates are involved, face definitions should
    be of the form as described in the documentation of :py:func:`read`, i.e.,
    the OBJ constructs v/vt, v//vn, and v/vt/vn should be modeled as
    corresponding tuples (v, vt), (v, None, vn) and (v, vt, vn), respectively.
    If faces are defined as ``list[int]`` normals and texture coordinates are
    still written but their correspondence to vertices is lost. Executing the
    script

    .. literalinclude:: ../../examples/cube_write.py
       :lines: 8-

    results in an OBJ file with the following contents:

    .. literalinclude:: ../../data/cube.obj
       :lines: 1-
    """
    # Open file in write mode 'w'. Could put a small header with creation time?
    # If the file already exists its contents will be replaced.
    file = open(filename, 'w')

    # Check for 'v' keyword parameter. Write all vertices to the file if given.
    try:
        V = kwargs['v']
    except KeyError:
        pass
    else:
        for v in V:
            file.write('v')
            for i in range(len(v)):
                file.write(' ' + str(v[i]))
            file.write('\n')

    # Check for 'vt' keyword parameter. Write all texture coordinates to the
    # file if provided.
    try:
        VT = kwargs['vt']
    except KeyError:
        pass
    else:
        for vt in VT:
            file.write('vt')
            for i in range(len(vt)):
                file.write(' ' + str(vt[i]))
            file.write('\n')

    # Check for 'vn' keyword argument. Write all normals to the file if given.
    try:
        VN = kwargs['vn']
    except KeyError:
        pass
    else:
        for vn in VN:
            file.write('vn')
            for i in range(len(vn)):
                file.write(' ' + str(vn[i]))
            file.write('\n')

    # Check for 'f' keyword argument. Write face definitions to the file if
    # given. If a vertex is iterable up to three components are interpreted
    # in order as vi/vt/vn. Surplus components are ignored. If the value vn
    # is given without vt a sequence (vi, None, vn, ...) is expected.
    try:
        F = kwargs['f']
    except KeyError:
        pass
    else:
        for f in F:
            file.write('f')
            for v in f:
                # Write all given data! Per vertex texture and normal indices
                # are written regardless of 'vt' and 'vn' kwarg values.
                try:
                    # Check if v is iterable. If not it should be a single
                    # integer, otherwise a sequence of integers.
                    vi = v[0]+1
                except TypeError:
                    # Not iterable, write to file and continue with the next
                    # vertex of the face.
                    file.write(' ' + str(v+1))
                else:
                    # Executed when the try block did not raise an exception.
                    # The vertex definition holds more information.
                    try:
                        # Try to extract uv coordinate index. If not present
                        # write the vertex index only.
                        vt = '' if v[1] is None else str(v[1]+1)
                    except IndexError:
                        file.write(' ' + str(vi))
                    else:
                        try:
                            # Try to extract normal index. If not present
                            # write vertex index and texture index only.
                            vn = '' if v[2] is None else str(v[2]+1)
                        except IndexError:
                            file.write(f' {vi}/{vt}')
                        else:
                            file.write(f' {vi}/{vt}/{vn}')
            file.write('\n')

    # Done, close the file. If no keyword arguments were given this will
    # overwrite an existing file of the same name with an empty file!
    file.close()
