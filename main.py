import csv
from textwrap import indent
from plot import plotPath
from SPoint import SPoint
from SConn import SConn
import random

       
FILE_BASE_PATH = "C:/Users/Tomasz/Documents/Projects/Studia/Heurystyki/scatter-search/"

def loadPointsFromFile(fileName):
    points = []
    fileData = list(csv.reader(open(fileName)))
    for dataPoint in fileData:
        point = SPoint(dataPoint[0], dataPoint[1])
        points.append(point)
    return points

def loadConnectionsFromFile(points, fileName):
    connections = []
    fileData = list(csv.reader(open(fileName)))
    for dataPoint in fileData:
        connection = SConn(points[int(dataPoint[0])-1], points[int(dataPoint[1])-1], dataPoint[2])
        connections.append(connection)
    return connections

def printMoves(moves):
    print("Current moves:")
    for move in moves:
        print(move)

def getPossibleMoves(connections: SConn, currentPosition: SPoint) -> SConn:
    return [c for c in connections if c.origin == currentPosition and c.used == False and c.destination.visited == False]

def pickWeightedRandomMove(possibleMoves: SConn):
    if len(possibleMoves) == 1:
        return possibleMoves[0]
    weights = [1/c.cost for c in possibleMoves]
    selected = random.choices(possibleMoves, weights)
    return selected[0]
    # totalConst = 0
    # for m in currentMoves:
    #     totalConst += m.cost

def selectMove(possibleMoves: SConn):
    return pickWeightedRandomMove(possibleMoves)

def improvementFunction(pathConnections: SConn):
    lastestTopCostConnection = pathConnections[len(pathConnections) - 1]
    lastestTopCostConnectionIndex = len(pathConnections) - 1
    for index, connection in reversed(list(enumerate(pathConnections))):
        if connection.cost > lastestTopCostConnection.cost:
            lastestTopCostConnection = connection
            lastestTopCostConnectionIndex = index
    return pathConnections[:lastestTopCostConnectionIndex]

        
def makeMove(currentPosition, connection, path):
    path.append(connection)
    connection.used = True
    connection.destination.visited = True
    return connection.destination

def createSimplePath(connections):
    # INITIALIZE
    path = []
    totalCost = 0
    currentPosition = connections[0].origin
    currentPosition.visited = True
    #
    # possibleMoves = getPossibleMoves(connections, currentPosition)
    # printMoves(possibleMoves)
    # selectedConnection = pickWeightedRandomMove(possibleMoves)
    # currentPosition = makeMove(currentPosition, selectedConnection, path)
    # totalCost += selectedConnection.cost
    while True:
        possibleMoves = getPossibleMoves(connections, currentPosition)
        if len(possibleMoves) == 0:
            break
        printMoves(possibleMoves)
        selectedConnection = selectMove(possibleMoves)
        currentPosition = makeMove(currentPosition, selectedConnection, path)
        totalCost += selectedConnection.cost
    return path, totalCost


if __name__ == '__main__':
    points = loadPointsFromFile(FILE_BASE_PATH  + 'points.csv')
    points[0].visited = True
    connections = loadConnectionsFromFile(points, FILE_BASE_PATH + 'connections.csv')

    moves, cost = createSimplePath(connections)
    subsequentOrigins = []

    print("Selected path with cost " + str(cost) + " steps taken " + str(len(moves)))
    for m in moves:
        print(str(m))
        subsequentOrigins.append(m.origin)

    plotPath(subsequentOrigins)