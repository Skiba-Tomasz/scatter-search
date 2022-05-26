import copy
import csv
from importlib.resources import path
from textwrap import indent
from plot import plotConnections, setFolderName
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
    # print("Current moves:")
    for move in moves:
        print(move)
    print("")

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

def resetPositionToLastTopCostMove(path: SPath):
    lastestTopCostConnection = path.path[0]
    lastestTopCostConnectionIndex = 0
    for index, connection in list(enumerate(path.path)):
        if connection.cost > lastestTopCostConnection.cost:
            lastestTopCostConnection = connection
            lastestTopCostConnectionIndex = index
    movesToReset = path.path[lastestTopCostConnectionIndex:]
    for move in movesToReset:
        for con in path.possibleConnections:
            if con.origin == move.origin and con.destination == move.destination:
                con.used = False
                con.destination.visited = False
        move.destination.visited = False
        move.used = False
        path.cost -= move.cost
    path.path = path.path[:lastestTopCostConnectionIndex]
    return path
    
def continuePath(path: SPath, allConnections: SConn):
    if len(path.path) == 0:
        return createSimplePath(allConnections)
    currentPosition = path.path[len(path.path) - 1].destination #TODO move position to path object
    # currentPosition.visited = True
    while True:
        test = [c for c in path.possibleConnections if c.origin == currentPosition and c.used == False]
        possibleMoves = getPossibleMoves(path.possibleConnections, currentPosition)
        # printMoves(possibleMoves)
        if len(possibleMoves) == 0:
            break
        selectedConnection = selectMove(possibleMoves)
        currentPosition = makeMove(selectedConnection, path.path)
        path.cost += selectedConnection.cost
    return SPath(path.path, path.cost, allConnections)
        
def makeMove(connection, path):
    path.append(connection)
    connection.used = True
    connection.destination.visited = True
    return connection.destination

def createSimplePath(allConnections):
    # INITIALIZE
    path = SPath([], 0, allConnections)
    pathConnections = []
    currentPosition = path.possibleConnections[0].origin
    currentPosition.visited = True
    # STARTING PATH
    while True:
        possibleMoves = getPossibleMoves(path.possibleConnections, currentPosition)
        # printMoves(possibleMoves)
        if len(possibleMoves) == 0:
            break
        selectedConnection = selectMove(possibleMoves)
        currentPosition = makeMove(selectedConnection, pathConnections)
        path.cost += selectedConnection.cost
    path.setPathConnections(pathConnections)
    return path

def start(i):
    #Initialize
    folder = "C:/Users/Tomasz/Documents/Projects/Studia/Heurystyki/scatter-search/plots/" + str(i) + "/"
    saveGraphs = True
    iterationLimit = 10000
    optimalSolution = 70
    points = loadPointsFromFile(FILE_BASE_PATH  + 'points.csv')
    connections = loadConnectionsFromFile(points, FILE_BASE_PATH + 'connections.csv')
    finalMessage = ""

    #Start algorithm

    #Get a solution
    bestSolutions = []
    blockedSolutions = []
    firstPath = createSimplePath(connections)
    bestSolutions.append(copy.deepcopy(firstPath))
    # plotConnections(firstPath.path, save = saveGraphs, show = False)
    nextPath = copy.deepcopy(firstPath)

    stuckMax = 10
    stuckCounter = 0

    #Get improvement solutions
    i = 0
    while True:
        resetPositionToLastTopCostMove(nextPath)
        nextPath = continuePath(nextPath, nextPath.possibleConnections)
        printMoves(nextPath.path)
        if nextPath.cost < bestSolutions[len(bestSolutions) - 1].cost:
            bestSolutions.append(copy.deepcopy(nextPath))
            # plotConnections(nextPath.path, save = saveGraphs, show = False)
        else:
            stuckCounter += 1
            if stuckCounter >= stuckMax:
                lastBlocked = copy.deepcopy(bestSolutions[len(bestSolutions) - 1])
                if len(lastBlocked.path) == 0:
                    print('dupa')
                blockedSolutions.append(copy.deepcopy(bestSolutions[len(bestSolutions) - 1]))
                bestSolutions = bestSolutions[:len(bestSolutions) - 1]
                if len(bestSolutions) >= 1:
                    nextPath = copy.deepcopy(bestSolutions[len(bestSolutions) - 1])
                else:
                    firstPath = createSimplePath(connections)
                    bestSolutions.append(copy.deepcopy(firstPath))
                    # plotConnections(firstPath.path, save = saveGraphs, show = False)
                    nextPath = copy.deepcopy(firstPath)
                stuckCounter = 0

        i += 1
        if nextPath.cost == optimalSolution:
            finalMessage = "Optimal solution found"
            break
        if i >= iterationLimit:
            finalMessage = "Iteration limit reached"
            break
    print("Summary:")
    for p in bestSolutions:
        print("Selected path with cost " + str(p.cost) + " steps taken " + str(len(p.path)) + ":")
        printMoves(p.path)
        plotConnections(p.path, save = saveGraphs, show = False, folder=folder)
    print("Blocked solutions:")
    for p in blockedSolutions:
        print("Selected path with cost " + str(p.cost) + " steps taken " + str(len(p.path)) + ":")
        printMoves(p.path)
        plotConnections(p.path, save = saveGraphs, show = False, color="r", folder=folder)

    print(finalMessage)


if __name__ == '__main__':
    
    for i in range(0,10):
        start(i)