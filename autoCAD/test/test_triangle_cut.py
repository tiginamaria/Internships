import math
import unittest

from autoCAD.src.constants import DELTA, EPSILON
from autoCAD.src.point import Point
from autoCAD.src.side import Side
from autoCAD.src.triangle import Triangle
from autoCAD.src.triangle_cat import can_cut, get_cut_points, get_cuts
from autoCAD.src.visualizer import draw


class InterpreterTests(unittest.TestCase):

    def cos(self, v1, v2):
        return v1.s_prod(v2) / v1.length() / v2.length()

    def point_on_side(self, p, side):
        return abs(self.cos(side, Side(p, side.a)) + 1) < EPSILON

    def cut_cross_side_perpendicular(self, cut, side):
        return abs(self.cos(side, Side(cut[0], cut[1]))) < EPSILON

    def side_cross_cut_in_the_middle(self, p, cut):
        return abs(Side(p, cut[0]).length() - Side(p, cut[1]).length()) < EPSILON

    def cuts_do_not_cross(self, cut1, cut2):
        a, b = cut1
        c, d = cut2
        return self.do_not_cross(a, b, c, d)

    def do_not_cross(self, a, b, c, d):
        def area(a, b, c):
            return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

        def intersect(a, b, c, d):
            if a > b:
                a, b = b, a
            if c > d:
                c, d = d, c
            return max(a, c) <= min(b, d)

        return not (intersect(a.x, b.x, c.x, d.x) and
                    intersect(a.y, b.y, c.y, d.y) and
                    area(a, b, c) * area(a, b, d) <= 0 and
                    area(c, d, a) * area(c, d, b) <= 0)

    def cut_do_not_cross_side(self, cut, side):
        a, b = cut
        return self.do_not_cross(a, b, side.a, side.b)

    def test_draw_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        l = 2.
        draw(tr, get_cut_points(l, tr), get_cuts(l, tr))

    def test_equilateral_triangle(self):
        a = Point(0., 0.)
        b = Point(4., 0.)
        c = Point(2., 2 * math.sqrt(3))
        tr = Triangle(a, b, c)
        self.assertTrue(tr.is_equilateral())
        a = Point(0., 0.)
        b = Point(-4., 0.)
        c = Point(-2., 2 * math.sqrt(3))
        tr = Triangle(a, b, c)
        self.assertTrue(tr.is_equilateral())

    def test_can_cut_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        self.assertTrue(can_cut(1., tr))
        self.assertTrue(can_cut(2., tr))
        l = tr.sides[0].length() * math.sqrt(3) + DELTA
        self.assertFalse(can_cut(l, tr))

    def test_cut_points_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        p1, p2, p3 = get_cut_points(2., tr)
        ab, bc, ca = tr.sides

        self.assertTrue(self.point_on_side(p1, ab))
        self.assertTrue(self.point_on_side(p2, bc))
        self.assertTrue(self.point_on_side(p3, ca))

    def test_cuts_equilateral_triangle_perpendicular(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        c1, c2, c3 = get_cuts(2., tr)
        ab, bc, ca = tr.sides
        self.assertTrue(self.cut_cross_side_perpendicular(c1, ab))
        self.assertTrue(self.cut_cross_side_perpendicular(c2, bc))
        self.assertTrue(self.cut_cross_side_perpendicular(c3, ca))

    def test_cuts_equilateral_triangle_side_cross_cut_in_the_middle(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        c1, c2, c3 = get_cuts(2., tr)
        p1, p2, p3 = get_cut_points(2., tr)
        self.assertTrue(self.side_cross_cut_in_the_middle(p1, c1))
        self.assertTrue(self.side_cross_cut_in_the_middle(p2, c2))
        self.assertTrue(self.side_cross_cut_in_the_middle(p3, c3))

    def test_cuts_equilateral_triangle_cuts_do_not_cross(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        c1, c2, c3 = get_cuts(2., tr)
        self.assertTrue(self.cuts_do_not_cross(c1, c2))
        self.assertTrue(self.cuts_do_not_cross(c1, c3))
        self.assertTrue(self.cuts_do_not_cross(c2, c3))

    def test_cuts_equilateral_triangle_cut_do_not_cross_side(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        c1, c2, c3 = get_cuts(2., tr)
        ab, bc, ca = tr.sides
        self.assertTrue(self.cut_do_not_cross_side(c1, ca))
        self.assertTrue(self.cut_do_not_cross_side(c1, bc))
        self.assertTrue(self.cut_do_not_cross_side(c2, ca))
        self.assertTrue(self.cut_do_not_cross_side(c2, ab))
        self.assertTrue(self.cut_do_not_cross_side(c3, ab))
        self.assertTrue(self.cut_do_not_cross_side(c3, bc))



    def test_acute_triangle(self):
        a = Point(0., 0.)
        b = Point(4., 0.)
        c = Point(2., 3.5)
        tr = Triangle(a, b, c)
        self.assertTrue(tr.is_acute())

    def test_draw_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        draw(tr, get_cut_points(2., tr), get_cuts(2., tr))

    def test_cut_points_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        p1, p2, p3 = get_cut_points(2., tr)
        ab, bc, ca = tr.sides

        self.assertTrue(self.point_on_side(p1, ab))
        self.assertTrue(self.point_on_side(p2, bc))
        self.assertTrue(self.point_on_side(p3, ca))

    def test_cuts_acute_triangle_perpendicular(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        c1, c2, c3 = get_cuts(2., tr)
        ab, bc, ca = tr.sides
        self.assertTrue(self.cut_cross_side_perpendicular(c1, ab))
        self.assertTrue(self.cut_cross_side_perpendicular(c2, bc))
        self.assertTrue(self.cut_cross_side_perpendicular(c3, ca))

    def test_cuts_acute_triangle_side_cross_cut_in_the_middle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        c1, c2, c3 = get_cuts(2., tr)
        p1, p2, p3 = get_cut_points(2., tr)
        self.assertTrue(self.side_cross_cut_in_the_middle(p1, c1))
        self.assertTrue(self.side_cross_cut_in_the_middle(p2, c2))
        self.assertTrue(self.side_cross_cut_in_the_middle(p3, c3))

    def test_cuts_acute_triangle_cuts_do_not_cross(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        c1, c2, c3 = get_cuts(2., tr)
        self.assertTrue(self.cuts_do_not_cross(c1, c2))
        self.assertTrue(self.cuts_do_not_cross(c1, c3))
        self.assertTrue(self.cuts_do_not_cross(c2, c3))

    def test_cuts_acute_triangle_cut_do_not_cross_side(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.7))
        c1, c2, c3 = get_cuts(2., tr)
        ab, bc, ca = tr.sides
        self.assertTrue(self.cut_do_not_cross_side(c1, ca))
        self.assertTrue(self.cut_do_not_cross_side(c1, bc))
        self.assertTrue(self.cut_do_not_cross_side(c2, ca))
        self.assertTrue(self.cut_do_not_cross_side(c2, ab))
        self.assertTrue(self.cut_do_not_cross_side(c3, ab))
        self.assertTrue(self.cut_do_not_cross_side(c3, bc))


if __name__ == '__main__':
    unittest.main()
