import inkex

class Effect(inkex.Effect):
    """
    TBD
    """
    
    def __init__(self):
        """
        TBD
        """
        inkex.Effect.__init__(self)

        p = self.arg_parser

        p.add_argument("--size-hx", type=int, default=15)
        p.add_argument("--size-hy", type=int, default=22)

        p.add_argument("--origin-hx", type=int, default=0)
        p.add_argument("--origin-hy", type=int, default=0)

        p.add_argument("--orientation",
                       choices=['vertical', 'horizontal'],
                       default='vertical')
        p.add_argument("--coordinate-system",
                       choices=['rectangle', 'triangle', 'vee'],
                       default='rectangle')
        p.add_argument("--wrap", type=inkex.Boolean, default=False)
        p.add_argument("--mirror", type=inkex.Boolean, default=False)
        p.add_argument("--colshift", type=inkex.Boolean, default=False)

        p.add_argument("--hexshape",
                       choices=['hex', 'brick', 'square'],
                       default='hex')
        p.add_argument("--border",
                       choices=['solid', 'vertices', 'fill', 'none'],
                       default='solid')
        p.add_argument("--borderwidth", type=float, default=1.0)
        p.add_argument("--units",
                       choices=['mm', 'cm', 'in', 'pt', 'px'],
                       default='mm')

        p.add_argument("--vertex-size", type=int, default=10)

        p.add_argument("--dots", type=inkex.Boolean, default=True)
        p.add_argument("--dot-size", type=int, default=5)

        p.add_argument("--label", type=inkex.Boolean, default=True)
        p.add_argument("--label-grouping",
                       choices=['parentheses', 'brackets', 'braces', 'none'],
                       default='none')
        p.add_argument("--label-swap", type=inkex.Booean, default=False)
        p.add_argument("--label-zeros", type=inkex.Boolean, default=False)
        p.add_argument("--label-letters", type=inkex.Boolean, default=False)

        p.add_argument("--log", type=inkex.Boolean, default=False)
        p.add_argument("--log-path", default='debug.txt')

    def effect(self):
        """
        TBD
        """
        pass
