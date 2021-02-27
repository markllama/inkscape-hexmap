#!/usr/bin/env python
import unittest

from hexmaplib import HexVector
from hexmaplib import TriangleGeometry, RectangleGeometry, HerringboneGeometry

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

        m0 = HexVector(-5, 2)
        self.assertEqual(m0, tg0.togrid(m0))
        self.assertEqual(m0, tg0.tomap(m0))
        
        #
        # Origin of the map is 0, -1 -> grid 0,0
        #
        tg1 = TriangleGeometry(HexVector(1, 1))
        m1 = HexVector(1, 1)
        g1 = HexVector.ORIGIN
        self.assertEqual(tg1.togrid(m1), g1)


        m3 = HexVector(5, 8)
        g3 = HexVector(4, 7)
        self.assertEqual(tg1.togrid(m3), g3)
        self.assertEqual(tg1.tomap(g3), m3)


class TestRectangleGeometry(unittest.TestCase):

    def test_constructor(self):

        rg0 = RectangleGeometry(HexVector.ORIGIN)

        self.assertEqual(rg0.togrid(HexVector.ORIGIN), HexVector.ORIGIN)
        self.assertEqual(rg0.tomap(HexVector.ORIGIN), HexVector.ORIGIN)

        m0 = HexVector(5,0)
        g0 = HexVector(5,2)
        self.assertEqual(rg0.togrid(m0), g0)
        self.assertEqual(rg0.tomap(g0), m0)

        m1 = HexVector(8, 14)
        g1 = HexVector(8, 18)
        self.assertEqual(rg0.togrid(m1), g1)
        self.assertEqual(rg0.tomap(g1), m1)


        origin1 = HexVector(9, 14)
        m2 = HexVector(15, 22)
        g2 = HexVector(6, 11)
        rg1 = RectangleGeometry(origin1)
        
        self.assertEqual(rg1.togrid(m2), g2)
        self.assertEqual(rg1.tomap(g2), m2)
        
class TestHerringboneGeometry(unittest.TestCase):

    def test_constructor(self):

        hb0 = HerringboneGeometry(HexVector.ORIGIN)

        self.assertEqual(HexVector.ORIGIN, hb0.togrid(HexVector.ORIGIN),
                         "identity: togrid")
        self.assertEqual(HexVector.ORIGIN, hb0.tomap(HexVector.ORIGIN),
                         "identity: tomap")

        # pick a map hex:
        m1 = HexVector(3, 4)
        g1 = HexVector(-1, 3)
        self.assertEqual(g1, hb0.togrid(m1), "herringbone: togrid")
        self.assertEqual(m1, hb0.tomap(g1), "herringbone: tomap")


        # make sure that the transforms are reversable
        m2 = HexVector(9,4)
        g2 = HexVector(5, 9)
        self.assertEqual(g2, hb0.togrid(m2), "herringbone: togrid")
        self.assertEqual(m2, hb0.tomap(g2), "herringbone: tomap")

        # Try again just because
        m3 = HexVector(-4, 1)
        g3 = HexVector(-5, -4)
        self.assertEqual(g3, hb0.togrid(m3), "herringbone: togrid")
        self.assertEqual(m3, hb0.tomap(g3), "herringbone: tomap")
                
if __name__ == "__main__":
    unittest.main()
