#!/usr/bin/env python
import unittest

from hexmaplib import HexVector, Point
from hexmaplib import Canvas

class SvgMock:

    def __init__(self, width, height):
        self._dim = {
            'height': height,
            'width': width
        }

    def get(self, dim):
        return self._dim[dim]

    def unittouu(self, info):
        return info

class TestCanvas(unittest.TestCase):

    def setUp(self):

        self.svg = SvgMock(200, 300)

    def test_constructor(self):

        canvas = Canvas(self.svg, HexVector(6, 8))

    def test_size(self):

        svg = SvgMock(200, 300)
        canvas = Canvas(svg, HexVector(6, 8))

        self.assertEqual(200.0, canvas.size.x)
        self.assertEqual(300.0, canvas.size.y)

    def test_stroke_width(self):

        svg = SvgMock(300, 300)
        canvas = Canvas(svg, HexVector(6, 8), stroke_percent=0.05)

        self.assertEqual(canvas.stroke_width, 2.5)


    def test_tile_size(self):

        svg = SvgMock(300, 300)
        canvas = Canvas(svg, HexVector(6, 8), stroke_percent=0.05)

        ts = canvas.tile_size

        print(ts)
        
if __name__ == "__main__":
    unittest.main()
