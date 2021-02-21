# ----------------------------------------------------------------------------
# Hex Map Geometry
# ----------------------------------------------------------------------------

class HexVector:
    """
    This class represents a single point on a hexmap or triangular tesselation
    """

    def __init__(self, hx = 0, hy = 0):
        self._hx = hx
        self._hy = hy

    def __str__(self):
        return "{},{}".format(self._hx, self._hy)

    def __repr__(self):
        return "<{},{}>".format(self._hx, self._hy)

    @property
    def hx(self):
        return self._hx

    @property
    def hy(self):
        return self._hy

    @property
    def hz(self):
        return self._hy - self._hx

    @property
    def swap(self):
        return HexVector(self._hy, self._hx)

    @property
    def length(self):
        """
        TBD
        """
        return max(abs(self._hx), abs(self._hy), abs(self.hz))

    # comparison operators
    def __eq__(self, other):
        if isinstance(other, HexVector):
            return self._hx == other.hx and self._hy == other.hy
        return False

    def __ne__(self, other):
        if isinstance(other, HexVector):
            return self._hx != other.hx or self._hy != other.hy
        return True

    def __add__(self, other):
        if isinstance(other, HexVector):
            return HexVector(self._hx + other.hx, self._hy + other.hy)
        raise ValueError("operand of HexVector addition must be a HexVector")

    def __sub__(self, other):
        if isinstance(other, HexVector):
            return HexVector(self._hx - other.hx, self._hy - other.hy)    
        raise ValueError("operand of HexVector addition must be a HexVector")

    def rotate(self, hextant):
        """
        TBD
        """
        # This can be made more efficient with a table lookup for a lambda
        h = hextant % 6
        if h == 0:
            return self
        return HexVector(-self.hz, self.hx).rotate(h - 1)

HexVector.ORIGIN = HexVector()
HexVector.UNIT = [
    HexVector(0, -1),
    HexVector(1, 0),
    HexVector(1, 1),
    HexVector(0, 1),
    HexVector(-1, 0),
    HexVector(-1, -1)
]
