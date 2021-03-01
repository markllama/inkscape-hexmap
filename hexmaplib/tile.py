from lxml import etree

from .point import Point

class Tile:
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
        place the tile on a canvas.
        center and size are in convas units
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
        
    def draw(self, stroke, orientation, border='solid', tic_size=0.25, dot=True):
        """
        Draw the complete hex

        Border (solid, corners)
        Center
        Label
        """

        group = etree.Element('g')
        group.set('style', 'stroke:#cccccc; stroke-width:'
                  + str(stroke) + ';stroke-linecap:round')

        v = self.vertices(orientation)
        if border == 'solid':
            group.append(self._polyline(v))
        elif border == 'vertex':
            for t in self._tics(v, tic_size):
                group.append(t)
            
        # or append corners
        # Append dots
        if (dot and self._side in ['interior', 'top', 'bottom']):
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


class BrickTile(Tile):
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
