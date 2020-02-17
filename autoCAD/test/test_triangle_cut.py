import math
import unittest

from autoCAD.src.constants import DELTA
from autoCAD.src.geom_utils import point_on_side, cut_cross_side_perpendicular, side_cross_cut_in_the_middle, \
    cuts_do_not_cross, cut_do_not_cross_side
from autoCAD.src.point import Point
from autoCAD.src.triangle import Triangle
from autoCAD.src.triangle_cat import can_cut, get_cut_points, get_cuts
from autoCAD.src.visualizer import draw


class InterpreterTests(unittest.TestCase):

    def check_point_on_side(self, L, tr):
        p1, p2, p3 = get_cut_points(L, tr)
        ab, bc, ca = tr.sides
        self.assertTrue(point_on_side(p1, ab))
        self.assertTrue(point_on_side(p2, bc))
        self.assertTrue(point_on_side(p3, ca))

    def check_cuts_cross_sides_perpendicular(self, L, tr):
        c1, c2, c3 = get_cuts(L, tr)
        ab, bc, ca = tr.sides
        self.assertTrue(cut_cross_side_perpendicular(c1, ab))
        self.assertTrue(cut_cross_side_perpendicular(c2, bc))
        self.assertTrue(cut_cross_side_perpendicular(c3, ca))

    def check_sides_cross_cuts_in_the_middle(self, L, tr):
        c1, c2, c3 = get_cuts(L, tr)
        p1, p2, p3 = get_cut_points(L, tr)
        self.assertTrue(side_cross_cut_in_the_middle(p1, c1))
        self.assertTrue(side_cross_cut_in_the_middle(p2, c2))
        self.assertTrue(side_cross_cut_in_the_middle(p3, c3))

    def check_cuts_do_not_cross(self, L, tr):
        c1, c2, c3 = get_cuts(L, tr)
        self.assertTrue(cuts_do_not_cross(c1, c2))
        self.assertTrue(cuts_do_not_cross(c1, c3))
        self.assertTrue(cuts_do_not_cross(c2, c3))

    def check_cuts_do_not_cross_sides(self, L, tr):
        c1, c2, c3 = get_cuts(L, tr)
        ab, bc, ca = tr.sides
        self.assertTrue(cut_do_not_cross_side(c1, ca))
        self.assertTrue(cut_do_not_cross_side(c1, bc))
        self.assertTrue(cut_do_not_cross_side(c2, ca))
        self.assertTrue(cut_do_not_cross_side(c2, ab))
        self.assertTrue(cut_do_not_cross_side(c3, ab))
        self.assertTrue(cut_do_not_cross_side(c3, bc))

    def test_draw_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        l = 2.
        draw(tr, get_cut_points(l, tr), get_cuts(l, tr))

    def test_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        self.assertTrue(tr.is_equilateral())
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        self.assertTrue(tr.is_equilateral())

    def test_can_cut_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        self.assertTrue(can_cut(1., tr))
        self.assertTrue(can_cut(2., tr))
        self.assertFalse(can_cut(tr.sides[0].length() * math.sqrt(3) + DELTA, tr))

    def test_cut_points_equilateral_triangle(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        self.check_point_on_side(2.0, tr)

    def test_cuts_equilateral_triangle_perpendicular(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        self.check_cuts_cross_sides_perpendicular(2.0, tr)

    def test_cuts_equilateral_triangle_side_cross_cut_in_the_middle(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        self.check_sides_cross_cuts_in_the_middle(2.0, tr)

    def test_cuts_equilateral_triangle_cuts_do_not_cross(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 2 * math.sqrt(3)))
        self.check_cuts_do_not_cross(2.0, tr)

    def test_cuts_equilateral_triangle_cut_do_not_cross_side(self):
        tr = Triangle(Point(0., 0.), Point(-4., 0.), Point(-2., 2 * math.sqrt(3)))
        self.check_cuts_do_not_cross_sides(2.0, tr)

    def test_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.assertTrue(tr.is_acute())

    def test_draw_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        draw(tr, get_cut_points(2., tr), get_cuts(2., tr))
        tr = Triangle(Point(-2., 0.), Point(3., 0.), Point(1., 7.))
        draw(tr, get_cut_points(2., tr), get_cuts(2., tr))

    def test_can_cut_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.assertTrue(can_cut(1., tr))
        self.assertTrue(can_cut(2., tr))
        self.assertFalse(can_cut(5., tr))

    def test_cut_points_acute_triangle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.check_point_on_side(2.0, tr)

    def test_cuts_acute_triangle_perpendicular(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.check_cuts_cross_sides_perpendicular(2.0, tr)

    def test_cuts_acute_triangle_side_cross_cut_in_the_middle(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.check_sides_cross_cuts_in_the_middle(2.0, tr)

    def test_cuts_acute_triangle_cuts_do_not_cross(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.check_cuts_do_not_cross(2.0, tr)

    def test_cuts_acute_triangle_cut_do_not_cross_side(self):
        tr = Triangle(Point(0., 0.), Point(4., 0.), Point(2., 3.5))
        self.check_cuts_do_not_cross_sides(2.0, tr)

    def test_draw_obtuse_triangle(self):
        tr = Triangle(Point(0., 0.), Point(8., 0.), Point(2., 3.))
        draw(tr, get_cut_points(2., tr), get_cuts(2., tr))
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        draw(tr, get_cut_points(2., tr), get_cuts(2., tr))
        tr = Triangle(Point(8., 2.), Point(2., -1.), Point(0., 0.))
        draw(tr, get_cut_points(1.5, tr), get_cuts(1.5, tr))

    def test_can_cut_obtuse_triangle(self):
        tr = Triangle(Point(8., 2.), Point(2., -1.), Point(0., 0.))
        self.assertTrue(can_cut(1., tr))
        self.assertTrue(can_cut(1.5, tr))
        self.assertFalse(can_cut(2., tr))

    def test_cut_points_obtuse_triangle(self):
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        self.check_point_on_side(2.0, tr)

    def test_cuts_obtuse_triangle_perpendicular(self):
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        self.check_cuts_cross_sides_perpendicular(2.0, tr)

    def test_cuts_obtuse_triangle_side_cross_cut_in_the_middle(self):
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        self.check_sides_cross_cuts_in_the_middle(2.0, tr)

    def test_cuts_obtuse_triangle_cuts_do_not_cross(self):
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        self.check_cuts_do_not_cross(2.0, tr)

    def test_cuts_obtuse_triangle_cut_do_not_cross_side(self):
        tr = Triangle(Point(8., 2.), Point(0., 0.), Point(2., 3.))
        self.check_cuts_do_not_cross_sides(2.0, tr)


if __name__ == '__main__':
    unittest.main()
