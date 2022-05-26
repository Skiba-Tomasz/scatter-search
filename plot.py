import time
import matplotlib.pyplot as plt
from SPoint import SPoint
from SConn import SConn

FILE_BASE_PATH = "C:/Users/Tomasz/Documents/Projects/Studia/Heurystyki/scatter-search/"


def plotConnections(connections: SConn, show = True, color = "g", stroke = 1, save = False):
    subsequentOrigins = []
    for m in connections:
        subsequentOrigins.append(m.origin)
    subsequentOrigins.append(connections[len(connections) - 1].destination)
    plotPath(subsequentOrigins, show, color, stroke, save)

def plotPath(points: SPoint, show = True, color = "g", stroke = 1, save = False):
    x = [float(i.x) for i in points]
    y = [float(i.y) for i in points]

    plt.plot(x, y, 'co', markersize=3, linewidth=5*stroke)

    a_scale = float(max(x)) / float(100)

    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale*3,
              color=color, length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale*3,
                  color=color, length_includes_head=True)

    xMargin = min(x) * 0.8
    yMargin = min(y) * 0.8

    plt.xlim(min(x) - xMargin, max(x) + xMargin)
    plt.ylim(min(y) - yMargin, max(y) + yMargin)
    if save == True:
        plt.savefig(FILE_BASE_PATH + "plots/"+str(int(time.time()*1000))+".png")
        if show == False:
            plt.clf()
    if show == True:
        plt.show()

def comparePlot(points1, points2):
    plotConnections(points1, False, "r", 1)
    plotConnections(points2, False, "g", 3)
    plt.show()
