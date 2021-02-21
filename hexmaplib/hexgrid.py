# ============================================================================
# Combined grid and placement classes
# ============================================================================
class HexGridRectangle:
    """
    This class represents the descrete locations on a hexmap
    """

    def __init__(self, size, origin=HexVector.ORIGIN, shift=False):
        """
        TBD
        """
        self._size = size
        self._origin = origin
        self._shift = shift

    @property
    def size(self):
        return self._size

    @property
    def origin(self):
        return self._origin
    
    @property
    def hexes(self):
        """
        A generator that iterates over all of the hexes in the map
        """
        for col in range(0, self._size.hx):
            for row in range(0, self._size.hy):
                #location = HexVector(col, row
                yield HexVector(col, row) + self._origin

    def translate(self, hexloc):
        """
        Convert the hex location to units of hexrun and hexrise
        """
        # triangle
        #return Point(hexloc.hx, hexloc.hy - (hexloc.hx / 2))
        return Point(hexloc.hx, hexloc.hy - ((hexloc.hx % 2)/2))

    def ybias(self, col):
        """
        Adjust the set of rows to create a rectangular grid for drawing
        """
        # Adjust so negative columns are properly shifted
        c = col if col >= 0 else col - 1
        return int(c / 2)
    
    def edge(self, hexloc):
        """
        Determine if the hex is on an edge and if so, which one?
        """

        if self._shift is False:
            return 'interior'

        if (hexloc.hx - self._origin.hx) == 0:
            return 'left'
        elif self._size.hx - (hexloc.hx - self._origin.hx) == 1:
            return 'right'

        if (hexloc.hy - self._origin.hy) == 0:
            return 'top'
        elif self._size.hy - (hexloc.hy - self._origin.hy) == 1:
            return 'bottom'

        return 'interior'

class HexGridTriangle(HexGridRectangle):
    """
    TBD
    """

    @property
    def hexes(self):
        """
        A generator that iterates over all of the hexes in the map
        """
        for col in range(0, self._size.hx):
            ybias = self.ybias(col)
            for row in range(ybias, self._size.hy + ybias):
                yield HexVector(col, row) + self._origin

    def translate(self, hexloc):
        """
        Convert the hex location to units of hexrun and hexrise
        """
        # triangle
        return Point(hexloc.hx, hexloc.hy - (hexloc.hx /2))
    

class HexGridHerringbone(HexGridRectangle):
    @property
    def hexes(self):
        """
        A generator that iterates over all of the hexes in the map
        """
        col_start = self._origin.hx - int(self._size.hx / 2)
        col_end = col_start + self._size.hx
        for col in range(col_start, col_end):
            
            ybias = self.ybias(col)
            for row in range(ybias, self._size.hy + ybias):
                yield HexVector(col+row, row)

    def translate(self, hexloc):
        """
        Convert the hex location to units of hexrun and hexrise
        """
        # herringbone
        return Point(hexloc.hx - hexloc.hy, hexloc.hy + hexloc.hz/2)
