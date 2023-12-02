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

""" Visualization using VTK.

Wrapper functions for `VTK <https://vtk.org/doc/nightly/html>`_ functionality.
This is not meant as a full featured set of visualization routines but should
serve as a quick and convenient way to achieve basic visualization tasks.
"""

import numpy as np
import vtk
import vtk.util.colors as vuc


_render_window = None                       # active render window, global
_renderer = []                              # all active renderers, global


def canvas(xmin, ymin, xmax, ymax, color=vuc.white, color2=None):
    """ Define viewport in the current window.

    Creates a viewport inside the current window. A viewport's size and
    position is defined relative to the size of the render window. A newly
    created canvas becomes the active viewport.

    Parameters
    ----------
    xmin : float
        Smaller x-coordinate of the viewport.
    ymin : float
        Smaller y-coordinate of the viewport.
    xmax : float
        Larger x-coordinate of the viewport.
    ymax : float
        Larger y-coordinate of the viewport.
    color : array_like, optional
        Bottom background color as RGB intensity triplet.
    color2 : array_like, optional
        Top background color as RGB intensity triplet.

    Returns
    -------
    vtkRenderer
        Renderer responsible for the created viewport. Can be used to
        add/delete actors, set the background color, resize the viewport etc.


    A minimal :download:`script <../../examples/vtk_canvas.py>` that opens a
    render window with three viewports. Each viewport uses a different
    background color.

    .. literalinclude:: ../../examples/vtk_canvas.py
       :lines: 8-

    A color gradient can be used as background by setting ``color2``. By
    default the value of ``color`` is used as homogeneous background color.
    A preview of named colors can be found `here
    <https://htmlpreview.github.io/?https://github.com/Kitware/vtk-examples/
    blob/gh-pages/VTKNamedColorPatches.html>`_.
    """
    # A nice choice for a background gradient from a light color at the
    # bottom to a dark color at the top of the viewport:
    # color  = vtk.util.colors.dim_grey,
    # color2 = vtk.util.colors.ivory_black

    # Basic setup: set viewport dimension relative to the size of the
    # render window.
    ren = vtk.vtkRenderer()
    ren.SetViewport(xmin, ymin, xmax, ymax)
    ren.SetBackground(color[0], color[1], color[2])

    # Defines a color gradient from background color (bottom) to
    # background2 color (top).
    if color2 is not None:
        ren.SetBackground2(color2[0], color2[1], color2[2])
        ren.SetGradientBackground(True)

    # This will improve the visual quality of transparent objects.
    ren.SetUseDepthPeeling(1)
    ren.SetOcclusionRatio(0.1)
    ren.SetMaximumNumberOfPeels(100)

    # The previously set options only work as intended if multisampling is
    # turned off. This prevents us from using MSAA. Instead use cheap FXAA.
    ren.SetUseFXAA(1)

    # Add the renderer to the list of all renderers and return a reference
    # to the caller that created the renderer.
    _renderer.append(ren)
    return ren


def add(actor, renderer=None):
    """ Queue an actor for display.

    Parameters
    ----------
    actor : vtkActor
        Instance of a renderable object.
    renderer : vtkRenderer
        The renderer/viewport to which to add the actor.


    The ``renderer`` argument should be a value returned by :py:func:`canvas`.
    If not specified the current viewport is used or a new one is created if
    this is the first object to be displayed.

    Note
    ----
    It is almost never necessary to use this function directly. It is used by
    all drawing and plotting commands automatically.
    """
    # Raise an exception if the function is not used as intended.
    if renderer is not None and renderer not in _renderer:
        msg = ('add(): The specified render was not created using the ' +
               'canvas() function!')
        raise ValueError(msg)

    # In case this is the first time an actor is displayed and no canvas
    # has been defined explicitly.
    if not len(_renderer):
        canvas(0.0, 0.0, 1.0, 1.0)

    # If no renderer is specified use the last one created, i.e., the
    # 'active' renderer/viewport.
    if renderer is None:
        renderer = _renderer[-1]

    # Check if the actor is a 3D prop or 2D. Different functions are used
    # to add them to the viewport.
    if isinstance(actor, vtk.vtkActor2D): renderer.AddActor2D(actor)
    elif isinstance(actor, vtk.vtkActor): renderer.AddActor(actor)
    else:
        msg = 'add(): Cannot handle the passed render object!'
        raise ValueError(msg)


def delete(actor):
    """ Remove actor.

    Searches all defined viewports and tries to remove the given actor.

    Parameters
    ----------
    actor : vtkActor
        Actor instance to be removed.

    Note
    ----
    This will prevent an object from being displayed. As long as there are
    other references to it, it will not be removed from memory.
    """
    for ren in _renderer: ren.RemoveActor(actor)


def update():
    """ Update viewports.

    Some changes to actors require an explicit re-render requests. Use this
    function if your changes are not diplayed properly.

    Note
    ----
    It may also be necessary to invoke the ``Modified()`` function on a data
    set to see changes.
    """
    for ren in _renderer: ren.GetRenderWindow().Render()


def scatter(P, size=2, style='.', color=(0.25, 0.25, 0.25)):
    """ Scatter plot.

    Parameters
    ----------
    P : list[~numpy.ndarray]
        Point coordinates in 2 or 3 dimensions.
    size : int
        Point size in pixels.
    style : str
        Either ``'.'`` or ``'o'`` to render points as spheres.
    color : array_like
        RGB intensity triplet.

    Returns
    -------
    vtkActor
        The corresponding actor object.
    """
    P = np.atleast_2d(P)
    points = vtk.vtkPoints()

    for i in range(len(P)):
        try:
            points.InsertNextPoint(P[i][0], P[i][1], P[i][2])
        except IndexError:
            points.InsertNextPoint(P[i][0], P[i][1], 0.0)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)

    vertices = vtk.vtkVertexGlyphFilter()
    vertices.SetInputData(polyData)
    vertices.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(vertices.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)
    actor.GetProperty().SetPointSize(size)
    actor.GetProperty().SetColor(color[0], color[1], color[2])

    if style == 'o':
        actor.GetProperty().SetRenderPointsAsSpheres(True)

    add(actor)
    return actor


