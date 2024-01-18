from geomdl import NURBS
from geomdl.visualization import VisMPL

# https://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node20.html

if __name__ == '__main__':
    a = 4.0
    b = 2.0

    ctrlpts_quarter = [[a, 0.0],
                       [a, b],
                       [0.0, b]]

    quarter_ellipse = NURBS.Curve()

    quarter_ellipse.degree = 2
    quarter_ellipse.ctrlpts = ctrlpts_quarter

    quarter_ellipse.weights = [1, 1, 2]
    quarter_ellipse.knotvector = [0, 0, 0, 1, 1, 1]

    # Set evaluation delta
    quarter_ellipse.delta = 0.01

    # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
    vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)

    # Create a visualization method instance using the configuration above
    vis_obj = VisMPL.VisCurve2D(vis_config)

    # Set the visualization method of the curve object
    quarter_ellipse.vis = vis_obj

    # Plot the curve
    quarter_ellipse.render()
