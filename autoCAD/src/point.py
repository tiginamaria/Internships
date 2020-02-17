import math

from autoCAD.src.constants import EPSILON


class Point(object):
    """ Creates a point on a coordinate plane with values x and y. """

    def __init__(self, x, y):
        """ Defines x and y variables. """
        self.x = x
        self.y = y

    def dist(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def sqr_dist(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def __eq__(self, other):
        return abs(self.x - other.x) < EPSILON and abs(self.y - other.y) < EPSILON

    def __str__(self):
        return "(%.6f, %.6f)" % (self.x, self.y)

    def __repr__(self):
        return "(%.6f, %.6f)" % (self.x, self.y)
