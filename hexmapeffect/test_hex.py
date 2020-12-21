#!/usr/bin/env python

import unittest

from lxml import etree

from point import Point
from hexvector import HexVector
from hexmap import HexMap
from hex import Hex


class TestHex(unittest.TestCase):

    def setUp(self):
        self.hsize = HexVector(15, 22)
        self.horigin = HexVector(0,0)

        self.hexrun = 50
        self.hexrise = self.hexrun * 1.7321
        self.hm = HexMap(self.hsize, self.horigin, hexrun=self.hexrun)
        
    def test_constructor(self):
        h0 = Hex(HexVector(0, 0), self.hm)

        self.assertEqual(h0.location, HexVector.ORIGIN)
        self.assertEqual(h0.hexmap, self.hm)


    def test_center(self):
        h0 = Hex(HexVector(0, 0), self.hm)
        c0 = h0.center

        self.assertIsInstance(c0, Point)
        self.assertEqual(c0.x, self.hexrun * 2)
        self.assertEqual(c0.y, self.hexrise * 2)

        h1 = Hex(HexVector(1, 0), self.hm)
        c1 = h1.center
        self.assertEqual(c1.x, self.hexrun * 5)
        self.assertEqual(c1.y, self.hexrise)

        h2 = Hex(HexVector(2, 0), self.hm)
        c2 = h2.center
        self.assertEqual(c2.x, self.hexrun * 8)
        self.assertEqual(c2.y, self.hexrise * 2)

        h3 = Hex(HexVector(0, 1), self.hm)
        c3 = h3.center
        self.assertEqual(c3.x, self.hexrun * 2)
        self.assertEqual(c3.y, self.hexrise * 4)

        h4 = Hex(HexVector(1, 1), self.hm)
        c4 = h4.center
        self.assertEqual(c4.x, self.hexrun * 5)
        self.assertEqual(c4.y, self.hexrise * 3)


    def test_nodes(self):

        h0 = Hex(HexVector(0, 0), self.hm)
        c0 = h0.center
        v0 = h0.nodes

        self.assertEqual(len(v0), 6)

        self.assertEqual(v0[0].x, self.hexrun)
        self.assertEqual(v0[0].y, self.hexrise)


    def test_draw(self):
        pass

    def test_label(self):
        pass

    def test_border(self):
        pass

    @unittest.skip("not implemented")
    def test_dot(self):
        """
        Return an SVG circle around the center of the hex
        """
        h0 = Hex(HexVector(0, 0), self.hm)
        center_dot = h0.dot

        self.assertIsInstance(center_dot, etree._Element)

    
if __name__ == "__main__":
    unittest.main()
