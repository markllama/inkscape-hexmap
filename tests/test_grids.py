#!/usr/bin/env python

import unittest

from hexmaplib import HexVector
from hexmaplib import RadialHexGrid, RectangleHexGrid

class TestRadialHexGrid(unittest.TestCase):

    def test_contructor(self):

        radial0 = RadialHexGrid(HexVector(3,0))

        self.assertEqual(len(list(radial0.hexes)), 37)
#        print(list(rg0.hexes))

class TestRectangleHexGrid(unittest.TestCase):

    def test_constructor(self):

        rect0 = RectangleHexGrid(HexVector(6, 8))
        self.assertEqual(len(list(rect0.hexes)), 48)

if __name__ == "__main__":
    unittest.main()
