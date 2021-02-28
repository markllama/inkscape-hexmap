from .hexvector import HexVector
from .point import Point

# ============================================================================
# Grid classes
#   These generate a list of hexes in a specified shape
#   They can be re-mapped to different hex locationl labelling schemes
# ============================================================================
class RadialHexGrid:
    """
    A radial hex grid is a set of hex rings centered on the origin
    The size of a radial hex grid is specified in as the length of a HexVector
    """

    def __init__(self, size):
        """
        TBD
        """
        self._size = size

    @property
    def size(self):
        return self._size

    @property
    def _radius(self):
        """
        The radius of a radial hexgrid is the length of the size vector
        """
        return max(abs(self._size.hx), abs(self._size.hy))

    def column(self,hx):
        """
        Produce a list of the hexes in the indicated column
        """
        # column 0
        radius = self._radius
        min = -radius if hx < 0 else -radius + hx
        max = radius if hx > 0 else radius - hx
        for hy in range(min, max):
            yield HexVector(hx, hy)

    @property
    def hexes(self):
        """
        Produce a list of hexes in a radial map, ring by ring
        Take advantage of the rotational symmetry of the triangluar lattice
        """
        # column 0
        radius = self._radius
        
        # The first time, just give the center hex
        yield HexVector.ORIGIN
        
        # produce each ring, starting at the center
        for ring in range(1, radius + 1):
            # start at hextant 0 on the axis
            for step in range(0, ring):
                # step along the side
                h0 = HexVector(step, -ring + step)
                # produce this hex in each hextant
                for hextant in range(0, 6):
                    yield h0.rotate(hextant)

    @property
    def _rectheight(self):
        """
        TBD
        """
        return (self._radius * 4) - 2

    @property
    def _rectwidth(self):
        """
        TBD
        """
        return (self._radius * 6) - 2

    @property
    def _rectorigin(self):
        """
        TBD
        """
        return Point(self._rectwidth / 2,  self._rectheight / 2)
        
    def rectloc(self, loc):
        """
        Return the rectangular coordinate of the hex location in multiples
        of hexrun and hexrise.
        For a radial grid, the origin hex is in the center of the rectangular
        space.
        """
        return self._rectorigin + (Point(loc.hx, loc.hy) * Point(3, 2))


class RectangleHexGrid(RadialHexGrid):
    """
    TBD
    """

    def column(self,hx):
        """
        TBD
        """
        min = self._ybias(hx)
        for hy in range(min, min + self._size.hy):
            yield HexVector(hx, hy)

    @property
    def hexes(self):
        """
        """
        for hx in range(0, self._size.hx):
            min = hx % 2
            for hy in range(min, min + self._size.hy):
                yield HexVector(hx, hy)

    @property
    def _rectorigin(self):
        """
        TBD
        """
        return Point(1,  2)
