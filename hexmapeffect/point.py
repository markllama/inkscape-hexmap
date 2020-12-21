#!/bin/env python

class Point:
    """
    This class represents a location or a vector on a cartesian plane.
    The methods are all transformations within the cartesian plane.
    """
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        if isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        return True

    def __str__(self):
        return '%f,%f' % (self.x, self.y)

    def __sub__(self, other):
        """
        Cartesian vector subtraction
        """
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """
        Cartesian vector addition
        """
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        """
        Cartesian dot-product
        """
        return Point(self.x * k, self.y * k)

    def y_mirror(self, h=0):
        """
        Reflect about the Y axis, offset by h
        """
        return Point(self.x, h - self.y);

    def rotated(self, total_width):
        """
        Cartsian rotation - 90 degrees clockwise, sort of
        """
        return Point(self.y, total_width - self.x)
