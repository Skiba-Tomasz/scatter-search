import copy
import csv
from importlib.resources import path
from textwrap import indent
from plot import plotConnections, comparePlot
from SPoint import SPoint
from SConn import SConn
from SPath import SPath
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

def resetPositionToLastTopCostMove(path: SPath, connections: SConn):
    lastestTopCostConnection = path.connections[0]
    lastestTopCostConnectionIndex = 0
    for index, connection in list(enumerate(path.connections)):
        if connection.cost > lastestTopCostConnection.cost:
            lastestTopCostConnection = connection
            lastestTopCostConnectionIndex = index
    movesToReset = path.connections[lastestTopCostConnectionIndex:]
    for move in movesToReset:
        for con in connections:
            if con.origin == move.origin and con.destination == move.destination:
                con.used = False
        move.destination.visited = False
        move.used = False
        path.cost -= move.cost
    path.connections = path.connections[:lastestTopCostConnectionIndex]
    return path, lastestTopCostConnectionIndex
    
def continuePath(path, connections, index):
    if len(path.connections) == 0:
        return createSimplePath(connections)
    currentPosition = path.connections[index - 1].destination
    currentPosition.visited = True
    while True:
        possibleMoves = getPossibleMoves(connections, currentPosition)
        printMoves(possibleMoves)
        if len(possibleMoves) == 0:
            break
        selectedConnection = selectMove(possibleMoves)
        currentPosition = makeMove(currentPosition, selectedConnection, path.connections)
        path.cost += selectedConnection.cost
    return SPath(path.connections, path.cost)
        
def makeMove(currentPosition, connection, path):
    path.append(connection)
    connection.used = True
    connection.destination.visited = True
    return connection.destination

def createSimplePath(connections):
    # INITIALIZE
    pathConnections = []
    totalCost = 0
    currentPosition = connections[0].origin
    currentPosition.visited = True
    # STARTING PATH
    while True:
        possibleMoves = getPossibleMoves(connections, currentPosition)
        printMoves(possibleMoves)
        if len(possibleMoves) == 0:
            break
        selectedConnection = selectMove(possibleMoves)
        currentPosition = makeMove(currentPosition, selectedConnection, pathConnections)
        totalCost += selectedConnection.cost
    return SPath(pathConnections, totalCost)


if __name__ == '__main__':
    points = loadPointsFromFile(FILE_BASE_PATH  + 'points.csv')
    connections = loadConnectionsFromFile(points, FILE_BASE_PATH + 'connections.csv')
    pathStore = []

    basePath = createSimplePath(connections)
    pathStore.append(copy.deepcopy(basePath))

    print("Selected path with cost " + str(basePath.cost) + " steps taken " + str(len(basePath.connections)))
    plotConnections(basePath.connections, save = True)

    resetedPath, resetIndex = resetPositionToLastTopCostMove(basePath, connections)
    upgradedPath = continuePath(resetedPath, connections, resetIndex)
    pathStore.append(copy.deepcopy(upgradedPath))

    print("Selected path with cost " + str(upgradedPath.cost) + " steps taken " + str(len(upgradedPath.connections)))
    plotConnections(upgradedPath.connections, save = True)


    print("Summary:")
    for p in pathStore:
        print("Selected path with cost " + str(p.cost) + " steps taken " + str(len(p.connections)))
        printMoves(p.connections)

    # comparePlot(pathStore[0].connections, pathStore[1].connections)
    # print("END")