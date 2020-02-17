import math

from autoCAD.src.constants import DELTA, EPSILON
from autoCAD.src.point import Point
from autoCAD.src.triangle import Triangle
from autoCAD.src.visualizer import draw


def get_cut_point(l, side):
    ab = side.length()
    a, b = side.a, side.b
    d = (ab - l / math.sqrt(3) - DELTA) / 2
    return Point(d / ab * (a.x + (ab - d) / d * b.x), d / ab * (a.y + (ab - d) / d * b.y))


def get_cut_points(l, tr):
    return [get_cut_point(l, side) for side in tr.sides]


def get_cut(l, side):
    p = get_cut_point(l, side)
    a, b = side.a, side.b
    x1, y1 = a.x - b.x, a.y - b.y
    if x1 != 0:
        y2 = l * abs(x1) / math.sqrt(x1 ** 2 + y1 ** 2)
        x2 = - y1 * y2 / x1
    else:
        y2 = 0
        x2 = l
    return Point(x2 + p.x, y2 + p.y), Point(-x2 + p.x, -y2 + p.y)


def get_cuts(l, tr):
    return [get_cut(l, side) for side in tr.sides]


def can_cut(l, tr: Triangle):
    if not tr.is_valid_triangle():
        print("Not a triangle")
        return False
    if tr.is_equilateral():
        print("Triangle is equilateral")
        side, _, _ = tr.sides
        return l * math.sqrt(3) + 3 * DELTA < side.length() + EPSILON
    if tr.is_acute():
        print("Triangle is acute")
        return
    if tr.is_obtuse():
        print("Triangle is obtuse")
        return
    return


if __name__ == '__main__':
    L = float(input())
    points = []
    for _ in range(3):
        x, y = list(map(float, input().split()))
        points.append(Point(x, y))
    tr = Triangle(points[0], points[1], points[2])
    l = L / 2
    cut_exists = can_cut(l, tr)
    if cut_exists:
        for cut in get_cuts(l, tr):
            print("(%.6f, %.6f) (%.6f, %.6f)" % (cut[0].x, cut[0].y, cut[1].x, cut[1].y))
        draw(tr, get_cut_points(l, tr), get_cuts(l, tr))

