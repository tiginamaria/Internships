import matplotlib.pyplot as plt


def draw(triangle, cut_points, cuts):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    a, b, c = triangle.points
    ax.add_line(plt.Line2D([a.x, b.x, c.x, a.x], [a.y, b.y, c.y, a.y]))
    for p in cut_points:
        ax.add_artist(plt.Circle((p.x, p.y), 0.1))
    for (a, b) in cuts:
        ax.add_line(plt.Line2D([a.x, b.x], [a.y, b.y]))
    plt.axis('scaled')
    plt.show()
