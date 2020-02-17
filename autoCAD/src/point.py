import math


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