def mesh(M, *args, **kwargs):
    """ Basic mesh visualization.

    Displays meshes immersed in :math:`\mathbb{R}^2` and :math:`\mathbb{R}^3`.
    A mesh may be represented as :py:class:`~geopy.halfedgemesh.Mesh` or as a
    pair (V, F) with components of type ``list[ndarray]`` and ``list[int]``.

    Parameters
    ----------
    M
        Either indexed or halfedge based mesh representation.
    *args
        Variable length argument list. Pass ``'colorbar'`` as argument to
        show a color bar when using a color map.

    Keyword Arguments
    -----------------
    vt : list[ndarray] or list[float]
        Vertex texture information.
    ft : list[ndarray] or list[float]
        Face texture information.
    vn : list[ndarray]
        Vertex normals.
    color : array_like, shape (3,)
        Global mesh color.
    cmap : str
        Color map identifier. Valid values are 'jet', 'hot', and 'grey'.
    crange : (float, float)
        A pair of floats that define the range of the color map.
    img : str or vtkTexture
        Texture map.

    Raises
    ------
    IndexError
        If vertex coordinates are less than 2-dimensional.
    ValueError
        In case argument values are inconsistent.

    Returns
    -------
    vtkActor
        Corresponding actor object or a pair of actor objects if a color
        bar was created.

    Note
    ----
    Non-triangular faces are automatically triangulated by the render engine.
    This leads to visual artifacts when viewing non-planar faces from certain
    directions. This does not change ``M``!


    The appearance of the displayed mesh can be changed in several ways by
    keyword arguments. Normals as well as textures are implicitly assigned to
    vertices by their index. Hence there have to be as many vertex texture
    coordinates and vertex normals as vertices. Specifying normals via the
    ``vn`` keyword will result in a smoothly shaded mesh.


    Note
    ----
    The type of shading algorithm applied can be selected via one of the
    ``SetInterpolation*()`` methods of an actor's property object.


    If given, the argument ``vt`` is interpreted in different ways depending
    on its shape and the presence of other keyword arguments:

       * If ``img`` is given, ``vt`` should hold :math:`(u,v)` coordinates,
         one such value for each vertex. If this is not the case and if
         ``vt`` can be interpreted in one of the ways described below, the
         value of ``img`` is ignored, otherwise both values are ignored.

       * If ``img`` is not given, ``vt`` can specify a float value or a triple
         of floats for each vertex.

          * In the first case the single float value is used to look up a color
            in a specified color map via the ``cmap`` keyword argument. If
            not given a default color map is used. By default the color map
            scales to the range given by the smallest and largest value in
            ``vt``. This can be changed via the ``crange`` keyword argument.

          * In the second case the triple is interpreted as a RGB color
            intensity triplet. Colors are linearly interpolated across faces.

    Similar to ``vt`` the keyword argument ``ft`` can be used to set face
    colors either via a lookup table or by directly specifiying RGB intensity
    triplets on a per face basis.

    Note
    ----
    Vertex normals and vertex texture coordinates that are also face dependent
    -- as allowed in the Wavefront OBJ format -- are not supported. If faces
    include this information it is ignored.
    """
    # Point and face array setup. Vertex coordinates and face definitions are
    # always given.
    point_array = vtk.vtkPoints()
    face_array = vtk.vtkCellArray()

    # Detect the input type. A halfedge mesh M or and indexed mesh M = (V,F)
    # is expected as input.
    try:
        nverts = M.num_vertices()
        nfaces = M.num_faces()
    except AttributeError:
        try:
            V = M[0]
            F = M[1]
        except (TypeError, IndexError):
            msg = ('mesh(): expecting indexed mesh (V, F) or halfedge ' +
                   'mesh M as input!')
            raise ValueError(msg)
        else:
            # The indexed mesh case. Fill vertex and face arrays. Texture
            # information on the face level is ignored.
            for v in V:
                try:
                    point_array.InsertNextPoint(v[0], v[1], v[2])
                except IndexError:
                    point_array.InsertNextPoint(v[0], v[1], 0.0)

            for f in F:
                face = vtk.vtkIdList()
                for vdef in f:
                    try:
                        face.InsertNextId(vdef[0])
                    except (TypeError, IndexError):
                        face.InsertNextId(vdef)
                face_array.InsertNextCell(face)

            # Set the total number of vertices. Used later to check if there
            # are enough normals and vertex texture coordinates.
            nverts = len(V)
            nfaces = len(F)
    else:
        # The halfedge mesh case. The variables nverts and nfaces have
        # already been set.
        for v in M.vertices():
            p = v.point
            try:
                point_array.InsertNextPoint(p[0], p[1], p[2])
            except IndexError:
                point_array.InsertNextPoint(p[0], p[1], 0.0)

        for f in M.faces():
            face = vtk.vtkIdList()
            for v in f.vertices():
                face.InsertNextId(v.index)
            face_array.InsertNextCell(face)

    # Start building the VTK representation of the mesh. Further data like
    # normals and texture are added along the way.
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(point_array)
    polyData.SetPolys(face_array)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    # Check if vertex normals were specified. Set normals if their number
    # matches the number of vertices.
    try:
        VN = kwargs['vn']
    except KeyError:
        pass
    else:
        if len(VN) == nverts:
            normal_array = vtk.vtkFloatArray()
            normal_array.SetNumberOfComponents(3)
            for n in VN:
                normal_array.InsertNextTuple3(n[0], n[1], n[2])
            polyData.GetPointData().SetNormals(normal_array)
        else:
            msg = ('mesh(): vertex normals were specified but their ' +
                   'number does not match the number of vertices!')
            raise ValueError(msg)

    # Check for vertex texture information. Add texture information to VTK
    # mesh representation accordingly.
    try:
        VT = kwargs['vt']
    except KeyError:
        pass
    else:
        # Convert to ndarray if not already the case. Makes it easier to
        # check dimensionality.
        texels = np.asarray(VT)

        if texels.ndim == 1:
            # Texels are one dimensional, i.e., intensity values or values
            # used to look up colors.
            texdim = 1
        elif texels.ndim == 2:
            # Texels are two or three dimensional, either (u,v) values or
            # (r,g,b) triplets.
            texdim = texels.shape[1]

        if texdim not in {1,2,3}:
            msg = ("mesh(): don't know how to handle texture elements " +
                   "with " + str(texdim) + " dimensions.")
            raise ValueError(msg)

        # Proceed by adding texture information to VTK's mesh representation.
        # Do nothing if sizes don't match.
        if len(VT) == nverts:
            texel_array = vtk.vtkFloatArray()
            texel_array.SetNumberOfComponents(texdim)

            for t in texels:
                if   texdim == 1: texel_array.InsertNextTuple1(t)
                elif texdim == 2: texel_array.InsertNextTuple2(t[0], t[1])
                elif texdim == 3: texel_array.InsertNextTuple3(t[0], t[1], t[2])

            if texdim == 1:
                # Vertex colors are assigned by using a lookup table.
                polyData.GetPointData().SetScalars(texel_array)
                mapper.SetScalarModeToUsePointData()
                mapper.ScalarVisibilityOn()

                # Start setting up the lookup table. This is the default
                # color ramp which is kind of an inverse 'jet' color map.
                lut = vtk.vtkLookupTable()
                lut.SetNumberOfTableValues(512)

                # Query the camp keyword argument. If not given stick with
                # the default color map.
                try:
                    CMAP = kwargs['cmap']
                except KeyError:
                    pass
                else:
                    # Adapt the color map if a supported value is given.
                    # Otherwise raise an unkown cmap value exception.
                    if CMAP == 'hot':
                        lut.SetHueRange(0, 1/6)
                        lut.SetSaturationRange(1, 0.5)
                        lut.SetValueRange(1, 1)
                    elif CMAP == 'jet':
                        lut.SetHueRange(2/3, 0)
                        lut.SetSaturationRange(1, 1)
                        lut.SetValueRange(1, 1)
                    elif CMAP == 'grey':
                        lut.SetHueRange(0, 0)
                        lut.SetSaturationRange(0, 0)
                        lut.SetValueRange(0, 1)
                    else:
                        msg = ('mesh(): unknown color map: ' + CMAP)
                        raise ValueError(msg)

                # Query the crange keyword argument. If not given the color
                # map scales to the provided values.
                try:
                    CRANGE = kwargs['crange']
                except KeyError:
                    lut.SetTableRange(np.min(texels), np.max(texels))
                else:
                    lut.SetTableRange(CRANGE[0], CRANGE[1])

                lut.Build()

                mapper.SetColorModeToMapScalars()
                mapper.SetLookupTable(lut)
                mapper.SetUseLookupTableScalarRange(True)

                # Create a correponding color bar for visualization if
                # requested by the caller.
                if 'colorbar' in args:
                    scalarBar = vtk.vtkScalarBarActor()
                    scalarBar.SetNumberOfLabels(5)
                    scalarBar.SetBarRatio(0.2)
                    scalarBar.GetLabelTextProperty().SetFontSize(14)
                    scalarBar.SetUnconstrainedFontSize(True)
                    scalarBar.SetLookupTable(lut)
                    scalarBar.SetPickable(False)
            elif texdim == 2:
                # Vertex colors are assigned by uv-mapping.
                polyData.GetPointData().SetTCoords(texel_array)
            elif texdim == 3:
                # Vertex colors are assigned directly as RGB triplets.
                polyData.GetPointData().SetScalars(texel_array)
                mapper.SetScalarModeToUsePointData()
                mapper.ScalarVisibilityOn()
                mapper.SetColorModeToDirectScalars()
        else:
            msg = ('mesh(): texture coordinates were specified but their ' +
                   'number does not match the number of vertices!')
            raise ValueError(msg)

    # Check for face texture information. Add texture information to VTK's
    # mesh representation accordingly.
    try:
        FT = kwargs['ft']
    except KeyError:
        pass
    else:
        # Convert to ndarray if not already the case. Makes it easier to
        # check dimensionality.
        texels = np.asarray(FT)

        if texels.ndim == 1:
            # Texels are one dimensional, i.e., intensity values or values
            # used to look up colors.
            texdim = 1
        elif texels.ndim == 2:
            # Texels are two or three dimensional, either (u,v) values or
            # (r,g,b) triplets.
            texdim = texels.shape[1]

        if texdim not in {1,3}:
            msg = ("mesh(): don't know how to handle texture elements " +
                   "with " + str(texdim) + " dimensions.")
            raise ValueError(msg)

        # Proceed by adding texture information to VTK's mesh representation.
        # Do nothing if sizes don't match.
        if len(FT) == nfaces:
            texel_array = vtk.vtkFloatArray()
            texel_array.SetNumberOfComponents(texdim)

            for t in texels:
                if   texdim == 1: texel_array.InsertNextTuple1(t)
                elif texdim == 3: texel_array.InsertNextTuple3(t[0], t[1], t[2])

            polyData.GetCellData().SetScalars(texel_array)
            mapper.SetScalarModeToUseCellData()
            mapper.ScalarVisibilityOn()

            if texdim == 1:
                # Start setting up the lookup table. This is the default
                # color ramp which is kind of an inverse 'jet' color map.
                lut = vtk.vtkLookupTable()
                lut.SetNumberOfTableValues(512)

                # Query the camp keyword argument. If not given stick with
                # the default color map.
                try:
                    CMAP = kwargs['cmap']
                except KeyError:
                    pass
                else:
                    # Adapt the color map if a supported value is given.
                    # Otherwise raise an unkown cmap value exception.
                    if CMAP == 'hot':
                        lut.SetHueRange(0, 1/6)
                        lut.SetSaturationRange(1, 0.5)
                        lut.SetValueRange(1, 1)
                    elif CMAP == 'jet':
                        lut.SetHueRange(2/3, 0)
                        lut.SetSaturationRange(1, 1)
                        lut.SetValueRange(1, 1)
                    elif CMAP == 'grey':
                        lut.SetHueRange(0, 0)
                        lut.SetSaturationRange(0, 0)
                        lut.SetValueRange(0, 1)
                    else:
                        msg = ('mesh(): unknown color map: ' + CMAP)
                        raise ValueError(msg)

                # Query the crange keyword argument. If not given the color
                # map scales to the provided values.
                try:
                    CRANGE = kwargs['crange']
                except KeyError:
                    lut.SetTableRange(np.min(texels), np.max(texels))
                else:
                    lut.SetTableRange(CRANGE[0], CRANGE[1])

                lut.Build()

                mapper.SetColorModeToMapScalars()
                mapper.SetLookupTable(lut)
                mapper.SetUseLookupTableScalarRange(True)

                # Create a correponding color bar for visualization if
                # requested by the caller.
                if 'colorbar' in args:
                    scalarBar = vtk.vtkScalarBarActor()
                    scalarBar.SetNumberOfLabels(5)
                    scalarBar.SetBarRatio(0.2)
                    scalarBar.GetLabelTextProperty().SetFontSize(14)
                    scalarBar.SetUnconstrainedFontSize(True)
                    scalarBar.SetLookupTable(lut)
                    scalarBar.SetPickable(False)
            elif texdim == 3:
                # Face colors are assigned directly as RGB triplets.
                mapper.SetColorModeToDirectScalars()
        else:
            msg = ('mesh(): texture coordinates were specified but their ' +
                   'number does not match the number of vertices!')
            raise ValueError(msg)

    # Finalize the VTK render object representation. Add texture image if it
    # was given. Need an actor for that.
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)

    # Query the img keyword argument. Load and set the corresponding texture.
    # Setting the texture has no effect if texture coordinates are not set.
    try:
        IMG = kwargs['img']
    except KeyError:
        pass
    else:
        if isinstance(IMG, vtk.vtkTexture):
            actor.SetTexture(IMG)
        else:
            readerFactory = vtk.vtkImageReader2Factory()
            textureReader = readerFactory.CreateImageReader2(IMG)
            textureReader.SetFileName(IMG)
            textureReader.Update()

            texture = vtk.vtkTexture()
            texture.InterpolateOn()
            texture.SetInputConnection(textureReader.GetOutputPort())
            actor.SetTexture(texture)

    # Set global mesh color. Overwrites all other appearance attributes.
    try:
        color = kwargs['color']
    except KeyError:
        pass
    else:
         actor.GetProperty().SetColor(color[0], color[1], color[2])

    try:
        scalarBar
    except NameError:
        add(actor)                      # add the mesh actor
        return actor                    # and return it to the caller
    else:
        add(scalarBar)                  # add the scalar bar actor
        add(actor)                      # and the mesh actor
        return actor, scalarBar         # and return both to the caller


def quiver(P, N, scale=1.0, color=(0.5, 0.5, 0.5)):
    """ Quiver plot.

    Display arrows at given locations pointing in given directions. For
    each point exactly one direction vector has to be given.

    Parameters
    ----------
    P : array_like
        A list of :math:`(x,y,z)` point coordinates.
    N : array_like
        A list of vectors with coordinates :math:`(u,v,w)`.
    scale : float or array_like
        Scale of the displayed arrows. Either one global scale factor
        or one scalar per point/arrow pair.
    color : array_like
        Color specification. Either one global RGB color triplet or
        one color triplet per point/arrow pair.

    Raises
    ------
    ValueError
        If the sizes/shapes of input arguments do not match up.

    Returns
    -------
    vktActor
        Corresponding actor object.
    """
    # The total number of point/vector pairs. Glyph color and scale arrays
    # have to be of the same length.
    n = len(P)

    # Check number of vectors.
    if len(N) != n:
        msg = ('quiver(): the given number of points and vectors are ' +
               'inconsistent!')
        raise ValueError(msg)

    # Check number of scale factors.
    if np.shape(scale) != (n,):
        if isinstance(scale, int) or isinstance(scale, float):
            scale = np.tile(scale, (n,))
        else:
            msg = ('quiver(): the given number of scale factors does not ' +
                   'match the number of point/vector pairs!')
            raise ValueError(msg)

    # Check number of colors.
    if np.shape(color) != (n,3):
        if np.shape(color) == (3,):
            color = np.tile(color, (n,1))
        else:
            msg = ('quiver(): the given number of colors does not match ' +
                   'the number of point/vector pairs!')
            raise ValueError(msg)

    # Prepare the data buffers used by VTK and fill them with the data
    # provided.
    points = vtk.vtkPoints()

    vectors = vtk.vtkFloatArray()
    vectors.SetNumberOfComponents(3)

    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName('glyph_scale')

    colors = vtk.vtkFloatArray()
    colors.SetNumberOfComponents(3)
    colors.SetName('glyph_color')

    for i in range(n):
        points.InsertNextPoint(P[i][0], P[i][1], P[i][2])
        vectors.InsertNextTuple3(N[i][0], N[i][1], N[i][2])
        scalars.InsertNextTuple1(scale[i])
        colors.InsertNextTuple3(color[i][0], color[i][1], color[i][2])

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.GetPointData().SetVectors(vectors)
    polyData.GetPointData().AddArray(scalars)
    polyData.GetPointData().AddArray(colors)
    polyData.GetPointData().SetActiveScalars('glyph_scale')

    # The source shape used for glyphs. If rendering is too slow when there
    # is a large number of glyphs, the resolution of each can be reduced.
    arrow = vtk.vtkArrowSource()
    arrow.SetTipRadius(1.75*arrow.GetShaftRadius())
    arrow.SetTipLength(0.5)
    arrow.SetTipResolution(10)
    arrow.SetShaftResolution(10)

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.OrientOn()
    glyph.SetVectorModeToUseVector()
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SetColorModeToDirectScalars()
    mapper.ScalarVisibilityOn()
    mapper.SelectColorArray('glyph_color')

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)

    add(actor)
    return actor


