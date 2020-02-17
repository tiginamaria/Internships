import math

from autoCAD.src.constants import DELTA, EPSILON
from autoCAD.src.geom_utils import cuts_do_not_cross
from autoCAD.src.point import Point
from autoCAD.src.triangle import Triangle
from autoCAD.src.visualizer import draw


def calc_cut_point(d, side):
    ab = side.length()
    a, b = side.a, side.b
    return Point((ab - d) / ab * (a.x + d / (ab - d) * b.x), (ab - d) / ab * (a.y + d / (ab - d) * b.y))


def calc_cut_points(L, cosines, sides):
    cut_points = []
    for (cos, side) in zip(cosines, sides):
        d, _ = calc_cut_sides(cos, L)
        cut_points.append(calc_cut_point(d, side))
    return cut_points


def calc_obtuse_cut_points(L, tr):
    cos_a, cos_b, cos_c = tr.cosines()
    xb, yb = calc_cut_sides(cos_b, L)
    ab = tr.sides[0]
    xa = yb + DELTA
    return [calc_cut_point(ab.length() - xa, ab)] + calc_cut_points(L, tr.cosines()[1:], tr.sides[1:])


def calc_cut(L, p, side):
    x1, y1 = side.to_zero().x, side.to_zero().y
    if x1 != 0:
        y2 = L / 2.0 * abs(x1) / side.length()
        x2 = - y1 * y2 / x1
    else:
        y2 = 0
        x2 = L / 2.0
    return Point(x2 + p.x, y2 + p.y), Point(-x2 + p.x, -y2 + p.y)


def calc_cuts(L, cut_points, sides):
    return [calc_cut(L, p, side) for p, side in zip(cut_points, sides)]


def can_cut_equilateral(L, tr: Triangle):
    side, _, _ = tr.sides
    return (L / 2.0 + DELTA) * math.sqrt(3) < side.length() + EPSILON


def calc_cut_sides(cos, L):
    sin = math.sqrt(1 - cos ** 2)
    side = L / 2.0 + DELTA
    return side * cos / sin, side / sin


def can_cut_acute(l, tr: Triangle):
    cos_a, cos_b, cos_c = tr.cosines()
    ab, bc, ca = map(lambda side: side.length(), tr.sides)
    xa, ya = calc_cut_sides(cos_a, l + DELTA)
    xb, yb = calc_cut_sides(cos_b, l + DELTA)
    xc, yc = calc_cut_sides(cos_c, l + DELTA)
    return xa + yb < ab + EPSILON and xb + yc < bc + EPSILON and xc + ya < ca + EPSILON


def can_cut_obtuse(L, tr: Triangle):
    cos_a, cos_b, cos_c = tr.cosines()
    xb, yb = calc_cut_sides(cos_b, L)
    xa, ya = yb + DELTA, cos_b * (yb + DELTA)
    cut_points = calc_obtuse_cut_points(L, tr)
    cuts = calc_cuts(L, cut_points, tr.sides)
    if (tr.sides[0].length() - xa) > EPSILON and cuts_do_not_cross(cuts[0], cuts[1]):
        return True
    return False


def can_cut(L, tr: Triangle):
    if not tr.is_valid_triangle():
        return False
    if tr.is_equilateral():
        return can_cut_equilateral(L, tr)
    if tr.is_acute():
        return can_cut_acute(L, tr)
    if tr.is_obtuse():
        return can_cut_obtuse(L, tr)


def get_cut_points(L, tr: Triangle):
    if not can_cut(L, tr):
        return []
    if tr.is_equilateral() or tr.is_acute():
        return calc_cut_points(L, tr.cosines(), tr.sides)
    if tr.is_obtuse():
        return calc_obtuse_cut_points(L, tr)
    return


def get_cuts(L, tr: Triangle):
    if not tr.is_valid_triangle():
        return []
    return calc_cuts(L, get_cut_points(L, tr), tr.sides)


def triangle_cut(L, tr: Triangle):
    cut_exists = can_cut(L, tr)
    if cut_exists:
        for cut in get_cuts(L, tr):
            print("(%.6f, %.6f) (%.6f, %.6f)" % (cut[0].x, cut[0].y, cut[1].x, cut[1].y))
        draw(tr, get_cut_points(L, tr), get_cuts(L, tr))
