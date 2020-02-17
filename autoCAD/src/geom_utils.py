from autoCAD.src.constants import EPSILON
from autoCAD.src.side import Side


def cos(v1, v2):
    return v1.s_prod(v2) / v1.length() / v2.length()


def point_on_side(p, side):
    return abs(cos(side, Side(p, side.a)) + 1) < EPSILON


def cut_cross_side_perpendicular(cut, side):
    return abs(cos(side, Side(cut[0], cut[1]))) < EPSILON


def side_cross_cut_in_the_middle(p, cut):
    return abs(p.dist(cut[0]) - p.dist(cut[1])) < EPSILON


def cuts_do_not_cross(cut1, cut2):
    a, b = cut1
    c, d = cut2
    return do_not_cross(a, b, c, d)


def do_not_cross(a, b, c, d):
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


def cut_do_not_cross_side(cut, side):
    a, b = cut
    return do_not_cross(a, b, side.a, side.b)