def _surface(X, Y, Z, faces=[], normals=[], col=[1.0, 1.0, 1.0], cm='jet'):
    """
    Surface plot.

    Diplays regular grids and unstructed grids (i.e., triangulations) with
    vertices defined by the given coordinate matrices.

    Parameters
    ----------
    X, Y, Z : array_like
        Coordinate arrays. If no connectivity information is given a regular
        grid is assumed, i.e., shape (m,n) is expected.
    faces : array_like
        A sequence of face defintions.
    normals : array_like
        Vertex normals, one coordinate triplet for each (x,y,z) vertex location
        in the same order as vertex coordinates.
    col : array_like
        Color attribute, can be a single RGB triplet to be used as global mesh
        color or per vertex color information that is interpolated.

    Returns
    -------
    actor :
        A vtk actor for visualization.
    """
    # Input arrays need to have the same shape
    if not np.shape(X) == np.shape(Y) == np.shape(Z):
        sys.exit('X, Y, Z dimension mismatch!')

    # Vertex normal data
    normals_array = vtk.vtkFloatArray()
    normals_array.SetNumberOfComponents(3)
    normals_ok = False

    # Take care of colors: Check if the size is correct, otherwise (or if only
    # a single value is given) create a suitable array of RGB triplets.
    colors_direct = True

    if np.shape(col) == (3,):
        # A single RGB triplet was given for all vertices of the mesh
        col_shape = list(np.shape(X))
        col_shape.append(1)
        # Repeat the RGB triplet for every vertex of the mesh
        col = np.tile(col, col_shape)
    elif np.shape(col) == np.shape(X):
        # A color index was given for every vertex of the mesh
        colors_direct = False
    else:
        # One RGB triplet was given for every vertex of the mesh
        col_shape = list(np.shape(X))
        col_shape.append(3)
        if  list(np.shape(col)) != col_shape:
            sys.exit('Color array size mismatch!')

    if colors_direct:
        colors_array = vtk.vtkUnsignedCharArray()
        colors_array.SetNumberOfComponents(3)
    else:
        colors_array = vtk.vtkFloatArray()
        colors_array.SetNumberOfComponents(1)

    # If F is given it defines the faces of the mesh, i.e., F is a list of
    # tuples/lists, each tuple defines a face.
    if len(faces):
        # Process the vertex normal data, if any.
        if np.shape(normals) == (len(X), 3):
            normals_ok = True
            for n in normals:
                normals_array.InsertNextTuple3(n[0], n[1], n[2])

        # Build the vtk representation of the mesh
        points_array = vtk.vtkPoints()
        for i in range(len(X)):
            points_array.InsertNextPoint(X[i], Y[i], Z[i])
            if colors_direct:
                colors_array.InsertNextTuple3(255*col[i][0],
                                              255*col[i][1],
                                              255*col[i][2])
            else:
                colors_array.InsertNextTuple1(col[i])

        faces_array = vtk.vtkCellArray()
        for f in faces:
            face = vtk.vtkIdList()
            for i in f:
                face.InsertNextId(i)
            faces_array.InsertNextCell(face)

    # F is not given, the connectivity is implicitly defined by the shape of
    # the matrices X, Y, and Z.
    else:
        if len(np.shape(X)) != 2:
            sys.exit('Coordinate matrices need to be of shape (m,n)')

        # Build the vtk representation of the mesh
        points_array = vtk.vtkPoints()
        m, n = np.shape(X)
        for i in range(m):
            for j in range(n):
                points_array.InsertNextPoint(X[i,j], Y[i,j], Z[i,j])
                if colors_direct:
                    colors_array.InsertNextTuple3(255*col[i,j][0],
                                                  255*col[i,j][1],
                                                  255*col[i,j][2])
                else:
                    colors_array.InsertNextTuple1(col[i,j])

        if np.shape(normals) == (m, n, 3):
            normals_ok = True
            for i in range(m):
                for j in range(n):
                    normals_array.InsertNextTuple3(normals[i,j][0],
                                                   normals[i,j][1],
                                                   normals[i,j][2])

        faces_array = vtk.vtkCellArray()
        for i in range(m-1):
            for j in range(n-1):
                face = vtk.vtkIdList()
                face.InsertNextId(i*n+j)
                face.InsertNextId((i+1)*n+j)
                face.InsertNextId((i+1)*n+j+1)
                face.InsertNextId(i*n+j+1)
                faces_array.InsertNextCell(face)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points_array)
    polyData.SetPolys(faces_array)
    polyData.GetPointData().SetScalars(colors_array)

    # Set vertex normal data
    if normals_ok: polyData.GetPointData().SetNormals(normals_array)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)
    mapper.SetScalarModeToUsePointData()
    mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)
    add(actor)

    if colors_direct:
        mapper.SetColorModeToDirectScalars()
        return actor
    else:
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange(np.min(col), np.max(col))
        hueLut.SetNumberOfTableValues(512)

        if cm == 'hot':
            hueLut.SetHueRange(0, 1/6)
            hueLut.SetSaturationRange(1, 0.5)
            hueLut.SetValueRange(1, 1)
        else:
            hueLut.SetHueRange(2/3, 0)
            hueLut.SetSaturationRange(1, 1)
            hueLut.SetValueRange(1, 1)

        hueLut.Build()

        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(hueLut)
        mapper.SetUseLookupTableScalarRange(True)

        scalarBar = vtk.vtkScalarBarActor()
        scalarBar.SetNumberOfLabels(5)
        scalarBar.SetBarRatio(0.2)
        scalarBar.GetLabelTextProperty().SetFontSize(14)
        scalarBar.SetUnconstrainedFontSize(True)
        scalarBar.SetLookupTable(hueLut)

        renderer[-1].AddActor2D(scalarBar)
        return actor, scalarBar


def _surface2(X, Y, Z, faces=[], normals=[], color=vtk.util.colors.snow,
             vertex_scalars=[], face_scalars=[], scalar_range=None,
             color_lookup='ordinal', color_map='jet', color_scheme=0):
    """
    Surface plot.

    Diplay regular grids and unstructed grids with vertex locations defined
    by the given coordinate matrices (and connectivity information given as
    a list of face definitions in the case of unstructured grids).

    Surfaces can be colored in different ways. Either give a global color to
    be applied to all faces of the mesh or provide scalar values at vertices
    or faces (if both are given face_scalars take precedence). Scalar values
    are mapped to colors either categorically (indexed lookup, in this case
    scalars should be integers) using the given color series or in an ordinal
    fashion by using the given color map. In the second case the range of the
    table used for lookup is set to range of the provided scalars. At different
    range can be provided.

    Parameters
    ----------
    X, Y, Z : array_like, shape(n,) or shape(m,n)
        Coordinate arrays. Either shape(n,) together with a non-empty face list
        or shape(m,n) for regular grids with implicitly defined connectivity.
    faces : array_like
        A sequence of face defintions. Faces are not required to have the
        same number of vertices. Ignored when the coordinate arrays are of
        shape(m,n)
    normals : array_like
        Vertex normals, one triplet for each (x,y,z) vertex location. Setting
        vertex normals switches from flat shaded faces to Gourad shading.
    color : array_like
        Color attribute, can be a single RGB intensity triplet to be used as
        global mesh color or per vertex color information that is interpolated
        across faces.

    Returns
    -------
    VTK actor. Can be used to further modify the appearance of the surface.
    """
    vertex_scalars_ok = False
    if len(vertex_scalars) and np.shape(vertex_scalars) == np.shape(X):
        if color_lookup == 'ordinal':
            vertex_scalar_array = vtk.vtkFloatArray()
        else:
            vertex_scalar_array = vtk.vtkIntArray()
        vertex_scalar_array.SetNumberOfComponents(1)
        vertex_scalars_ok = True

    face_scalars_ok = False
    if len(face_scalars) and len(faces) == len(face_scalars):
        if color_lookup == 'ordinal':
            face_scalar_array = vtk.vtkFloatArray()
        else:
            face_scalar_array = vtk.vtkIntArray()
        face_scalar_array.SetNumberOfComponents(1)
        face_scalars_ok = True

    normals_ok = False
    if len(normals) and list(np.shape(normals)) == list(np.shape(X)) + [3]:
        normals_ok = True
        normal_array = vtk.vtkFloatArray()
        normal_array.SetNumberOfComponents(3)

    if np.shape(color) == (3,):
        # A single RGB triplet was given for all vertices of the mesh.
        # Repeat the RGB triplet for every vertex of the mesh
        color_shape = list(np.shape(X)) + [1]
        color = np.tile(color, color_shape)
    else:
        # One RGB triplet has to be given for every vertex of the mesh.
        color_shape = list(np.shape(X)) + [3]
        if list(np.shape(color)) != color_shape:
            raise RuntimeError()

    color_array = vtk.vtkUnsignedCharArray()
    color_array.SetNumberOfComponents(3)

    if color_lookup != 'ordinal':
        color_series = vtk.vtkColorSeries()
        color_series.SetColorScheme(color_scheme)
        num_colors = color_series.GetNumberOfColors()

    if faces:
        point_array = vtk.vtkPoints()
        for i in range(len(X)):
            point_array.InsertNextPoint(X[i], Y[i], Z[i])
            color_array.InsertNextTuple3(255*color[i][0],
                                         255*color[i][1],
                                         255*color[i][2])

            if normals_ok:
                normal_array.InsertNextTuple3(normals[i][0],
                                              normals[i][1],
                                              normals[i][2])

            if vertex_scalars_ok:
                if color_lookup == 'ordinal':
                    vertex_scalar_array.InsertNextTuple1(vertex_scalars[i])
                else:
                    if vertex_scalars[i] >= 0:
                        vertex_scalar_array.InsertNextTuple1(
                            vertex_scalars[i] % num_colors)
                    else:
                        vertex_scalar_array.InsertNextTuple1(vertex_scalars[i])

        face_array = vtk.vtkCellArray()
        for i in range(len(faces)):
            face = vtk.vtkIdList()
            for j in faces[i]:
                face.InsertNextId(j)
            face_array.InsertNextCell(face)

            if face_scalars_ok:
                if color_lookup == 'ordinal':
                    face_scalar_array.InsertNextTuple1(face_scalars[i])
                else:
                    if face_scalars[i] >= 0:
                        face_scalar_array.InsertNextTuple1(
                            face_scalars[i] % num_colors)
                    else:
                        face_scalar_array.InsertNextTuple1(face_scalars[i])
    else:
        # If no face list is given, the connectivity is implicitly defined
        # by the shape of the matrices X, Y, and Z.
        raise ValueError()
        # if len(np.shape(X)) != 2:
        #     sys.exit('Coordinate matrices need to be of shape (m,n)')

        # # Build the vtk representation of the mesh
        # points_array = vtk.vtkPoints()
        # m, n = np.shape(X)
        # for i in range(m):
        #     for j in range(n):
        #         points_array.InsertNextPoint(X[i,j], Y[i,j], Z[i,j])
        #         if colors_direct:
        #             colors_array.InsertNextTuple3(255*col[i,j][0],
        #                                           255*col[i,j][1],
        #                                           255*col[i,j][2])
        #         else:
        #             colors_array.InsertNextTuple1(col[i,j])

        # if np.shape(normals) == (m, n, 3):
        #     normals_ok = True
        #     for i in range(m):
        #         for j in range(n):
        #             normals_array.InsertNextTuple3(normals[i,j][0],
        #                                            normals[i,j][1],
        #                                            normals[i,j][2])

        # faces_array = vtk.vtkCellArray()
        # for i in range(m-1):
        #     for j in range(n-1):
        #         face = vtk.vtkIdList()
        #         face.InsertNextId(i*n+j)
        #         face.InsertNextId((i+1)*n+j)
        #         face.InsertNextId((i+1)*n+j+1)
        #         face.InsertNextId(i*n+j+1)
        #         faces_array.InsertNextCell(face)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(point_array)
    polyData.SetPolys(face_array)
    polyData.GetPointData().SetScalars(color_array)

    if normals_ok:
        polyData.GetPointData().SetNormals(normal_array)

    if vertex_scalars_ok:
        polyData.GetPointData().SetScalars(vertex_scalar_array)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)
    mapper.SetScalarModeToUsePointData()
    mapper.SetColorModeToDirectScalars()
    mapper.ScalarVisibilityOn()

    if face_scalars_ok:
        polyData.GetCellData().SetScalars(face_scalar_array)
        mapper.SetScalarModeToUseCellData()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)
    add(actor)

    if vertex_scalars_ok or face_scalars_ok:
        if color_lookup == 'ordinal':
            hueLut = vtk.vtkLookupTable()
            hueLut.SetNumberOfTableValues(256)

            if vertex_scalars_ok:
                hueLut.SetTableRange(np.min(vertex_scalars),
                                     np.max(vertex_scalars))

            if face_scalars_ok:
                hueLut.SetTableRange(np.min(face_scalars),
                                     np.max(face_scalars))

            if scalar_range:
                hueLut.SetTableRange(scalar_range[0],
                                     scalar_range[1])

            if color_map == 'hot':
                hueLut.SetHueRange(0, 1/6)
                hueLut.SetSaturationRange(1, 0.5)
                hueLut.SetValueRange(1, 1)
            else:
                hueLut.SetHueRange(2/3, 0)
                hueLut.SetSaturationRange(1, 1)
                hueLut.SetValueRange(1, 1)

            hueLut.Build()
        else:
            hueLut = color_series.CreateLookupTable()

            for i in range(hueLut.GetNumberOfColors()):
                hueLut.SetAnnotation(i, str(i))

        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(hueLut)
        mapper.SetUseLookupTableScalarRange(True)

        scalarBarActor = vtk.vtkScalarBarActor()
        scalarBarActor.SetNumberOfLabels(5)
        scalarBarActor.SetBarRatio(0.2)
        scalarBarActor.GetLabelTextProperty().SetFontSize(14)
        scalarBarActor.SetUnconstrainedFontSize(True)
        scalarBarActor.SetLookupTable(hueLut)
        scalarBarActor.SetPickable(False)

        add(scalarBarActor)
        return actor, scalarBarActor

    return actor


