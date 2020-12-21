#!/usr/bin/env python

import unittest

from hexvector import HexVector

class TestHexVector(unittest.TestCase):

    def test_constructor(self):

        h0 = HexVector()
        self.assertEqual(0, h0._hx)
        self.assertEqual(0, h0._hy)

        h1 = HexVector(3, 5)
        self.assertEqual(3, h1._hx)
        self.assertEqual(5, h1._hy)

    def test_hx(self):
        h0 = HexVector()
        self.assertEqual(0, h0.hx)

        h1 = HexVector(4, 6)
        self.assertEqual(4, h1.hx)

    def test_hy(self):
        h0 = HexVector()
        self.assertEqual(0, h0.hy)

        h1 = HexVector(4, 6)
        self.assertEqual(6, h1.hy)

    def test_hz(self):
        h0 = HexVector()
        self.assertEqual(0, h0.hz)

        h1 = HexVector(5, 9)
        self.assertEqual(4, h1.hz)
        
    # comparison operators
    def test_equal(self):
        h0 = HexVector()
        self.assertFalse("not a hexvector" == h0)
        self.assertFalse(h0 == "not a hexvector")

        h1 = HexVector()
        self.assertTrue(h0 == h1)

        h2 = HexVector(2, 3)
        h3 = HexVector(2, 3)
        self.assertTrue(h2 == h3)

        h4 = HexVector(2, 4)
        self.assertFalse(h2 == h4)
        
        h5 = HexVector(3, 3)
        self.assertFalse(h2 == h5)

    def test_not_equal(self):
        h0 = HexVector()
        self.assertTrue("not a hexvector" != h0)
        self.assertTrue(h0 != "not a hexvector")

        h1 = HexVector()
        self.assertFalse(h0 != h1)

        h2 = HexVector(2, 3)
        h3 = HexVector(2, 3)
        self.assertFalse(h2 != h3)

        h4 = HexVector(2, 4)
        self.assertTrue(h2 != h4)
        
        h5 = HexVector(3, 3)
        self.assertTrue(h2 != h5)

    # artithmetic operators
    def test_add(self):
        pass

    def test_sub(self):
        pass

    def test_mul(self):
        pass

    # Origin and Units
    
if __name__ == "__main__":
    unittest.main()
