import numpy as np
from mayavi import mlab

@mlab.show
def test_quiver3d(a, b, c):
    dphi, dtheta = np.pi/30.0, np.pi/30.0
    [phi,theta] = np.mgrid[0:np.pi+dphi*1.5:dphi, 0:2*np.pi+dtheta*1.5:dtheta]
    x = a * np.sin(phi) * np.cos(theta)
    y = b * np.sin(phi) * np.sin(theta)
    z = c * np.cos(phi)

    # outward pointing unit vectors
    u = x
    u = np.array([e / np.linalg.norm(e, ord=2) for e in u])
    v = y
    v = np.array([e / np.linalg.norm(e, ord=2) for e in v])
    w = z
    w = np.array([e / np.linalg.norm(e, ord=2) for e in w])

    obj = mlab.quiver3d(x, y, z, u, v, w, line_width=1, scale_factor=1)
    mlab.axes(obj)
    mlab.outline(obj)
    mlab.imshow(10)
    return obj


if __name__ == "__main__":
    test_quiver3d(5, 3, 6)
