class SPoint:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def __str__(self):
        return "[x = " + str(self.x) + ", y = " + str(self.y) + ", v = " + str(self.visited) + "]"

    def __eq__(self, other):
        if isinstance(other, SPoint):
            return self.x == other.x and self.y == other.y
        return False