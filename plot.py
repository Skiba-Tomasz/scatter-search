import matplotlib.pyplot as plt
from SPoint import SPoint

def plotPath(points: SPoint):
    x = [float(i.x) for i in points]
    y = [float(i.y) for i in points]

    plt.plot(x, y, 'co', markersize=3)

    a_scale = float(max(x)) / float(100)

    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                  color='g', length_includes_head=True)

    xMargin = min(x) * 0.8
    yMargin = min(y) * 0.8

    plt.xlim(min(x) - xMargin, max(x) + xMargin)
    plt.ylim(min(y) - yMargin, max(y) + yMargin)
    plt.show()