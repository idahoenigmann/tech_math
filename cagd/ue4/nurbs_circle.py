import numpy as np
from geomdl import NURBS
from geomdl import utilities
from geomdl.visualization import VisMPL

# https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline

if __name__ == '__main__':
    ctrlpts = [[1.0, 0.0],
               [1.0, 1.0],
               [0.0, 1.0],
               [-1.0, 1.0],
               [-1.0, 0.0],
               [-1.0, -1.0],
               [0.0, -1.0],
               [1.0, -1.0],
               [1.0, 0.0]]

    curve = NURBS.Curve()

    curve.degree = 2
    curve.ctrlpts = ctrlpts

    curve.weights = [1, np.sqrt(2)/2, 1, np.sqrt(2)/2, 1, np.sqrt(2)/2, 1, np.sqrt(2)/2, 1]
    curve.knotvector = [0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4]
    # curve.knotvector = utilities.generate_knot_vector(curve.degree, curve.ctrlpts_size)

    # Set evaluation delta
    curve.delta = 0.01

    # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
    vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)

    # Create a visualization method instance using the configuration above
    vis_obj = VisMPL.VisCurve2D(vis_config)

    # Set the visualization method of the curve object
    curve.vis = vis_obj

    # Plot the curve
    curve.render()
