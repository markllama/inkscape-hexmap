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


class HexCanvas:
    """
    Draw the tiles on the SVG document
    """

    def __init__(self, svg, map_spec):
        """
        Store and initialize the elements to draw the map
        """
        self._svg = svg
        self._spec = map_spec

    @property
    def size(self):
        """
        Return the size of the svg canvas as a Point object
        """
        unit = self._svg.unittouu
        size = Point(float(unit(self._svg.get('width'))),
                     float(unit(self._svg.get('height'))))
        if self._spec['orientation'] == 'horizontal':
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
        if self._spec['orientation'] == 'vertical':
            return (self._spec['stroke_width'] / self.grid.size.hx) * csize.x
        else:
            return (self._spec['stroke_width'] / self.grid.size.hy) * csize.y
            
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
        if self._spec['wrap_x']:
            hexrun = csize.x / ((self.grid.size.hx - 1) * 3)
        else:
            hexrun = (csize.x - self.stroke_width) / ((self.grid.size.hx * 3) + 1)

        # The height of a hex is cos(pi/6) * the width
        # hexrise is 1/2 of a hex height
        hexrise = (hexrun * 2) * 0.8660254

        # TODO - check the canvas y as well and pick the smallest dimension
        #        that allows the entire hexgrid to pack within the canvas
        if hexrise * ((self.grid.size.hy * 2) + 1) > csize.y:
            hexrise = (csize.y - self.stroke_width) / ((self.grid.size.hy * 2) + 1)
            hexrun = hexrise / ( 2 * 0.8660254 )

        return Point(hexrun, hexrise)

    @property
    def padding(self):
        """
        Determine how much space exists on the page outside the boundaries
        of the hex grid
        """
        tdim = self.tile_size
        if self._spec['wrap_x'] is False:
            msize = Point(tdim.x * ((self.grid.size.hx * 3) + 1),
                          tdim.y * ((self.grid.size.hy * 2) + 1))

        else:
            msize = Point(tdim.x * ((self.grid.size.hx - 1) * 3),
                          tdim.y * ((self.grid.size.hy * 2) + 1))

        s = self.size
        excess = (s - msize)
        pad = Point(excess.x / 2, excess.y / 2)

        return pad

    @property
    def tile_origin(self):
        """
        Find the center point of the origin tile on the canvas
        """
        dim = self.tile_size

        # offset to center the map on the page
        offset_x = 0 if self._spec['wrap_x'] else dim.x * 2
        origin = Point(offset_x, dim.y * 2) + Point(self.stroke_width/2, self.stroke_width/2)
        if self._spec['pad']:
            origin += self.padding
        return origin


    @property
    def tile_step(self):
        """
        This a vector where the two coordinates correspond to the
        horizontal and vertical distance between one hex and the next in
        each dimension
        """
        return self.tile_size * Point(3, 2)

    def tile_center(self, hexloc):
        """
        Find the center point of a tile on the grid
        Multiply the hexloc coords by the tile_step and add the tile_origin
        """
        # Convert the hexvector to a point
        normalized = hexloc - self.grid.origin
        c = self.tile_origin + (self.grid.translate(normalized) * self.tile_step)
        if self._spec['orientation'] == 'horizontal':
            c = c.swap
        return c