def _wireframe(X, Y, Z, faces=[], linewidth=1.0, col=[1.0, 1.0, 1.0]):
    """
    Wireframe surface plot.

    Diplays regular grids and unstructed grids (i.e., triangulations) with
    vertices defined by the given coordinate matrices.

    Parameters
    ----------
    X, Y, Z : array_like
        Coordinate arrays. If no connectivity information is given a regular
        grid is assumed, i.e., shape (m,n) is expected.
    faces : array_like
        A sequence of face defintions.
    linewidth : float
        Global line width setting for displayed edges.
    col : array_like
        Color attribute, can be a single RGB triplet to be used as global mesh
        color or per vertex color information that is interpolated.

    Returns
    -------
    actor :
        A vtk actor for visualization.
    """
    # Input arrays need to have the same shape
    if not np.shape(X) == np.shape(Y) == np.shape(Z):
        sys.exit('X, Y, Z dimension mismatch!')

    # Check color specification
    if not np.shape(col) == (3,):
        sys.exit('Single RGB color triplet expected!')

    edges_array = None
    faces_array = None

    # If F is given it defines the faces of the mesh, i.e., F is a list of
    # tuples/lists, each tuple defines a face.
    if len(faces):
        # Build the vtk representation of the mesh
        points_array = vtk.vtkPoints()
        for i in range(len(X)):
            points_array.InsertNextPoint(X[i], Y[i], Z[i])

        faces_array = vtk.vtkCellArray()
        for f in faces:
            face = vtk.vtkIdList()
            for i in f:
                face.InsertNextId(i)
            faces_array.InsertNextCell(face)

    # F is not given, the connectivity is implicitly defined by the shape of
    # the matrices X, Y, and Z.
    else:
        if len(np.shape(X)) != 2:
            sys.exit('Coordinate matrices need to be of shape (m,n)')

        # Build the vtk representation of the mesh
        points_array = vtk.vtkPoints()
        m, n = np.shape(X)
        for i in range(m):
            for j in range(n):
                points_array.InsertNextPoint(X[i,j], Y[i,j], Z[i,j])

        edges_array = vtk.vtkCellArray()
        for i in range(m):
            for j in range(n-1):
                edge = vtk.vtkIdList()
                edge.InsertNextId(i*n+j)
                edge.InsertNextId(i*n+j+1)
                edges_array.InsertNextCell(edge)

        for j in range(n):
            for i in range(m-1):
                edge = vtk.vtkIdList()
                edge.InsertNextId(i*n+j)
                edge.InsertNextId((i+1)*n+j)
                edges_array.InsertNextCell(edge)

        # faces_array = vtk.vtkCellArray()
        # for i in range(m-1):
        #     for j in range(n-1):
        #         face = vtk.vtkIdList()
        #         face.InsertNextId(i*n+j)
        #         face.InsertNextId((i+1)*n+j)
        #         face.InsertNextId((i+1)*n+j+1)
        #         face.InsertNextId(i*n+j+1)
        #         faces_array.InsertNextCell(face)

    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points_array)

    if faces_array:
        polyData.SetPolys(faces_array)

        edges = vtk.vtkExtractEdges()
        edges.SetInputData(polyData)
        edges.Update()
        edge_mapper = vtk.vtkPolyDataMapper()
        edge_mapper.SetInputData(edges.GetOutput())

        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.SetPickable(False)
        edge_actor.GetProperty().SetColor(col[0], col[1], col[2])
        edge_actor.GetProperty().SetLineWidth(linewidth)
        edge_actor.GetProperty().EdgeVisibilityOn()

        # vtk.vtkPolyDataMapper().SetResolveCoincidentTopologyToPolygonOffset()

        add(edge_actor)
        return edge_actor

    if edges_array:
        polyData.SetLines(edges_array)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(polyData)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetPickable(False)

        add(actor)
        return actor

    raise RuntimeError


def _scatter(X, Y, Z, size=1.0, style='.', color=[1.0, 1.0, 1.0], scalar=[],
            cmap='jet', cbar=False):
    """
    Visualize points at given (x,y,z) locations.

    Parameters
    ----------
    X, Y, Z : array_like
        All coordinate arrays need to be of the same shape.
    size : scalar
        A single scalar value used as size for all diplayed points. Size measures
        the number of pixels occupied by a point. Marker size does not scale when
        zooming in or out.
    style : string
        Either '.' for a square (default) or 'o' for spherical appearance of
        markers.
    color : array_like
        Color intensity triplet(s). A single triplet specifies a global color
        for all points. To specify colors on a per point basis the last axis of
        color needs to hold color intensity triplets and each intensity channel
        color[..., i], i = 0,1,2, needs to be of the same shape as X, Y, and Z.
    scalar : array_like
        Scalar data associated with points, one scalar per point, i.e., the shape
        of the scalar data needs to match that of X, Y, and Z. If specified,
        color mapping based on scalar values takes precedence of direct coloring
        using the color array.
    cmap : string
        Color map identifier. Only used when scalar data is given. Invalid values
        default to the 'jet' color map.
    cbar : boolean
        Set to True if a corresponding color bar should be created and returned.

    Returns
    -------
    ret :
        A vtk actor or a tuple (actor, cbar) if cbar is set to True when using
        scalar based color mapping.

    """
    # In case the input is given as lists of lists etc. Won't change anything
    # if the input are already ndarrays (no copying or other overhead incurred).
    X = np.atleast_1d(np.asarray(X))
    Y = np.atleast_1d(np.asarray(Y))
    Z = np.atleast_1d(np.asarray(Z))
    C = np.asarray(color)
    S = np.atleast_1d(np.asarray(scalar))

    # Input arrays need to have the same shape in order to define a valid set
    # of locations in 3-space.
    if not X.shape == Y.shape == Z.shape:
        msg = 'vis.scatter(): X, Y, Z dimension mismatch!'
        raise ValueError(msg)

    # Size needs to be a single scalar value! The vertex glyph filter does not
    # support individual marker sizes.
    if np.ndim(size):
        msg = 'vis.scatter(): size should be a single scalar value!'
        raise ValueError(msg)

    # Prepare the colors and the corresponding mapper. The geometric input data
    # is created later.
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetScalarModeToUsePointData()

    if C.shape == (3,):
        # A single RGB triplet is repeated to match the size of the coordinate
        # arrays. This results in a gobal color applied to each point location.
        C = np.tile(C, X.shape + (1,))

    if C.shape == X.shape + (3,):
        # Store color information in an unsinged char array, i.e., each intensity
        # gets mapped to the range [0, 256).
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)

        R = np.ravel(C[..., 0])
        G = np.ravel(C[..., 1])
        B = np.ravel(C[..., 2])

        for i in range(len(R)):
            colors.InsertNextTuple3(255*R[i], 255*G[i], 255*B[i])

        mapper.SetColorModeToDirectScalars()
    else:
        msg = 'vis.scatter(): color array size mismatch!'
        raise ValueError(msg)

    # Will be set to an actual actor if scalar value are properly specified and
    # cbar is set to True
    colorBar = None

    if S.shape == X.shape:
        # If the correct number of scalar values is given, color mapping based on
        # those values according to the specified color map takes precedence.
        colors = vtk.vtkFloatArray()
        colors.SetNumberOfComponents(1)

        for s in S.flat:
            colors.InsertNextTuple1(s)

        # Prepare the color lookup table. Scalar values get mapped to color
        # intensity triplets.
        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange(np.min(S), np.max(S))
        hueLut.SetNumberOfTableValues(512)

        # The default 'jet' color map lookup table
        hueLut.SetHueRange(2/3, 0)
        hueLut.SetSaturationRange(1, 1)
        hueLut.SetValueRange(1, 1)

        if cmap == 'hot':
            hueLut.SetHueRange(0, 1/6)
            hueLut.SetSaturationRange(1, 0.5)
            hueLut.SetValueRange(1, 1)
        else:
            msg = 'vis.scatter(): unknown cmap id "' + cmap + '" specified.'
            warnings.warn(msg, RuntimeWarning)

        hueLut.Build()

        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(hueLut)
        mapper.SetUseLookupTableScalarRange(True)

        if cbar:
            colorBar = vtk.vtkScalarBarActor()
            colorBar.SetNumberOfLabels(5)
            colorBar.SetBarRatio(0.2)
            colorBar.GetLabelTextProperty().SetFontSize(14)
            colorBar.SetUnconstrainedFontSize(True)
            colorBar.SetLookupTable(hueLut)

    # From now on we work with flattened arrays since the logical arrangement of
    # coordinates has no effect on a point plot.
    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)

    # Build the vtk representation of the point cloud
    points = vtk.vtkPoints()
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.GetPointData().SetScalars(colors)

    # Extracts all points from the input point set. Ignores any other type of
    # cells if they are present.
    vertices = vtk.vtkVertexGlyphFilter()
    vertices.SetInputData(polyData)
    vertices.Update()

    mapper.SetInputConnection(vertices.GetOutputPort())
    mapper.ScalarVisibilityOn()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetPointSize(size)

    # By default points are display as pixels of a given size. This can be
    # changed to spheres of the same size.
    if style == 'o': actor.GetProperty().SetRenderPointsAsSpheres(True)

    # Add the point cloud the current renderer. Also add the colorBar if there
    # is one and return both.
    add(actor)

    if colorBar:
        add(colorBar)
        return actor, colorBar

    return actor


