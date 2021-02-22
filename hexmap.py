#!/usr/bin/env python3

import inkex
import sys
from inkex import NSS
import math
from lxml import etree

from hexmaplib import *


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

    def __init__(self, size, origin=HexVector.ORIGIN):
        """
        TBD
        """
        self._size = size
        self._origin = origin

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
            yield HexVector(hx, hy) + self._origin

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

    _grids = {
        'rectangle': RectangleHexGrid,
        'radial': RadialHexGrid
    }

    _geometries = {
        'triangle': HexGridTriangle,
        'rectangle': HexGridRectangle,
        'herringbone': HexGridHerringbone
    }

    @property
    def map_spec(self):
        """
        Collect the map parameters for easy access
        """
        # TBD - check the value of the grid selection
        grid = HexmapEffect._grids[self.options.shape](
            HexVector(self.options.size_hx, self.options.size_hy))

        geometry = HexmapEffect._geometries[self.options.geometry](
            HexVector(self.options.size_hx, self.options.size_hy))

        spec = {
            'geometry': geometry,
            'grid': grid,
            'orientation': self.options.orientation, # or horizontal
            'pad': self.options.pad,
            'tile_size': self.options.hexsize,
            'tile_shape': self.options.tileshape,
            'border_style': self.options.border_style,
            'tic_size': self.options.tic_size / 200,  # 1/2 of a percentage
            'center_dot': self.options.center_dot,
            'label': self.options.label,
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
        map_parser.add_argument('--shape', choices = ['rectangle', 'radial'],
                                default = 'rectangle',
                                help = "Hexmap Shape")
        map_parser.add_argument('--geometry',
                                choices = ['rectangle', 'triangle', 'herringbone'],
                                default = 'rectangle',
                                help = "Hexmap Coordinate System")
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
                                choices = ['solid', 'vertex', 'none'],
                                default = 'solid',
                                help = 'How to draw the hex border: solid or vertices')
        map_parser.add_argument('--tic-size', type = int, default = '25',
                                help = 'Size of corner tics in % of side')
        map_parser.add_argument('--center-dot', type = inkex.Boolean,
                                default = True,
                                help = "Draw a dot at the center of each hex")
        map_parser.add_argument('--label', type = inkex.Boolean,
                                default = True,
                                help = "Label each hex")
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

            #if shift:
            edge = hexcanvas.grid.edge(hexloc)
            # else: edge = 'interior'

            tile = HexTile(center, tilesize, edge)
            layer.append(tile.draw(
                hexcanvas.stroke_width,
                hexcanvas._spec['orientation'],
                hexcanvas._spec['border_style'],
                hexcanvas._spec['tic_size'],
                hexcanvas._spec['center_dot']
            ))
            if self.options.label:
                label = HexLabel(hexloc, edge)
                layer.append(label.draw(tile.label_center, tilesize.y/5))

# ============================================================================
#
# After defining everything, make it go
#
# ============================================================================
HexmapEffect().run()
