
from hexvector import HexVector
from point import Point

class Hex:
    """
    This class represents a single hex. It is used to define the operations
    to locate and draw the contents of a hex location on a map
    """

    def __init__(self, location, hexmap):
        self.location = location # HexVector
        self.hexmap = hexmap

    @property
    def center(self):
        """
        Find the center point of this hex.
        Based on the location of the origin of the map and the displacement
        from that point.
        """
        hm = self.hexmap
        c = hm.center0 + Point(self.location.hx * hm.colstep,
                               self.location.hy * hm.hexheight)
        if self.location.hx % 2:
            c -= Point(0,hm.hexrise)

        return c

    @property
    def nodes(self):
        """
        Produce the set of points that represent the corners of this hex
        """
        return [v + self.center for v in self.hexmap.vertices]

    def draw(self):
        pass

    @property
    def dot(self):
        pass

    @property
    def outline(self):
        pass

    @property
    def vertices(self):
        pass

    @property
    def label(self):
        """
        Generate the label for a map
        """
        pass
