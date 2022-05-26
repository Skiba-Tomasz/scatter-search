from SPoint import SPoint
class SConn:

    def __init__(self, origin: SPoint, destination: SPoint, cost: float):
        self.origin = origin
        self.destination = destination
        self.cost = float(cost)
        self.used = False

    def __str__(self):
        return "[from = " + str(self.origin) + ", to = " + str(self.destination) + ", cost = " + str(self.cost) + ", used = " + str(self.used) + "]"

    def __eq__(self, other):
        if isinstance(other, SConn):
            return self.origin == other.origin and self.destination == other.destination
        return False