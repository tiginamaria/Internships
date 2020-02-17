import math

from autoCAD.src.point import Point


class Side(object):
    """ Creates a point on a coordinate plane with values x and y. """

    def __init__(self, a: Point, b: Point):
        """ Defines x and y variables. """
        self.a = a
        self.b = b

    def s_prod(self, other):
        p1, p2 = self.to_zero(), other.to_zero()
        return p1.x * p2.x + p1.y * p2.y

    def length(self):
        p = self.to_zero()
        return math.sqrt(p.x ** 2 + p.y ** 2)

    def sqr_length(self):
        p = self.to_zero()
        return p.x ** 2 + p.y ** 2

    def to_zero(self):
        return Point(self.a.x - self.b.x, self.a.y - self.b.y)
