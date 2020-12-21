#!/usr/bin/env python

import unittest

from point import Point

class TestPoint(unittest.TestCase):

    # test constructor
    def test_constructor(self):

        # test default constructor
        p0 = Point()
        self.assertEqual(p0.x, 0)
        self.assertEqual(p0.y, 0)

        # test explicit constructor
        p1 = Point(-3, 2)
        self.assertEqual(p1.x, -3)
        self.assertEqual(p1.y, 2)
        

    # test string representation
    def test_str(self):
        # test converting a point to string
        p0 = Point(3, 5)
        self.assertEqual(str(p0), "3.000000,5.000000")

    def test_eq(self):
        p0 = Point()

        self.assertFalse(p0 == "not a point")

        p1 = Point()
        self.assertTrue(p0 == p1)

        p2 = Point(1, 3)
        p3 = Point(1, 3)
        p4 = Point(2, 3)
        p5 = Point(1, 4)

        self.assertTrue(p2 == p3)
        self.assertFalse(p2 == p4)
        self.assertFalse(p2 == p5)
        
    # test arithmetic methods
    # subtraction
    def test_sub(self):
        p0 = Point(4, 10)
        p1 = Point(2, 5)

        p2 = p0 - p1

        self.assertEqual(p2.x, 2)
        self.assertEqual(p2.y, 5)

    # addition
    def test_add(self):
        p0 = Point(6, 3)
        p1 = Point(4, 5)

        p2 = p0 + p1
        
        self.assertEqual(p2.x, 10)
        self.assertEqual(p2.y, 8)

    # multiplication (dot product)
    def test_mul(self):
        p0 = Point(2, 5)
        p1 = p0 * 3

        self.assertEqual(p1.x, 6)
        self.assertEqual(p1.y, 15)

    # test transformations
    # reflect (y mirror)
    @unittest.skip("test not implemented")
    def test_reflect(self):
        pass

    # rotate/swap coordinates
    @unittest.skip("test not implemented")
    def test_rotate(self):
        pass


if __name__ == "__main__":
    unittest.main()