def _scatter3(X, Y, Z, size=1.0, color=[1.0, 1.0, 1.0], scalar=[], cmap='jet',
             cbar=False):
    """
    Visualize points at given (x,y,z) locations as spheres of a given radius
    and color. Unless you need differently sized point markers you should use
    scatter2() instead.

    Parameters
    ----------
    X, Y, Z : array_like
        Coordinate arrays need to be of the same shape.
    size : array_like
        A single scalar value used as radius for all spheres. To specify individual
        radii size needs to be of the same shape as the coordinate arrays.
    color : array_like
        Color intensity triplet(s). A single triplet specifies a global color
        for all points. To specify colors on a per point basis the last axis of
        col needs to hold color intensity triplets and each intensity channel
        col[..., i], i = 0,1,2, needs to be of the same shape as X, Y, and Z.
    scalar : array_like
        Scalar data associated with points, one scalar per point, i.e., the shape
        of the scalar data needs to match the match of X, Y, and Z. If specified
        color mapping based on scalar values takes precedence of direct coloring
        using the color array.
    cmap : string
        Color map identifier. Only used when scalar data is given. Invalid values
        prevents scalar based color mapping.

    Returns
    -------
    actor :
        A vtk actor.

    """
    # In case the input is given as lists of lists etc. Won't change anything
    # if the input are already ndarrays (no copying or other overhead incurred).
    X = np.atleast_1d(np.asarray(X))
    Y = np.atleast_1d(np.asarray(Y))
    Z = np.atleast_1d(np.asarray(Z))
    C = np.asarray(color)
    D = np.atleast_1d(np.asarray(scalar))
    S = np.atleast_1d(np.asarray(size))

    # Input arrays need to have the same shape in order to define a valid set
    # of locations in 3-space.
    if not X.shape == Y.shape == Z.shape:
        msg = 'vis.scatter(): X, Y, Z dimension mismatch!'
        raise ValueError(msg)

    if np.ndim(size) == 0: S = np.tile(size, X.shape)
    if S.shape == X.shape:
        radius = vtk.vtkFloatArray()
        radius.SetName('glyph_size')
        radius.SetNumberOfComponents(1)

        S = np.ravel(S)

        for s in S:
            radius.InsertNextTuple1(s)
    else:
        msg = 'vis.scatter(): input array size mismatch!'
        raise ValueError(msg)

    # Prepare the colors and the corresponding mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetScalarModeToUsePointFieldData()

    if C.shape == (3,): C = np.tile(C, X.shape + (1,))
    if C.shape == np.shape(X) + (3,):
        colors = vtk.vtkUnsignedCharArray()
        colors.SetName('glyph_color')
        colors.SetNumberOfComponents(3)

        R = np.ravel(C[..., 0])
        G = np.ravel(C[..., 1])
        B = np.ravel(C[..., 2])

        for i in range(len(R)):
            colors.InsertNextTuple3(255*R[i], 255*G[i], 255*B[i])

        mapper.SetColorModeToDirectScalars()
    else:
        msg = 'vis.scatter(): input array size mismatch!'
        raise ValueError(msg)

    if D.shape == X.shape:
        # If the correct number of scalar values is given, color mapping based on
        # those values according to the specified color map takes precedence.
        colors = vtk.vtkFloatArray()
        colors.SetName('glyph_color')
        colors.SetNumberOfComponents(1)

        D = np.ravel(D)

        for d in D:
            colors.InsertNextTuple1(d)

        hueLut = vtk.vtkLookupTable()
        hueLut.SetTableRange(np.min(D), np.max(D))
        hueLut.SetNumberOfTableValues(512)

        if cmap == 'hot':
            hueLut.SetHueRange(0, 1/6)
            hueLut.SetSaturationRange(1, 0.5)
            hueLut.SetValueRange(1, 1)
        elif cmap == 'jet':
            hueLut.SetHueRange(2/3, 0)
            hueLut.SetSaturationRange(1, 1)
            hueLut.SetValueRange(1, 1)
        else:
            msg = 'vis.scatter(): unknown cmap id "' + cmap + '" specified.'
            warnings.warn(msg, RuntimeWarning)

        hueLut.Build()

        mapper.SetColorModeToMapScalars()
        mapper.SetLookupTable(hueLut)
        mapper.SetUseLookupTableScalarRange(True)

    # From now on we work with flattened arrays since the logical arrangement of
    # coordinates has no effect on a point plot.
    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)

    # Build the vtk representation of the point cloud
    points = vtk.vtkPoints()
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.GetPointData().AddArray(colors)
    polyData.GetPointData().AddArray(radius)
    polyData.GetPointData().SetActiveScalars('glyph_size')

    # The source shape used for glyphs. If rendering is too slow when there
    # is a large number of glyphs, the resolution of each sphere can be
    # reduced.
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(1.0)
    sphere.SetThetaResolution(20)
    sphere.SetPhiResolution(15)
    sphere.Update()

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(sphere.GetOutputPort())
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()

    mapper.SetInputConnection(glyph.GetOutputPort())
    mapper.ScalarVisibilityOn()
    mapper.SelectColorArray('glyph_color')

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)

    add(actor)
    return actor


def _plot(X, Y, Z, style='-', width=2.0, size=6.0, color=[1.0, 1.0, 1.0]):
    """
    Polyline plotting.

    Parameters
    ----------
    X, Y, Z : array_like
        Coordinate arrays of shape (m,).
    style : string
        A combination of '.', 'o', '-', and '='.
    width : float
        Width of line segments.
    size: float
        Marker size.
    col : array_like
        Global RGB color triplet for all line segments and markers.

    The style of points/lines can be changed to spheres/tubes by setting the
    corresponding properties of the actor via RenderPointsAsSpheresOn() and
    RenderLinesAsTubesOn().

    """
    # Input arrays need to have the same shape
    if not np.shape(X) == np.shape(Y) == np.shape(Z):
        sys.exit('X, Y, Z dimension mismatch!')

    # Check input parameters
    if not (isinstance(width, int) or isinstance(width, float)):
        sys.exit('width needs to be a single scalar value!')

    if not (isinstance(size, int) or isinstance(size, float)):
        sys.exit('size needs to be a single scalar value!')

    if not np.shape(color) == (3,):
        sys.exit('expected a single RGB triplet for color specification!')

    # From now on we work with flattened arrays
    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)

    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    verts = vtk.vtkCellArray()
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])
        vert = vtk.vtkIdList()
        vert.InsertNextId(int(i))
        verts.InsertNextCell(vert)

    # Create lines joining points with index i and i+1
    lines = vtk.vtkCellArray()
    for i in range(len(X)-1):
        line = vtk.vtkIdList()
        line.InsertNextId(int(i))
        line.InsertNextId(int(i+1))
        lines.InsertNextCell(line)

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)

    if ('o' in style) or ('.' in style): polyData.SetVerts(verts)
    if ('-' in style) or ('=' in style): polyData.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)
    actor.GetProperty().SetLineWidth(width)
    actor.GetProperty().SetPointSize(size)
    actor.GetProperty().SetColor(color[0], color[1], color[2])

    if 'o' in style: actor.GetProperty().SetRenderPointsAsSpheres(True)
    if '=' in style: actor.GetProperty().SetRenderLinesAsTubes(True)

    add(actor)
    return actor


def box(bb_min, bb_max, color=(0.8, 0.8, 0.8)):
    """ Bounding box.

    Covenience function that displays an axis aligned box with given corner
    vertices.

    Parameters
    ----------
    bb_min : array_like
        Lower left corner of the box.
    bb_max : array_like
        Upper right corner of the box.

    Returns
    -------
    vtkActor
        The corresponding actor object.

    """
    cube = vtk.vtkCubeSource()
    cube.SetBounds(bb_min[0], bb_max[0],
                   bb_min[1], bb_max[1],
                   bb_min[2], bb_max[2])
    cube.Update()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cube.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)
    actor.GetProperty().SetColor(color[0], color[1], color[2])
    actor.GetProperty().SetOpacity(0.25)
    actor.GetProperty().SetEdgeVisibility(True)
    actor.GetProperty().SetLineWidth(2.0)

    add(actor)
    return actor


def cube(xdim, ydim, zdim):
    """ A cube.

    Convenience function to create an axis aligned cube of given dimensions.
    Upon creation the cube is directly added to the scene.

    Parameters
    ----------
    xdim : (float, float)
        Cube dimension in x-direction.
    ydim : (float, float)
        Cube dimension in y-direction.
    zdim : (float, float)
        Cube dimension in z-direction.

    Returns
    -------
    vtkActor
        The corresponding actor.
    """
    V = [[xdim[0], ydim[0], zdim[0]],
         [xdim[1], ydim[0], zdim[0]],
         [xdim[1], ydim[0], zdim[1]],
         [xdim[0], ydim[0], zdim[1]],
         [xdim[0], ydim[1], zdim[0]],
         [xdim[1], ydim[1], zdim[0]],
         [xdim[1], ydim[1], zdim[1]],
         [xdim[0], ydim[1], zdim[1]]]

    F = [[0, 1, 2, 3],
         [1, 5, 6, 2],
         [3, 2, 6, 7],
         [7, 6, 5, 4],
         [3, 7, 4, 0],
         [0, 4, 5, 1]]

    obj = mesh((V,F))
    obj.SetPickable(False)
    obj.GetProperty().SetEdgeVisibility(True)
    obj.GetProperty().SetLineWidth(2.0)

    return obj


