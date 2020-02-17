from autoCAD.src.point import Point
from autoCAD.src.triangle import Triangle
from autoCAD.src.triangle_cat import triangle_cut

if __name__ == '__main__':
    L = float(input())
    points = []
    for _ in range(3):
        x, y = list(map(float, input().split()))
        points.append(Point(x, y))
    tr = Triangle(points[0], points[1], points[2])
    triangle_cut(L, tr)
