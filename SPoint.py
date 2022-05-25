class SPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def __str__(self):
        return "[x = " + str(self.x) + ", y = " + str(self.y) + ", v = " + str(self.visited) + "]"