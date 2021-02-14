#!/usr/bin/env python3

import inkex
import sys
from inkex import NSS
import math
from lxml import etree


class Point:
    """
    This class implements some simple vector algebra for cartesian coodinates
    Several methods assume an offset from the origin to represent
    a region with the origin at one corner.
    """

    def __init__(self, x, y):
        """
        Create a Point object with cartesian components
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Convert a Point object to a string
        """
        return '%f,%f' % (self.x, self.y)

    def __sub__(self, other):
        """
        Cartesian vector subtraction
        """
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """
        Cartesian vector addition
        """
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        """
        Cartesian dot-product of a vector and scalar value
        """
        if isinstance(k, Point):
            return Point(self.x * k.x, self.y * k.y)

        if isinstance(k, int) or isinstance(k, float):
            return Point(self.x * k, self.y * k)

        raise ValueError("point muliplier must be point or scalar")

    @property
    def swap(self):
        """
        Swap the X and Y coordinates
        """
        return Point(self.y, self.x)

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

HexVector.ORIGIN = HexVector()


class HexTile:
    """
    TBD
    """

    # Indicate the multipliers for hexrun and hexrise

    _vertices = {}
    _vertices['interior'] = [
        Point(-2, 0),
        Point(-1, -1),
        Point(1, -1),
        Point(2, 0),
        Point(1, 1),
        Point(-1, 1),
        # Wrap back to close the polygon
        Point(-2, 0)
    ]
    _vertices['top'] = _vertices['interior'][0:4]
    _vertices['bottom'] = _vertices['interior'][3:7]
    _vertices['left'] = [
        Point(0, -1),
        Point(1, -1),
        Point(2, 0),
        Point(1, 1),
        Point(0, 1)        
    ]
    _vertices['right'] = [Point(-v.x, v.y) for v in _vertices['left']]

    def __init__(self, center, size, side='interior'):
        """
        TBD
        """
        self._center = center
        self._size = size
        self._side = side

    #@property
    def vertices(self, orientation):
        """
        6 vertices offset from center
        """
        # Scale the hex vertices
        points =  [ p * self._size for p in self._vertices[self._side]]

        # Rotate the vertices for horizontal
        if orientation == 'horizontal':
            points = [ p.swap for p in points ]

        # translate the vertices to the canvas location
        v = [ p + self._center for p in points ]
        
        return v

    @property
    def label_offset(self):
        """
        TBD
        """
        if self._side in ['interior', 'top', 'bottom']:
            offset = Point(0, (self._size.y * 0.75))
        elif self._side == 'left':
            offset = Point(self._size.x, 0)
        elif self._side == 'right':
            offset = Point(-self._size.x, 0)

        return offset

    @property
    def label_center(self):
        """
        TBD
        """

        c = self._center
        p = c + self.label_offset
        return p
        
    def draw(self, stroke, orientation, border='solid', tic_size=0.25):
        """
        Draw the complete hex

        Border (solid, corners)
        Center
        Label
        """

        group = etree.Element('g')
        group.set('style', 'stroke:#000000; stroke-width:'
                  + str(stroke) + ';stroke-linecap:round')

        v = self.vertices(orientation)
        if border == 'solid':
            group.append(self._polyline(v))
        else:
            for t in self._tics(v, tic_size):
                group.append(t)
            
        # or append corners
        # Append dots
        if self._side in ['interior', 'top', 'bottom']:
            c = self._center
            group.append(self._circle(stroke, c))

        return group

    def _circle(self, radius, loc=None):
        """
        Create an SVG Circle object with the indicated size
        """
        circle = etree.Element('circle')
        circle.set('r', str(radius))
        circle.set('fill', 'black')

        if loc is not None:
            circle.set('cx', str(loc.x))
            circle.set('cy', str(loc.y))
        return circle

    def _polyline(self, vertices):
        """
        TBD
        """
        pline = etree.Element('polyline')
        pline.set('fill', 'none')
        pline.set('points', ' '.join([str(p) for p in vertices]))
        return pline

    def _tics(self, vertices, tic_size=0.25):
        """
        Draw just corner tics for each vertex
        """
        # for each pair of points in the vertices list...
        tics = []
        for i in range(0, len(vertices) - 1):
        
            (start, end) = vertices[i:i+2]
            tic = (end - start) * tic_size
            # each pair of vertices, draw two tics, on from each vertex
            # toward the other
            t1 = [ start, start + tic ]
            tics.append(self._line(t1))
            t2 = [ end, end - tic ]
            tics.append(self._line(t2))

        return tics
        
    def _line(self, endpoints):
            line = etree.Element('line')
            (start, end) = endpoints
            line.set('x1', str(start.x))
            line.set('y1', str(start.y))
            line.set('x2', str(end.x))
            line.set('y2', str(end.y))

            return line


class BrickTile(HexTile):
    """
    TBD
    """
    _unit_vertices = [
        Point(-2, -1),
        Point(2, -1),
        Point(2, 1),
        Point(-2, -1)
    ]