def _sphere(c, r):
    """
    """



def _stroke(X, Y, Z, I, J, K, width=1.0, size=1.0, col=[1.0, 1.0, 1.0]):
    """
    """
    # Input arrays need to have the same shape
    if not np.shape(X) == np.shape(Y) == np.shape(Z): raise ValueError()
    if not np.shape(I) == np.shape(J) == np.shape(K): raise ValueError()
    if not np.shape(X) == np.shape(I): raise ValueError()

    # Check input parameters
    if not (isinstance(width, int) or isinstance(width, float)): raise ValueError()
    if not (isinstance(size,  int) or isinstance(size,  float)): raise ValueError()
    if not np.shape(col) == (3,): raise ValueError()

    # From now on we work with flattened arrays
    X, Y, Z = np.ravel(X), np.ravel(Y), np.ravel(Z)
    I, J, K = np.ravel(I), np.ravel(J), np.ravel(K)

    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    verts = vtk.vtkCellArray()
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])
        vert = vtk.vtkIdList()
        vert.InsertNextId(int(2*i))
        verts.InsertNextCell(vert)

        points.InsertNextPoint(I[i], J[i], K[i])
        vert = vtk.vtkIdList()
        vert.InsertNextId(int(2*i+1))
        verts.InsertNextCell(vert)

    # Create lines joining points with index 2i and 2i+1
    lines = vtk.vtkCellArray()
    for i in range(len(X)):
        line = vtk.vtkIdList()
        line.InsertNextId(int(2*i))
        line.InsertNextId(int(2*i+1))
        lines.InsertNextCell(line)

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    # polyData.SetVerts(verts)
    polyData.SetLines(lines)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(width)
    actor.GetProperty().SetPointSize(size)
    actor.GetProperty().SetColor(col[0], col[1], col[2])

    add(actor)
    return actor


def _quiverXYZ(X, Y, Z, U, V, W, scale=1.0, col=[1.0, 1.0, 1.0]):
    """ Quiver plot.

    Display arrows at (x,y,z) locations pointing in direction (u,v,w).
    Scale and color can be a single value that is applied globally or
    on a per arrow basis. In the latter case there needs to be exactly
    one value per point/arrow.

    Parameters
    ----------
    X, Y, Z, U, V, W : array_like
        Points (x,y,z) and directions (u,v,w). All arrays needs to have
        the same shape.
    scale : array_like
        Scale of the displayed arrow. Either one scalar or one scalar per
        arrow.
    col : array_like
        Color specification. Either one RGB triplet or one triplet per
        arrow.
    """
    if not np.shape(X) == np.shape(Y) == np.shape(Z) == np.shape(U):
        msg = 'quiver(): X, Y, Z, U, V, W dimension mismatch!'
        raise ValueError(msg)

    if not np.shape(U) == np.shape(V) == np.shape(W):
        msg = 'quiver(): X, Y, Z, U, V, W dimension mismatch!'
        raise ValueError(msg)

    if isinstance(scale, int) or isinstance(scale, float):
        scale = np.tile(scale, np.shape(X))

    if np.shape(scale) != np.shape(X):
        msg = 'quiver(): input array size mismatch'
        raise ValueError(msg)

    # Size check for color specification ...
    if np.shape(col) != (3,):
        col_shape = list(np.shape(col))
        if col_shape[-1] != 3:
            sys.exit('RGB triplets expected as entries of the last axis')

        pts_shape = list(np.shape(X))
        pts_shape.append(3)
        if col_shape != pts_shape:
            sys.exit('Array size mismatch!')
    else:
        col_shape = list(np.shape(X))
        col_shape.append(1)
        col = np.tile(col, col_shape)

    # From now on we work with flattened arrays
    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)
    U = np.ravel(U)
    V = np.ravel(V)
    W = np.ravel(W)
    S = np.ravel(scale)
    C = np.reshape(np.ravel(col), (-1, 3))

    # Build the vtk representation of the point cloud
    points = vtk.vtkPoints()
    verts = vtk.vtkCellArray()
    vectors = vtk.vtkFloatArray()
    vectors.SetNumberOfComponents(3)
    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName('glyph_scale')
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName('glyph_color')
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])
        vert = vtk.vtkIdList()
        vert.InsertNextId(i)
        verts.InsertNextCell(vert)
        vectors.InsertNextTuple3(U[i], V[i], W[i])
        scalars.InsertNextTuple1(S[i])
        colors.InsertNextTuple3(255*C[i][0], 255*C[i][1], 255*C[i][2])

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetVerts(verts)
    polyData.GetPointData().SetVectors(vectors)
    polyData.GetPointData().AddArray(scalars)
    polyData.GetPointData().AddArray(colors)
    polyData.GetPointData().SetActiveScalars('glyph_scale')

    # The source shape used for glyphs. If rendering is too slow when there
    # is a large number of glyphs, the resolution of each can be reduced.
    arrow = vtk.vtkArrowSource()
    arrow.SetTipRadius(1.75*arrow.GetShaftRadius())
    arrow.SetTipLength(0.5)
    arrow.SetTipResolution(10)
    arrow.SetShaftResolution(10)

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(arrow.GetOutputPort())
    glyph.OrientOn()
    glyph.SetVectorModeToUseVector()
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SetColorModeToDirectScalars()
    mapper.ScalarVisibilityOn()
    mapper.SelectColorArray('glyph_color')

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetPickable(False)

    add(actor)
    return actor


def _quiverd(X, Y, Z, U, V, W, scale=1.0, col=[1.0, 1.0, 1.0]):
    """
    Quiver disk plot.

    Display disk at (x,y,z) locations orthogonal to direction (u,v,w).
    Scale and color can be a single value that is applied globally or
    on a per disk basis. In the latter case there needs to be exactly
    one value per point/disk.

    Parameters
    ----------
    X, Y, Z, U, V, W : array_like
        Points (x,y,z) and directions (u,v,w). All arrays needs to have
        the same shape.
    scale : array_like
        Scale of the displayed disk. Either one scalar or one scalar per
        disk.
    col : array_like
        Color specification. Either one RGB triplet or one triplet per
        disk.
    """
    # Input arrays need to have the same shape
    if not np.shape(X) == np.shape(Y) == np.shape(Z) == np.shape(U):
        sys.exit('X, Y, Z, U, V, W dimension mismatch!')

    if not np.shape(U) == np.shape(V) == np.shape(W):
        sys.exit('X, Y, Z, U, V, W dimension mismatch!')

    # size needs to be a scalar ...
    if isinstance(scale, int) or isinstance(scale, float):
        scale = np.tile(scale, np.shape(X))

    # ... or a matrix/array of scalars of the same shape as X etc.
    if np.shape(scale) != np.shape(X):
        sys.exit('Array size mismatch!')

    # Size check for color specification ...
    if np.shape(col) != (3,):
        col_shape = list(np.shape(col))
        if col_shape[-1] != 3:
            sys.exit('RGB triplets expected as entries of the last axis')

        pts_shape = list(np.shape(X))
        pts_shape.append(3)
        if col_shape != pts_shape:
            sys.exit('Array size mismatch!')
    else:
        col_shape = list(np.shape(X))
        col_shape.append(1)
        col = np.tile(col, col_shape)

    # From now on we work with flattened arrays
    X = np.ravel(X)
    Y = np.ravel(Y)
    Z = np.ravel(Z)
    U = np.ravel(U)
    V = np.ravel(V)
    W = np.ravel(W)
    S = np.ravel(scale)
    C = np.reshape(np.ravel(col), (-1, 3))

    # Build the vtk representation of the point cloud
    points = vtk.vtkPoints()
    verts = vtk.vtkCellArray()
    vectors = vtk.vtkFloatArray()
    vectors.SetNumberOfComponents(3)
    scalars = vtk.vtkFloatArray()
    scalars.SetNumberOfComponents(1)
    scalars.SetName('glyph_scale')
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName('glyph_color')
    for i in range(len(X)):
        points.InsertNextPoint(X[i], Y[i], Z[i])
        vert = vtk.vtkIdList()
        vert.InsertNextId(i)
        verts.InsertNextCell(vert)
        vectors.InsertNextTuple3(U[i], V[i], W[i])
        scalars.InsertNextTuple1(S[i])
        colors.InsertNextTuple3(255*C[i][0], 255*C[i][1], 255*C[i][2])

    # Create a polydata to store everything in
    polyData = vtk.vtkPolyData()
    polyData.SetPoints(points)
    polyData.SetVerts(verts)
    polyData.GetPointData().SetVectors(vectors)
    polyData.GetPointData().AddArray(scalars)
    polyData.GetPointData().AddArray(colors)
    polyData.GetPointData().SetActiveScalars('glyph_scale')

    # The source shape used for glyphs. If rendering is too slow when there
    # is a large number of glyphs, the resolution of each can be reduced.
    disk = vtk.vtkDiskSource()
    disk.SetInnerRadius(0.0)
    disk.SetOuterRadius(1.0)
    disk.SetCircumferentialResolution(50)

    xform = vtk.vtkTransform()
    xform.Identity()
    xform.RotateY(90.0)

    glyph = vtk.vtkGlyph3D()
    glyph.SetInputData(polyData)
    glyph.SetSourceConnection(disk.GetOutputPort())
    glyph.SetSourceTransform(xform)
    glyph.OrientOn()
    glyph.SetVectorModeToUseVector()
    glyph.ScalingOn()
    glyph.SetScaleModeToScaleByScalar()

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(glyph.GetOutputPort())
    mapper.SetScalarModeToUsePointFieldData()
    mapper.SetColorModeToDirectScalars()
    mapper.ScalarVisibilityOn()
    mapper.SelectColorArray('glyph_color')

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    add(actor)
    return actor


def _display(message):
    """ Display static text in the render window.

    Parameters
    ----------
    message : str
        The message to be displayed.

    Returns
    -------
    ret : vtkActor2D
        The corresponding text actor.
    """
    global _splash
    _splash += message

    textProp = vtk.vtkTextProperty()
    textProp.SetFontSize(12)
    textProp.SetFontFamilyToCourier()
    textProp.BoldOn()
    textProp.SetBackgroundColor(vtk.util.colors.black)
    textProp.SetBackgroundOpacity(0.0)
    textProp.FrameOff()
    textProp.ItalicOff()
    textProp.ShadowOn()
    textProp.SetVerticalJustificationToTop()

    textMapper = vtk.vtkTextMapper()
    textMapper.SetInput(_splash)
    textMapper.SetTextProperty(textProp)

    textActor = vtk.vtkActor2D()
    textActor.SetMapper(textMapper)
    textActor.GetPositionCoordinate().SetCoordinateSystemToNormalizedDisplay()
    textActor.GetPositionCoordinate().SetValue(0.05, 0.95)

    add(textActor)
    return textActor


