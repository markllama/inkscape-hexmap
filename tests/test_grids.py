#!/usr/bin/env python

import unittest

from hexmaplib import HexVector, Point
from hexmaplib import RadialHexGrid, RectangleHexGrid

class TestRadialHexGrid(unittest.TestCase):

    def test_contructor(self):

        radial0 = RadialHexGrid(HexVector(3,0))

        self.assertEqual(len(list(radial0.hexes)), 37)
#        print(list(rg0.hexes))

    def test_radius(self):

        radial0 = RadialHexGrid(HexVector(3,0))
        self.assertEqual(radial0._radius, 3)
        
    def test_rectwidth(self):
        
        radial0 = RadialHexGrid(HexVector(3,0))
        self.assertEqual(radial0._rectwidth, 16)

    def test_rectheight(self):
        radial0 = RadialHexGrid(HexVector(3,0))
        self.assertEqual(radial0._rectheight, 10)

    def test_rectorigin(self):
        radial0 = RadialHexGrid(HexVector(3,0))
        self.assertEqual(radial0._rectorigin, Point(8,5))

    def test_rectloc(self):
        radial0 = RadialHexGrid(HexVector(3,0))
        self.assertEqual(radial0.rectloc(HexVector.ORIGIN), Point(8,5))

        # check x multiples
        self.assertEqual(radial0.rectloc(HexVector(-2, 0)),
                         Point(2, radial0._rectorigin.y))
        self.assertEqual(radial0.rectloc(HexVector(2, 0)),
                         Point(radial0._rectwidth-2, radial0._rectorigin.y))

        # check y multiples
        self.assertEqual(radial0.rectloc(HexVector(0, -2)),
                         Point(radial0._rectorigin.x, 1))
        self.assertEqual(radial0.rectloc(HexVector(0, 2)),
                         Point(radial0._rectorigin.x, radial0._rectheight-1))
        
class TestRectangleHexGrid(unittest.TestCase):

    def test_constructor(self):

        rect0 = RectangleHexGrid(HexVector(6, 8))
        self.assertEqual(len(list(rect0.hexes)), 48)

if __name__ == "__main__":
    unittest.main()
