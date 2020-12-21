import math

from hex import Hex
from hexvector import HexVector
from point import Point

class HexMap:
    """
    This class represents an entire hexagonal map
    """

    def __init__(self, size, origin, hexrun=15, rotate=False):

        self.size = size
        self.origin = origin
        self._hexrun = hexrun
        self.rotate = rotate

        self._hexrise = hexrun * 1.7321

    @property
    def hexrun(self):
        return self._hexrun

    @property
    def hexside(self):
        return self._hexrun * 2

    @property
    def colstep(self):
        return self._hexrun * 3
    
    @property
    def hexwidth(self):
        return self._hexrun * 4

    @property
    def hexrise(self):
        return self._hexrise

    @property
    def hexheight(self):
        return self._hexrise * 2

    @property
    def vertices(self):
        """
        Return the set of points offset from the center of a hex that represent
        the vertices of a hex.
        """
        return [
            Point(-self.hexrun, -self.hexrise),
            Point(self.hexrun, -self.hexrise),
            Point(self.hexside, 0),
            Point(self.hexrun, self.hexrise),
            Point(-self.hexrun, self.hexrise),
            Point(-self.hexside, 0)
        ]
    
    @property
    def labelsize(self):
        """
        Determine the size of the text labels for each hex
        Return them as a (col,row) tuple
        """
        
        coldigits = nrdigits(self.size.hx + self.origin.hx)
        rowdigits = nrdigits(self.size.hy + self.origin.hy)
        # Require minimum text width
        if coldigits < 2:
            coldigits = 2
        if rowdigits < 2:
            rowdigits = 2

        return (coldigits, rowdigits)

    @property
    def hexes(self):
        """
        A generator that iterates over all of the hexes in the map
        """
        for col in range(self.size.hx + 1):
            for row in range(self.size.hy + 1):
                yield Hex(HexVector(col, row), self)

    @property
    def center0(self):
        """
        Hex(0, 0) has a fixed place on the SVG map
        """
        return Point(self.hexside, self.hexheight)
        
        
def nrdigits(f):
    """
    Return the number of digits in an integer
      Negative numbers get another
    """
    fill = 1 if f >= 0.0 else 2
    return int(math.floor(math.log10(abs(f)))) + fill
