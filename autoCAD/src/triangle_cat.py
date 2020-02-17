import math

from autoCAD.src.constants import DELTA, EPSILON
from autoCAD.src.point import Point
from autoCAD.src.triangle import Triangle
from autoCAD.src.visualizer import draw


def calc_cut_point(d, side):
    ab = side.length()
    a, b = side.a, side.b
    return Point((ab - d) / ab * (a.x + d / (ab - d) * b.x), (ab - d) / ab * (a.y + d / (ab - d) * b.y))


def calc_cut_points(l, cosines, sides):
    cut_points = []
    for (cos, side) in zip(cosines, sides):
        d, _ = calc_cut_sides(cos, l + DELTA)
        print(cos, side.length(), d)
        cut_points.append(calc_cut_point(d, side))
    return cut_points


def calc_cut(l, p, side):
    a, b = side.a, side.b
    x1, y1 = a.x - b.x, a.y - b.y
    if x1 != 0:
        y2 = l * abs(x1) / math.sqrt(x1 ** 2 + y1 ** 2)
        x2 = - y1 * y2 / x1
    else:
        y2 = 0
        x2 = l
    return Point(x2 + p.x, y2 + p.y), Point(-x2 + p.x, -y2 + p.y)


def calc_cuts(l, tr):
    cut_points = calc_cut_points(l, tr.cosines(), tr.sides)
    return [calc_cut(l, p, side) for p, side in zip(cut_points, tr.sides)]


def can_cut_equilateral(l, tr: Triangle):
    side, _, _ = tr.sides
    return (l + DELTA) * math.sqrt(3) < side.length() + EPSILON


def calc_cut_sides(cos, side):
    sin = math.sqrt(1 - cos ** 2)
    return side * cos / sin, side / sin


def can_cut_acute(l, tr: Triangle):
    cos_a, cos_b, cos_c = tr.cosines()
    ab, bc, ca = map(lambda side: side.length(), tr.sides)
    xa, ya = calc_cut_sides(cos_a, l + DELTA)
    xb, yb = calc_cut_sides(cos_b, l + DELTA)
    xc, yc = calc_cut_sides(cos_c, l + DELTA)
    return xa + yb < ab + EPSILON and xb + yc < bc + EPSILON and xc + ya < ca + EPSILON


def can_cut_obtuse(l, tr: Triangle):
    pass


def can_cut(l, tr: Triangle):
    if not tr.is_valid_triangle():
        print("Not a triangle")
        return False
    if tr.is_equilateral():
        print("Triangle is equilateral")
        return can_cut_equilateral(l, tr)
    if tr.is_acute():
        print("Triangle is acute")
        return can_cut_acute(l, tr)
    if tr.is_obtuse():
        print("Triangle is obtuse")
        return can_cut_obtuse(l, tr)


def get_cut_points(L, tr: Triangle):
    l = L / 2
    if not tr.is_valid_triangle():
        return []
    if tr.is_equilateral() or tr.is_acute():
        return calc_cut_points(l, tr.cosines(), tr.sides)
    if tr.is_obtuse():
        print("Triangle is obtuse")
        return
    return


def get_cuts(L, tr: Triangle):
    l = L / 2
    if not tr.is_valid_triangle():
        return []
    if tr.is_equilateral() or tr.is_acute():
        return calc_cuts(l, tr)
    if tr.is_obtuse():
        print("Triangle is obtuse")
        return
    return


def triangle_cut(L, tr: Triangle):
    l = L / 2
    cut_exists = can_cut(l, tr)
    if cut_exists:
        for cut in calc_cuts(l, tr):
            print("(%.6f, %.6f) (%.6f, %.6f)" % (cut[0].x, cut[0].y, cut[1].x, cut[1].y))
        draw(tr, get_cut_points(l, tr), calc_cuts(l, tr))