class SquareTile(BrickTile):
    """
    TBD
    """
    _height_ratio = 1


class HexLabel:
    """
    This class represents and draws a hex coordinate label
    """

    def __init__(self, hextile, edge='interior'):
        self._hextile = hextile
        self._edge = edge

    def draw(self, loc, font_size, anchor='middle'):
        label = etree.Element('text')

        label.text = str(self._hextile)

        # Set the fond and drawing characteristics
        style = ('text-align:center;text-anchor:%s;font-size:%fpt'
                 % (anchor, font_size))
        label.set('style', style)

        label.set('x', str(loc.x))
        label.set('y', str(loc.y))

        return label


class HexGrid:
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
    def column(self, col):
        """
        """
        for row in range(self._size.hy):
            location = Hex
            yield HexVector(col, row)

    @property
    def hexes(self):
        """
        A generator that iterates over all of the hexes in the map
        """
        for col in range(self._origin.hx, self._size.hx + self._origin.hx):
            for row in range(self._origin.hy, self._size.hy + self._origin.hy):
                #location = HexVector(col, row
                yield HexVector(col, row)
        
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
    def grid(self):
        return self._spec['grid']

    @property
    def stroke_width(self):
        """
        TBD
        """
        csize = self.size
        if self._spec['orientation'] == 'vertical':
            return (self._spec['stroke_width'] / self.grid.size.hx) * csize.x
        else:
            return (self._spec['stroke_width'] / self.grid.size.hy) * csize.y
            
        #self.size.x / (self.grid.size.hx + (0.05 /self.grid.size.hx))

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
        origin = Point(offset_x, dim.y) + Point(self.stroke_width/2, self.stroke_width/2)
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
        dim = self.tile_size
        return Point(dim.x * 3, dim.y * 2)


    def tile_center(self, hexloc):
        """
        Find the center point of a tile on the grid
        Multiply the hexloc coords by the tile_step and add the tile_origin
        """
        # Convert the hexvector to a point
        normalized = hexloc - self.grid.origin
        multiplier = Point(normalized.hx, normalized.hy)
        coldown = 1 if self._spec['sawtooth'] else 0
        ybias = Point(0, ((hexloc.hx + coldown) % 2) * self.tile_size.y)
        # Calculate the center
        c = (multiplier * self.tile_step) + self.tile_origin + ybias
        if self._spec['orientation'] == 'horizontal':
            c = c.swap
        return c

# -------------------------------------------------------------------------
# Layer creation and management
# -------------------------------------------------------------------------

def append_if_new_name(svg, layer):
    if layer is not None:
        name = layer.get(inkex.addNS('label', 'inkscape'))
        if not name in [c.get(inkex.addNS('label', 'inkscape'), 'name')
                        for c in svg.iterchildren()]:
            svg.append(layer)

def createLayer(name):
    layer = etree.Element(inkex.addNS('g', 'svg'))
    layer.set(inkex.addNS('label', 'inkscape'), name)
    layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
    return layer

# ----------------------------------------------------------------------------
# Inkscape Hexmap Drawing
# ----------------------------------------------------------------------------

class HexmapEffect(inkex.Effect):
    """
    This class defines how to draw a hexmap in an Inkscape drawing.
    """

    def __init__(self):
        """
        Create a HexmapEffect object and define the CLI inputs that control
        the drawing.
        """
        inkex.Effect.__init__(self)

        self.arg_parser.add_argument('--tab')

        # Map Dimensions and layout
        self._add_map_parser()

        # Drawing Parameters
        draw_parser = self.arg_parser.add_argument_group("drawing parameters")
        draw_parser.add_argument("--units", default='mm',
                                 help="Units this dialog is using")
        # Hex size is calculated by default
        draw_parser.add_argument('--hexsize', type = float, default = 0.0)
        draw_parser.add_argument('--strokewidth', type = float, default = 2.5)

        # Label Spec and Layout
        self._add_label_parser()


