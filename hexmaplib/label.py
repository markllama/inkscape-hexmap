class HexLabel:
    """
    This class represents and draws a hex coordinate label
    """

    def __init__(self, hextile, edge='interior'):
        self._hextile = hextile
        self._edge = edge

    def draw(self, loc, font_size, anchor='middle'):
        label = etree.Element('text')

        label.text = str(self._hextile)

        # Set the fond and drawing characteristics
        style = ('text-align:center;text-anchor:%s;font-size:%fpt'
                 % (anchor, font_size))
        label.set('style', style)

        label.set('x', str(loc.x))
        label.set('y', str(loc.y))

        return label
