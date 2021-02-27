from .hexvector import HexVector

# ============================================================================
# Geometries transform the canonical triangular lattice to other forms and back
# ============================================================================

"""
All hexmaps are triangular tiling. [1] Adding a coordinate system means
assigning each node in the plan a location. Like any planar coordinate system
it takes two axes to define a point. Because the coordinate system has three
axes instead of two, the third is redundant, and dependent on the other two: 
(hz = hy - hx).

All of the possible coordinate systems assign a single unique value to each node
in the grid.  This means that any system can map to any other. The systems are
one-to-one and onto. [2].

Each Geometry object creates a mapping from the canonical triangular coordinate
system to a common alternate.  The 'forward' method transforms from grid to map
coordinates.  The 'reverse' function transforms from map to canonical grid
location.

Given a grid, each geometry object also provides placement of each node within
the grid. That is, it can report the distance of each node from the edge of the
grid in terms of HexVector and Tiles.

[1] https://en.wikipedia.org/wiki/Triangular_tiling
[2] https://mathbitsnotebook.com/Algebra2/Functions/FNOneOnto2.html
"""


class TriangleGeometry:
    """
    The Triangle geometry is the canonical one.  The only transformation
    applied is translation of each hex in relation to the origin.
    """

    def __init__(self, origin=HexVector.ORIGIN):
        """
        The triangle geometry is the Identity geometry.  It makes no change
        to the canonical triangle geometry
        """
        self._origin = origin

    def togrid(self, src):
        """
        Return the grid location of a map hex
        """
        return src - self._origin

    def tomap(self, dst):
        """
        Return the map location of a grid node
        """
        return dst + self._origin

class RectangleGeometry(TriangleGeometry):
    """
    Rectangle grids morph the triangle grid to force one "axis" to be 
    perpendicular to the other.  The adjustment is 1 for every 2 columns.
    """

    def togrid(self, src):
        """
        Transform the map coordinate to the canonical grid
        """
        normal = src - self._origin
        bias = int(normal.hx / 2)
        return HexVector(normal.hx, normal.hy + bias)

    def tomap(self, dst):
        """
        Transform a grid coordinate to the map location
        """
        bias = int(dst.hx / 2)
        return self._origin + HexVector(dst.hx, dst.hy - bias)


class HerringboneGeometry(TriangleGeometry):
    """
    Herringbone geometry is drawn with a hex with hx=0 in one upper corner
    and hy=0 in the other.  The hx=hy axis runs down the center spine of
    a rectangular grid. This means that unlike the triangle grid, the
    axes are at 120 degrees instead of 60.
    """

    def togrid(self, src):
        """
        TBD
        """
        return HexVector(-src.hz, src.hx)

    def tomap(self, src):
        """
        TBD
        """
        return HexVector(src.hy, src.hz)

