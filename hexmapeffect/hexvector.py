

class HexVector:
    """
    """
    def __init__(self, hx=0, hy=0):
        self._hx = hx
        self._hy = hy

    @property
    def hx(self):
        return self._hx

    @property
    def hy(self):
        return self._hy

    @property
    def hz(self):
        return self._hy - self._hx

    # comparison operators
    def __eq__(self, other):
        if isinstance(other, HexVector):
            return self._hx == other.hx and self._hy == other.hy
        return False

    def __ne__(self, other):
        if isinstance(other, HexVector):
            return self._hx != other.hx or self._hy != other.hy
        return True
    
HexVector.ORIGIN = HexVector()