# -----------------------------------------------------------------------------
# Argument Parser Groups
# -----------------------------------------------------------------------------
    @property
    def map_spec(self):
        """
        Collect the map parameters for easy access
        """
        grid = HexGrid(HexVector(self.options.size_hx, self.options.size_hy),
                       HexVector(self.options.origin_hx,self.options.origin_hy),
                       self.options.wrap_x)
        spec = {
            'grid': grid,
            'orientation': self.options.orientation, # or horizontal
            'pad': self.options.pad,
            'tile_size': self.options.hexsize,
            'tile_shape': self.options.tileshape,
            'border_style': self.options.border_style,
            'tic_size': self.options.tic_size / 200,  # 1/2 of a percentage
            'wrap_x': self.options.wrap_x,
            'wrap_y': self.options.wrap_y,
            'reverse_x': False,
            'reverse_y': False,
            'sawtooth': self.options.sawtooth,
            # drawing spec
            'units': self.options.units,
            'stroke_width': self.options.strokewidth / 100.0
        }

        return spec

    def _add_map_parser(self):
        """
        add Map dimension and layout arguments
        """
        map_parser = self.arg_parser.add_argument_group("map parameters")
        map_parser.add_argument('--size-hx', type = int, default = '10',
                                help = 'Number of columns')
        map_parser.add_argument('--size-hy', type = int, default = '10',
                                help = 'Number of rows')
        map_parser.add_argument('--origin-hx', type = int, default = '0',
                                help = 'Location of the first column')
        map_parser.add_argument('--origin-hy', type = int, default = '0',
                                help = 'Location of the first row')
        map_parser.add_argument('--orientation',
                                choices = ['vertical', 'horizontal'],
                                default = 'vertical',
                                help = 'Orientation of the x axis')
        map_parser.add_argument('--pad', type = inkex.Boolean,
                                default = True,
                                help = 'Pad and center the grid on the page')
        map_parser.add_argument('--wrap-x', type = inkex.Boolean,
                                default = False,
                                help = 'Shift grid half hex and wrap')
        map_parser.add_argument('--wrap-y', type = inkex.Boolean,
                                default = False,
                                help = 'Shift grid half hex and wrap')
        map_parser.add_argument('--reverse-x', type = inkex.Boolean,
                                default = False,
                                help = 'Number columns right to left')
        map_parser.add_argument('--reverse-y', type = inkex.Boolean,
                                default = False,
                                help = 'number rows from bottom to top')
        map_parser.add_argument('--sawtooth', type = inkex.Boolean,
                                default = False, dest='sawtooth',
                                help = 'First column half-hex down')
        map_parser.add_argument('--halfhexes', type = inkex.Boolean,
                                default = False)
        map_parser.add_argument('--tileshape',
                                choices = ['hex', 'brick', 'square'],
                                default = 'hex',
                                help = 'The shape for each tile in the map')
        map_parser.add_argument('--border-style',
                                choices = ['solid', 'vertex'],
                                default = 'solid',
                                help = 'How to draw the hex border: solid or vertices')
        map_parser.add_argument('--tic-size', type = int, default = '25',
                                help = 'Size of corner tics in % of side')
        
    @property
    def label_spec(self):
        """
        Collect label parameters for easy access
        """
        # determine the size of the label component fields
        hxdigits = nrdigits(self.options.size_hx + self.options.coordcolstart)
        hydigits = nrdigits(self.options.size_hy + self.options.coordrowstart)
        if hxdigits < 2:
            hxdigits = 2
        if hydigits < 2:
            hydigits = 2
        if self.coordrowfirst:
            hxdigits,hydigits = [hydigits,hxdigits]

        spec = {
            'seperator': self.options.coordseparator,
            'alphacolumn': self.options.coordalphacol,
            'zeropad': self.options.coordzeros,
            'invert': self.options.coordrowfirst,
            'hxdigits': hxdigits,
            'hydigits': hydigits
        }

        return spec

    def _add_label_parser(self):
        """
        Add hex label arguments
        """
        label_parser = self.arg_parser.add_argument_group("label parameters")
        label_parser.add_argument('--coordcolstart', type = int, default = '0')
        label_parser.add_argument('--coordrowstart', type = int, default = '0')
        label_parser.add_argument('--coordrows', type = int, default = '1')
        label_parser.add_argument('--coordseparator', type = str, default = ',')
        label_parser.add_argument('--coordalphacol', type = inkex.Boolean,
                                  default = False,
                                  help = 'Alpha Column Labels')
        label_parser.add_argument('--coordrevrow', type = inkex.Boolean,
                                  default = False, dest='label_reverse_y',
                                  help = 'Reverse row label coordinates')
        label_parser.add_argument('--coordzeros', type = inkex.Boolean,
                                  default = True,
                                  help = 'Pad coordinates with zeros')
        label_parser.add_argument('--coordrowfirst', type = inkex.Boolean,
                                  default = False,
                                  help = 'Row coordinate first in a label')


# ----------------------------------------------------------------------------
# The 'main' method for drawing the map
# ----------------------------------------------------------------------------

    def effect(self):

        # Define some local references to shorten later lines

        svg = self.document.xpath('//svg:svg' , namespaces=NSS)[0]
        layer = createLayer('hexmap')
        append_if_new_name(svg, layer)
        
        hexcanvas = HexCanvas(svg, self.map_spec)

        # --------------------------------------------------------------------
        #
        # --------------------------------------------------------------------

        tilesize = hexcanvas.tile_size
        tilestep = hexcanvas.tile_step

        # draw all of the hexes in the grid
        for hexloc in hexcanvas.grid.hexes:
            
            center = hexcanvas.tile_center(hexloc)
            edge = hexcanvas.grid.edge(hexloc)
            tile = HexTile(center, tilesize, edge)
            layer.append(tile.draw(
                hexcanvas.stroke_width,
                hexcanvas._spec['orientation'],
                hexcanvas._spec['border_style'],
                hexcanvas._spec['tic_size']
            ))
            label = HexLabel(hexloc, edge)
            layer.append(label.draw(tile.label_center, tilesize.y/5))

# ============================================================================
#
# After defining everything, make it go
#
# ============================================================================
HexmapEffect().run()
