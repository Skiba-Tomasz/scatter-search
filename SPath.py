from SConn import SConn
class SPath:

    def __init__(self, connections: SConn, cost: float):
        self.connections = connections
        self.cost = float(cost)

    #TODO
    # def __str__(self):
    #     return "[from = " + str(self.origin) + ", to = " + str(self.destination) + ", cost = " + str(self.cost) + ", used = " + str(self.used) + "]"