def _annotate(point, string, size=1.0, color=(0.25, 0.25, 0.25)):
    """ Display 3D text annotation.

    Puts the given text at a certain location such that it always faces the
    camera.

    Parameters
    ----------
    point : array_like
        3D text location.
    string : str
        The text to be displayed.
    size : float, optional
        Size of the text.
    color : array_like, optional
        RGB triplet of color intensities.

    Returns
    -------
    vtkFollower
        The corresponding actor.
    """
    vecText = vtk.vtkVectorText()
    vecText.SetText(string)

    textMapper = vtk.vtkPolyDataMapper()
    textMapper.SetInputConnection(vecText.GetOutputPort())

    textActor = vtk.vtkFollower()
    textActor.SetMapper(textMapper)
    textActor.SetPosition(point[0], point[1], point[2])
    textActor.SetScale(size, size, size)
    textActor.SetPickable(False)
    textActor.GetProperty().SetColor(color[0], color[1], color[2])

    add(textActor)
    textActor.SetCamera(_renderer[-1].GetActiveCamera())
    _renderer[-1].ResetCamera()
    return textActor


def _caption(p, s, size=1.0, col=[1.0, 1.0, 1.0]):
    """
    """
    textActor = vtk.vtkCaptionActor2D()
    textActor.SetAttachmentPoint(p)
    textActor.SetCaption(s)
    textActor.SetBorder(False)
    textActor.SetThreeDimensionalLeader(True)
    textActor.SetPosition(10.0, 10.0)
    textActor.SetWidth(0.02)
    textActor.SetHeight(0.04)
    textActor.SetPadding(0)
    textActor.GetProperty().SetColor(vtk.util.colors.yellow_light)
    # textActor.GetProperty().SetLineWidth(4)

    textProp = textActor.GetCaptionTextProperty()
    textProp.SetBackgroundColor(vtk.util.colors.black)
    textProp.SetBackgroundOpacity(0.5)

    add(textActor)
    return textActor


def show(width=1200, height=600, title='geopy', **kwargs):
    """ Start the VTK event loop.

    Opens a window for rendering and starts the VTK event loop.

    Parameters
    ----------
    width : int, optional
        Window width in pixels.
    height : int, optional
        Window height in pixels.
    title : str, optional
        Window title.

    Keyword Arguments
    -----------------
    LMBDown : list[callable]
        Left button press callbacks.
    RMBDown : list[callable]
        Right button press callbacks.
    KEYDown : list[callable]
        Key press callbacks.
    LMBUp : list[callable]
        Left button release callbacks.
    RMBup : list[callable]
        Right button release callbacks.
    KEYUp : list[callable]
        Key release callbacks.
    MMove : list[callable]
        Mouse move callbacks.

    Raises
    ------
    RuntimeError
        When there is an active render window from a previous call.


    This is a blocking function, i.e., a script will not advance beyond this
    function until the event loop is stopped, i.e., the render window is
    closed. Interaction with the scene and displayed objects has to be
    triggered by mouse and keyboard events and corresponding event handlers.

    A callback function has to be declared in the following way:

        .. py:function:: callback(iren, x, y, **kwargs)

           Signature of a generic callback function.

           :param iren: Identifies the render window.
           :type iren: vtkRenderWindowInteractor
           :param x: Display coordinates of the mouse cursor.
           :type x: int
           :param y: Display coordinates of the mouse cursor.
           :type y: int

           :kwarg vtkActor obj: The active actor object.
           :kwarg int pid: The active point identifier.
           :kwarg ndarray p3d: Current world coordinates of the active point.

           When activated the callback receives a handle to the affected
           render window via the corresponding render window interactor
           ``iren`` as well as the mouse cursor postition inside this
           windows in pixels.

           The ``iren`` argument can be used to query the status of
           modifier keys via ``GetShiftKey()``, ``GetAltKey()``, and
           ``GetControlKey()``.

           During point dragging callbacks receive the listed additional
           keyword arguments.

    Note
    ----
    Object attributes can be used as callbacks. An object itself can be used
    as callback when it implements a ``__call__`` method.


    More than one callback can be registered to the same event. In this
    case callbacks are executed in the given order. The following events
    are recognized:

       Mouse events
          Left and right mouse button press and release events as well as
          mouse move events. Assign callbacks to the arguments ``LMBDown``,
          ``LMBUp``, ``RMBDown``, ``RMBUp``, and ``MMove``.

       Keyboard events
          Key press and release events. Assign callbacks to the arguments
          ``KEYDown`` and ``KEYUp``.


    .. literalinclude:: ../../examples/vtk_callback.py
       :lines: 8-
    """
    # Global state variables that are modified in this function. Should
    # be reset when show() terminates.
    global _renderer
    global _render_window

    # This method should only be called once. It can be called again in
    # a script if the active window has been closed.
    if _render_window is not None:
        msg = ('show(): active render window found -- this method ' +
               'should only be called once!')
        raise RuntimeError(msg)

    # Create a window, set its size and title. Multisampling is turned
    # off because of transparent objects.
    _render_window = vtk.vtkRenderWindow()
    _render_window.SetSize(width, height)
    _render_window.SetWindowName(title)
    _render_window.SetMultiSamples(0)
    _render_window.SetAlphaBitPlanes(1)

    # Allows us to interact with/modity the scene/camera.
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(_render_window)

    # Create a viewport that spans the entire render window if none
    # has been created so far.
    if not len(_renderer):
        canvas(0.0, 0.0, 1.0, 1.0)

    # Attach renderers to window. Each renderer is responsible for a
    # viewport inside the main render window.
    for ren in _renderer:
        _render_window.AddRenderer(ren)

    _render_window.Render()

    # Custom trackball mouse interactor style.
    irenStyle = MouseInteractorStyle(**kwargs)

    # Axes display in the lower left corner of each viewport. Only
    # shown in the active viewport, i.e., the one with mouse focus.
    axes = vtk.vtkAxesActor()
    widget = irenStyle._axes_widget
    widget.SetOrientationMarker(axes)
    widget.SetCurrentRenderer(_renderer[-1])
    widget.SetInteractor(iren)
    widget.SetViewport(0.0, 0.0, 0.2, 0.2)
    widget.SetEnabled(1)
    widget.InteractiveOff()

    # This automatically switches to trackball camera mode
    iren.SetInteractorStyle(irenStyle)
    iren.Initialize()

    # Print version information and some basic keyboard shortcuts to interact
    # with the scene.
    info = (vtk.vtkVersion.GetVTKSourceVersion() + '\n\n' +
        '--- Viewer commands ---\n' +
        ' e/q  quit\n' +
        ' p    perform pick\n' +
        ' f    fly to picked point\n' +
        ' r    reset/view all\n' +
        ' s/w  toggle surface/wireframe display\n\n')
    print(info)
    # display(info)

    # Start the event loop... the function returns when the render window
    # is closed.
    iren.Start()

    # This is helpful in an interactive sessions in IPython. Also allows us
    # to call show() more than once in a script.
    _render_window = None
    _renderer.clear()


def pick(x, y, *args, **kwargs):
    """ Perform pick action.

    Performs a pick operation at certain display coordinates. Cell and point
    picking is supported.

    Parameters
    ----------
    x : int
        Pick position in display coordinates.
    y : int
        Pick position in display coordinates.
    *args
        Additional arguments that determine the type of the pick action.
        Values other than ``'point'`` or ``'cell'`` have no effect.
    **kwargs
        Additional keyword arguments. This is only a place holder.

    Returns
    -------
    actor : vtkActor
        Results in :py:obj:`None` if nothing was picked.
    cell_id : int
        Numerical cell identifier. Results in ``-1`` if no cell was picked.
        Only returned when ``'cell'`` is specified.
    point_id : int
        Numerical point identifier. Results in ``-1`` if no point was picked.
    point : ndarray
        World coordinates of the picked point. Only meaningful if an actor
        was picked.


    By default all render objects created by functions in this module are not
    pickable. To make an actor available for picking its ``SetPickable()``
    method needs to be called with argument :py:obj:`True`.

    A successful pick operation returns the picked actor and information about
    the picked cell or point, respectively.

    .. literalinclude:: ../../examples/vtk_point_pick.py
       :lines: 8-


    When picking cells the coordinates of the intersection of the pick ray
    and the picked cell is returned in ``point``. In addition to the index
    ``cell_id`` of the picked cell, the index of the closest vertex of the
    picked cells to this location is also returned in ``point_id``.

    .. literalinclude:: ../../examples/vtk_cell_pick.py
       :lines: 8-
    """
    # Get the viewport that corresponds to the given location. What happens
    # if window coordinates are out of bounds?
    ren = _render_window.GetInteractor().FindPokedRenderer(x, y)

    if 'point' in args:
        picker = vtk.vtkPointPicker()
        picker.Pick(x, y, 0, ren)

        # The pick was successful, i.e., an actor was intersected with the
        # pick ray if the actor is valid.
        return (picker.GetActor(),
                picker.GetPointId(), np.array(picker.GetPickPosition()))

    if 'cell' in args:
        picker = vtk.vtkCellPicker()
        picker.Pick(x, y, 0, ren)

        # The pick was successful, i.e., an actor was intersected with the
        # pick rays if the actor is valid.
        return (picker.GetActor(), picker.GetCellId(),
                picker.GetPointId(), np.array(picker.GetPickPosition()))


class MouseInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    """ Trackball camera interactor style.

    Interactor style that supports point dragging on right mouse button
    clicks. An actor needs to be pickable for this feature to work,
    see an actor's ``SetPickable()`` method inherited from ``vtkProp``.

    Once an actor is pickable, it has control over which of its points may be
    dragged interactively by setting the attribute ``draggable_points`` to
    hold the identifiers of all draggable points. All points are considered
    draggable if this attribute is not provided.

    During vertex dragging all callbacks receive three additional keyword
    arguments ``obj``, ``pid``, and ``p3d`` that identify the active actor,
    the index of the point currently being dragged, as well as its current
    position in world coordinates.
    """
    def __init__(self, **kwargs):
        """ Constructor.

        Initialize state variables and user defined callbacks for mouse
        and keyboard events. Callbacks should be registered when starting
        the event loop via :py:func:`~geopy.vis.show`.

        Keyword Arguments
        -----------------
        LMBDown : list[callable]
            Left button press callbacks.
        RMBDown : list[callable]
            Right button press callbacks.
        KEYDown : list[callable]
            Key press callbacks.
        LMBUp : list[callable]
            Left button release callbacks.
        RMBup : list[callable]
            Right button release callbacks.
        KEYUp : list[callable]
            Key release callbacks.
        MMove : list[callable]
            Mouse move callbacks.

        Note
        ----
        Multiple callbacks for the same type of event are invoked in the
        specified order. See :py:func:`show` for an example on how to define
        and use callback functions.
        """
        # Axes widget to visualize global orientation. Used by every viewport
        # of the same render window.
        self._axes_widget = vtk.vtkOrientationMarkerWidget()

        # Vertex dragging state. Set when the right mouse button is pressed.
        # Reset when the button is released.
        self._vertex_drag = False
        self._picked_fac = 1.0

        # User defined callbacks. Those callbacks are invoked in the order
        # they were passed.
        self._lmb_down_cbs   = kwargs['LMBDown'] if 'LMBDown' in kwargs else []
        self._lmb_up_cbs     = kwargs['LMBUp']   if 'LMBUp'   in kwargs else []
        self._rmb_down_cbs   = kwargs['RMBDown'] if 'RMBDown' in kwargs else []
        self._rmb_up_cbs     = kwargs['RMBUp']   if 'RMBUp'   in kwargs else []
        self._key_down_cbs   = kwargs['KEYDown'] if 'KEYDown' in kwargs else []
        self._key_up_cbs     = kwargs['KEYUp']   if 'KEYUp'   in kwargs else []
        self._mouse_move_cbs = kwargs['MMove']   if 'MMove'   in kwargs else []

        self.AddObserver("LeftButtonPressEvent",    self._lmb_down_event)
        self.AddObserver("LeftButtonReleaseEvent",  self._lmb_up_event)
        self.AddObserver("RightButtonPressEvent",   self._rmb_down_event)
        self.AddObserver("RightButtonReleaseEvent", self._rmb_up_event)
        self.AddObserver("KeyPressEvent",           self._key_down_event)
        self.AddObserver("KeyReleaseEvent",         self._key_up_event)
        self.AddObserver("MouseMoveEvent",          self._mouse_move_event)

    def _project(self, ren, x, y):
        """ Display to world coordinate projection.

        Helper function mainly used during vertex dragging. Relies on the
        value of :py:attr:`_picked_fac`.

        Parameters
        ----------
        ren : vtkRenderer
            The affected renderer or viewport.
        x : int
            Display x-coordinate.
        y : int
            Display y-coordinate.

        Returns
        -------
        ndarray
            World coordinates of the mapped point.

        Note
        ----
        Display coordinates are given in pixels and determine a point in the
        active render window.
        """
        # Convert from display to world coordinates. Pixel coordinates are
        # transformed to 3D world coordinates of the corresponding point on
        # the image plane.
        p2d = vtk.vtkCoordinate()
        p2d.SetCoordinateSystemToDisplay()
        p2d.SetValue(x, y)
        p2d = np.array(p2d.GetComputedWorldValue(ren))

        # Now apply the intercept theorem. Need the eye position for that.
        # If the scale factor is 1.0 the coordinates of the corresponding
        # point on the image plane are returned.
        eye = np.array(ren.GetActiveCamera().GetPosition())
        return eye + self._picked_fac*(p2d-eye)

    def _lmb_down_event(self, irenstyle, event):
        """ LMB down event handler.

        Dispatches left mouse button press events to user defined callbacks.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'LeftButtonPressEvent'``
        """
        # Get corresponding render window interactor and event location
        # in window coordinates.
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        # Broadcast the event to all user defined callbacks. During vertex
        # dragging additional arguments are broadcast to callbacks.
        if self._vertex_drag:
            for cb in self._lmb_down_cbs:
                cb(iren, x, y, event=event, obj=self._picked_obj,
                                            pid=self._picked_pid,
                                            p3d=self._picked_p3d)
        else:
            for cb in self._lmb_down_cbs:
                cb(iren, x, y, event=event)

        # Forward event to the standard event handler.
        self.OnLeftButtonDown()

    def _lmb_up_event(self, irenstyle, event):
        """ LMB up event handler.

        Dispatch left mouse button release events to user defined callbacks.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'LeftButtonReleaseEvent'``
        """
        # Get corresponding render window interactor and event location
        # in window coordinates.
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        # Broadcast the event to all user defined callbacks. During vertex
        # dragging additional arguments are broadcast to callbacks.
        if self._vertex_drag:
            for cb in self._lmb_up_cbs:
                cb(iren, x, y, event=event, obj=self._picked_obj,
                                            pid=self._picked_pid,
                                            p3d=self._picked_p3d)
        else:
            for cb in self._lmb_up_cbs:
                cb(iren, x, y, event=event)

        # Hand off to standard event handlers
        self.OnLeftButtonUp()

    def _rmb_down_event(self, irenstyle, event):
        """ RMB down event handler.

        Dispatch to user defined event callbacks. On a successful point pick
        action the interactor style changes to vertex dragging. This stops
        once the right mouse button is released.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'RightButtonPressEvent'``
        """
        # Get corresponding render window interactor, viewport and event
        # location in window coordinates.
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        # Get the affected viewport. Need it to perform a pick operation.
        ren = iren.FindPokedRenderer(x, y)

        # If we are not already vertex dragging we start vertex dragging.
        # There cannot be a right button press event in this state.
        if not self._vertex_drag:
            picker = vtk.vtkPointPicker()
            picker.Pick(x, y, 0, ren)
            obj = picker.GetActor()

            if obj is not None:
                # Check if we may drag the picked point. If the attribute is
                # not present all points can be dragged.
                pid = picker.GetPointId()

                try:
                    draggable = pid in obj.draggable_points
                except AttributeError:
                    draggable = True
                except TypeError:
                    draggable = False

                if draggable:
                    # The picked point set is reachable by the picked actor's
                    # mapper object.
                    mapper = picker.GetMapper()

                    # Enter vertex dragging state. Store all information as
                    # attributes of the interactor style object.
                    self._vertex_drag = True
                    self._picked_obj = obj
                    self._picked_pts = mapper.GetInput().GetPoints()

                    p2d = vtk.vtkCoordinate()
                    p2d.SetCoordinateSystemToDisplay()
                    p2d.SetValue(x, y)
                    p2d = np.array(p2d.GetComputedWorldValue(ren))
                    p3d = np.array(picker.GetPickPosition())

                    # Eye point position and scale factor derived from the
                    # intercept thoerem.
                    eye = np.array(ren.GetActiveCamera().GetPosition())
                    fac = np.linalg.norm(p3d-eye)/np.linalg.norm(p2d-eye)

                    # World space coordinates of the point on the image
                    # plane and of the picked point.
                    self._picked_p2d = p2d
                    self._picked_p3d = p3d
                    self._picked_pid = pid
                    self._picked_fac = fac

                    # Broadcast the event to all user defined callbacks.
                    # Pass extra vertex dragging related keyword arguments.
                    for cb in self._rmb_down_cbs:
                        cb(iren, x, y, event=event, obj=obj,
                                                    pid=pid,
                                                    p3d=p3d)

                    # Do not execute standard event handlers. This would
                    # interfere with vertex dragging behavior.
                    return

            # Broadcast the event to all user defined callbacks. This path
            # is taken if nothing was picked.
            for cb in self._rmb_down_cbs:
                cb(iren, x, y, event=event)

            # Forward events to the standard event handlers when we are not
            # in vertex drag mode.
            self.OnRightButtonDown()
        else:
            # This point should never be reached! If it happens events were
            # received from the window system in asynchronous order.
            msg = ('Right mouse button press event received before ' +
                   'it was released!')
            raise RuntimeError(msg)

    def _rmb_up_event(self, irenstyle, event):
        """ RMB up event handler.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'RightButtonReleaseEvent'``
        """
        # Get corresponding render window interactor and event location
        # in window coordinates.
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        # Get the affected viewport. Need it to perform a pick operation.
        ren = iren.FindPokedRenderer(x, y)

        # This is the final update of the position of actively dragged points
        # on mouse movement.
        if self._vertex_drag:
            p3d = self._project(ren, x, y)
            pid = self._picked_pid
            obj = self._picked_obj

            # An actor can provide a project method. This method acts as a
            # constraint during point dragging.
            try:
                p3d = np.asarray(obj.project(ren, pid, p3d))
            except AttributeError:
                pass

            # Update point location of the point in the corresponding point
            # set. Call .Modified() to queue render window update.
            self._picked_pts.SetPoint(pid, p3d[0], p3d[1], p3d[2])
            self._picked_pts.Modified()

            # Calling .Modified is not always enough. Nudge...
            ren.GetRenderWindow().Render()

            # Broadcast the event to all user defined callbacks with extra
            # vertex dragging keyword arguments.
            for cb in self._rmb_up_cbs:
                cb(iren, x, y, event=event, obj=obj, pid=pid, p3d=p3d)
        else:
            # Broadcast the event to all user defined callbacks. No extra
            # keyword arguments.
            for cb in self._rmb_up_cbs:
                cb(iren, x, y, event=event)

        # Leave vertex dragging mode and hand off to standard event handlers.
        # Reset the scale factor. The _project method will now map 2D window
        # coordinates to 3D image plane point coordinates.
        self._vertex_drag = False
        self._picked_obj = None
        self._picked_fac = 1.0

        # Hand off to the standard event handler.
        self.OnRightButtonUp()

    def _mouse_move_event(self, irenstyle, event):
        """ Mouse move event handler.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'MouseMoveEvent'``
        """
        # Get corresponding render window interactor, viewport and event
        # location in window coordinates.
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        # Get the affected viewport. Need it to perform a pick operation.
        ren = iren.FindPokedRenderer(x, y)

        # Make the axes widget jump to the active viewport. Does not work
        # without disabling and then enabling it again...
        if self._axes_widget.GetCurrentRenderer() != ren:
            self._axes_widget.SetEnabled(0)
            self._axes_widget.SetCurrentRenderer(ren)
            self._axes_widget.SetEnabled(1)

            # Nudge for render window update...
            ren.GetRenderWindow().Render()

        # Update the position of actively dragged points on mouse movement.
        # We are in this state as long as the right mouse button is down.
        if self._vertex_drag:
            p3d = self._project(ren, x, y)
            pid = self._picked_pid
            obj = self._picked_obj

            # An actor can provide a project method. This method acts as a
            # constraint during point dragging.
            try:
                p3d = np.asarray(obj.project(ren, pid, p3d))
            except AttributeError:
                pass

            # Update point location of the point in the corresponding
            # point set. Calling .Modified() seems not enough to update the
            # render window.
            self._picked_pts.SetPoint(pid, p3d[0], p3d[1], p3d[2])
            self._picked_pts.Modified()

            # Nudge for render window update...
            ren.GetRenderWindow().Render()

            # Broadcast the event to all user defined callbacks. Pass extra
            # keyword argument during vertex dragging.
            for cb in self._mouse_move_cbs:
                cb(iren, x, y, event=event, obj=obj, pid=pid, p3d=p3d)

            # Do not execute standard event handlers. They interfere with
            # vertex dragging behavior.
            return
        else:
            # Broadcast the event to all user defined callbacks. No extra
            # argument except event identifier.
            for cb in self._mouse_move_cbs:
                cb(iren, x, y, event=event)

        # Hand off to the standard event handler.
        self.OnMouseMove()

    def _key_down_event(self, irenstyle, event):
        """ Key press event handler.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'KeyPressEvent'``
        """
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        if self._vertex_drag:
            for cb in self._key_down_cbs:
                cb(iren, x, y, event=event, obj=self._picked_obj,
                                            pid=self._picked_pid,
                                            p3d=self._picked_p3d)
        else:
            for cb in self._key_down_cbs:
                cb(iren, x, y, event=event)

        self.OnKeyPress()

    def _key_up_event(self, irenstyle, event):
        """ Key release event handler.

        Parameters
        ----------
        irenstyle : vtkInteractorStyle
            The corresponding interactor style, same as ``self``.
        event : str
            String identifier of the event: ``'KeyReleaseEvent'``
        """
        iren = irenstyle.GetInteractor()
        x, y = iren.GetEventPosition()

        if self._vertex_drag:
            for cb in self._key_up_cbs:
                cb(iren, x, y, event=event, obj=self._picked_obj,
                                            pid=self._picked_pid,
                                            p3d=self._picked_p3d)
        else:
            for cb in self._key_up_cbs:
                cb(iren, x, y, event=event)

        self.OnKeyRelease()
