from SConn import SConn
import copy 
class SPath:

    def __init__(self, path: SConn, cost: float, possibleConnections: SConn):
        self.path = copy.deepcopy(path)
        self.cost = float(cost)
        self.possibleConnections = copy.deepcopy(possibleConnections)

    def setPathConnections(self, path: SConn):
        self.path = copy.deepcopy(path)
    #TODO
    # def __str__(self):
    #     return "[from = " + str(self.origin) + ", to = " + str(self.destination) + ", cost = " + str(self.cost) + ", used = " + str(self.used) + "]"