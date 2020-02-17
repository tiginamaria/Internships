from autoCAD.src.constants import EPSILON
from autoCAD.src.point import Point
from autoCAD.src.side import Side


class Triangle(object):
    """ Creates a point on a coordinate plane with values x and y. """

    def __init__(self, a: Point, b: Point, c: Point):
        """ Defines x and y variables. """
        self.points = [a, b, c]
        self.sides = [Side(a, b), Side(b, c), Side(c, a)]

    def cosine(self, side1, side2):
        return side1.s_prod(side2) / side1.length() / side2.length()

    def cosines(self):
        a, b, c = self.points
        return [self.cosine(Side(a, b), Side(a, c)),
                self.cosine(Side(b, a), Side(b, c)),
                self.cosine(Side(c, b), Side(c, a))]

    def is_valid_triangle(self):
        ab, bc, ca = map(lambda side: side.length(), self.sides)
        return ab + bc + EPSILON > ca and \
               ab + ca + EPSILON > bc and \
               bc + ca + EPSILON > ab

    def is_equilateral(self):
        ab, bc, ca = map(lambda side: side.length(), self.sides)
        return abs(ab - bc) < EPSILON and \
               abs(ab - ca) < EPSILON and \
               abs(bc - ca) < EPSILON

    def is_acute(self):
        return min(self.cosines()) > 0

    def is_obtuse(self):
        return min(self.cosines()) <= 0
