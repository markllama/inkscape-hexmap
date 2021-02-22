#!/usr/bin/env python
import unittest

from hexvector import HexVector
from geometry import TriangleGeometry

"""
Geometries map the canonical triangular lattice to other numbering schemes
and back.
"""

class TestTriangleGeometry(unittest.TestCase):

    def test_constructor(self):

        tg0 = TriangleGeometry(HexVector.ORIGIN)
        

if __name__ == "__main__":
    unitttest.main()
