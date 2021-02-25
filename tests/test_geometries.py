#!/usr/bin/env python
import unittest

from hexmaplib import HexVector
from hexmaplib import TriangleGeometry, RectangleGeometry

"""
Geometries map the canonical triangular lattice to other numbering schemes
and back.
"""

class TestTriangleGeometry(unittest.TestCase):

    def test_constructor(self):

        tg0 = TriangleGeometry(HexVector.ORIGIN)
        

        f0 = tg0.togrid(HexVector.ORIGIN)
        self.assertEqual(f0, HexVector.ORIGIN, "togrid: identity")
        r0 = tg0.tomap(HexVector.ORIGIN)
        self.assertEqual(r0, HexVector.ORIGIN, "tomap: identity")

        #
        # Origin of the map is 0, -1 -> grid 0,0
        #
        tg1 = TriangleGeometry(HexVector(1, 1))
        f1 = tg1.togrid(HexVector(1, 1))
        self.assertEqual(f1, HexVector.ORIGIN)
        f2 = tg1.tomap(HexVector.ORIGIN)
        self.assertEqual(f2, HexVector(1, 1), "Not a good thing")

        f3 = tg1.togrid(HexVector(5, 8))
        self.assertEqual(f3, HexVector(4, 7))

class TestRectangleGeometry(unittest.TestCase):

    def test_constructor(self):

        rg0 = RectangleGeometry(HexVector.ORIGIN)

        f0 = rg0.togrid(HexVector.ORIGIN)
        self.assertEqual(f0, HexVector.ORIGIN)
        r0 = rg0.tomap(HexVector.ORIGIN)
        self.assertEqual(r0, HexVector.ORIGIN)

        f1 = rg0.togrid(HexVector(2,0))
        self.assertEqual(f1, HexVector(2, 1), "togrid bias = 1")
                         
                
if __name__ == "__main__":
    unittest.main()
