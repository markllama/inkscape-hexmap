class Point:
    """
    This class implements some simple vector algebra for cartesian coodinates
    Several methods assume an offset from the origin to represent
    a region with the origin at one corner.
    """

    def __init__(self, x, y):
        """
        Create a Point object with cartesian components
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        Convert a Point object to a string
        """
        return '%f,%f' % (self.x, self.y)

    # comparison operators
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other):
        if isinstance(other, Point):
            return self.x != other.x or self.y != other.y
        return True

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
        Cartesian dot-product of a vector and scalar value
        """
        if isinstance(k, Point):
            return Point(self.x * k.x, self.y * k.y)

        if isinstance(k, int) or isinstance(k, float):
            return Point(self.x * k, self.y * k)

        raise ValueError("point muliplier must be point or scalar")

    def __div__(self, k):
        """
        Inverse Cartesian dot-product of a vector and scalar value
        """
        if isinstance(k, Point):
            return Point(self.x / k.x, self.y / k.y)

        if isinstance(k, int) or isinstance(k, float):
            return Point(self.x / k, self.y / k)

        raise ValueError("point muliplier must be point or scalar")

    @property
    def swap(self):
        """
        Swap the X and Y coordinates
        """
        return Point(self.y, self.x)
