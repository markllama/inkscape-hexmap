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
        'radial': RadialHexGrid,
        'megahex': MegahexGrid,
    }

    _geometries = {
        'triangle': TriangleGeometry,
        'rectangle': RectangleGeometry,
        'herringbone': HerringboneGeometry
    }


    def _add_map_parser(self):
        """
        add Map dimension and layout arguments
        """
        map_parser = self.arg_parser.add_argument_group("map parameters")
        map_parser.add_argument('--shape', choices = ['rectangle', 'radial', 'megahex'],
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

        gridorigin = HexVector(self.options.origin_hx, self.options.origin_hy)
        gridsize = HexVector(self.options.size_hx, self.options.size_hy)
        grid = HexmapEffect._grids[self.options.shape](gridsize)
        geometry = HexmapEffect._geometries[self.options.geometry](gridorigin, gridsize)
        hexcanvas = Canvas(svg, grid.size,
                           stroke_percent=self.options.strokewidth / 100)
        # TBD - check the value of the grid selection

        # --------------------------------------------------------------------
        #
        # --------------------------------------------------------------------

        tilesize = hexcanvas.tile_size
        tilestep = hexcanvas.tile_step
        padding = hexcanvas.padding
        stroke_width = hexcanvas.stroke_width
        # adjust for the thickness of the border line drawing
        line_pack = Point(stroke_width * 3, 0)

        # draw all of the hexes in the grid
        for gridloc in grid.hexes:

            # get the placement of the tile from the geometry
            maploc = geometry.tomap(gridloc)
            # get the location of that placement from the canvas
            
            # multiply that by the tile step and add the padding
            center = (grid.rectloc(maploc) * tilestep) + padding - line_pack
            tile = Tile(center, tilesize)
            layer.append(tile.draw(
                hexcanvas.stroke_width,
                self.options.orientation,
                self.options.border_style,
                self.options.tic_size / 100,
                self.options.center_dot
            ))
            if self.options.label:
                label = HexLabel(geometry.togrid(gridloc), 'interior')
                layer.append(label.draw(tile.label_center, tilesize.y/5))

# ============================================================================
#
# After defining everything, make it go
#
# ============================================================================
HexmapEffect().run()
