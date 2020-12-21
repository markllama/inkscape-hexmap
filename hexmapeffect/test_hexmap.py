#!/bin/env python
import unittest

from hexvector import HexVector
from hexmap import HexMap

class TestHexMap(unittest.TestCase):
    """
    TBD
    """

    def setUp(self):
        self.hm_size = HexVector(15, 22)
        self.hm_origin = HexVector(0, 0)
        
    def test_constructor(self):
        """
        TBD
        """

        hm = HexMap(self.hm_size, self.hm_origin)

        self.assertEqual(hm.size, self.hm_size)
        self.assertEqual(hm.origin, self.hm_origin)
        self.assertEqual(hm.hexrun, 15)


    def test_hex_dimensions(self):
        hm = HexMap(self.hm_size, self.hm_origin)
        self.assertEqual(hm.hexside, hm.hexrun * 2)
        self.assertEqual(hm.hexwidth, hm.hexside * 2)

        self.assertEqual(hm.hexrise, 25.9815)
        self.assertEqual(hm.hexheight, hm.hexrise * 2)


    def test_hex0_center(self):
        hm = HexMap(self.hm_size, self.hm_origin)

        c0 = hm.center0

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
    
