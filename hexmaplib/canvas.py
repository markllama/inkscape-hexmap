#
#
#
from .point import Point
from .hexvector import HexVector

class Canvas:
    """
    A Canvas is an extension of an SVG object that is tuned to place objects
    in a triangular tiling on a cartesian coordinate space.
    """


    def __init__(self, svg, gridsize, orientation="vertical", stroke_percent=0.05):
        self._svg = svg
        self._gridsize = gridsize
        self._orientation = orientation
        self._stroke_percent = stroke_percent

    @property
    def size(self):
        """
        Return the size of the svg canvas as a Point object
        """
        unit = self._svg.unittouu
        size = Point(float(unit(self._svg.get('width'))),
                     float(unit(self._svg.get('height'))))
        if self._orientation == 'horizontal':
            size = size.swap
        return size

    @property
    def stroke_width(self):
        """
        The width of lines drawn for borders and vertices.
        A percentage of the total width or height of a hex
        """
        csize = self.size
        # Define the stroke width as a percentage of the size of one hex
        if self._orientation == 'vertical':
            return (self._stroke_percent / float(self._gridsize.hx)) * csize.x
        else:
            return (self._stroke_percent / float(self._gridsize.hy)) * csize.y
            
    @property
    def tile_size(self):
        """
        Determine the hexrise and hexrun dimensions of a hex by fitting
        a hexgrid into the canvas dimensions.
        Hexes pack so that the columns are only 3/4 as wide as one hex
        dim.x = hexrun = hexside / 2 = hexwidth / 4
        dim.y = hexrise = hexheight / 2
        """
        # TODO - Adjust for brick and square tiles
        csize = self.size

        # hexrun is the basic dimension of a hex
        # it is 1/2 of a hexside and 1/4 of the longest 'diameter' of a hex
        hexrun = (csize.x - self.stroke_width) / ((self._gridsize.hx * 3) + 1)

        # The height of a hex is cos(pi/6) * the width
        # hexrise is 1/2 of a hex height
        hexrise = (hexrun * 2) * 0.8660254

        # TODO - check the canvas y as well and pick the smallest dimension
        #        that allows the entire hexgrid to pack within the canvas
        if hexrise * ((self._gridsize.hy * 2) + 1) > csize.y:
            hexrise = (csize.y - self.stroke_width) / ((self._gridsize.hy * 2) + 1)
            hexrun = hexrise / ( 2 * 0.8660254 )

        return Point(hexrun, hexrise)

    @property
    def tile_step(self):
        """
        TBD
        """
        return self.tile_size * Point(3, 2)

    @property
    def padding(self):
        """
        Determine how much space exists on the page outside the boundaries
        of the hex grid
        """

        # The size of one tile in svg canvas units
        tdim = self.tile_size

        # the size of the grid in tile units (hexrun,hexrise)
        hsize = (self._gridsize * HexVector(3, 2)) + HexVector(1, 1)
        
        # the size of the grid in canvas units
        msize = tdim * Point(hsize.hx, hsize.hy)

        # The amount of unused space on the canvas
        excess = self.size - msize

        # The amount of padding allowed to center the grid on the canvas
        pad = excess / 2

        return pad
