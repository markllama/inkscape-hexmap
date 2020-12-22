#!/bin/env python
import unittest

from hexvector import HexVector
from hexgrid import HexGrid

class TestHexGrid(unittest.TestCase):
    """
    TBD
    """

    def setUp(self):
        self.hg_size = HexVector(15, 22)
        self.hg_origin = HexVector(0, 0)
        
    def test_constructor(self):
        """
        TBD
        """

        hg = HexGrid(self.hg_size, self.hg_origin)

        self.assertEqual(hg.size, self.hg_size)
        self.assertEqual(hg.origin, self.hg_origin)
        self.assertEqual(hg.hexrun, 15)


    def test_hex_dimensions(self):
        hg = HexGrid(self.hg_size, self.hg_origin)
        self.assertEqual(hg.hexside, hg.hexrun * 2)
        self.assertEqual(hg.hexwidth, hg.hexside * 2)

        self.assertEqual(hg.hexrise, 25.9815)
        self.assertEqual(hg.hexheight, hg.hexrise * 2)


    def test_hex0_center(self):
        hg = HexGrid(self.hg_size, self.hg_origin)

        c0 = hg.center0

        self.assertEqual(c0.x, 30)
        self.assertEqual(c0.y, 51.963)
        
    def test_vertices(self):
        pass

    def test_labelsize(self):
        pass

    def test_hexes(self):
        pass

if __name__ == "__main__":
    unittest.main()
    
