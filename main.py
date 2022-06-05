from email import iterators
from scipy.spatial import distance

import csv
import random

def hamilton(G, size, pt, path=[], trace = False):
    if trace == True:
        print('hamilton called with pt={}, path={}'.format(pt, path))
    if pt not in set(path):
        path.append(pt)
        if len(path)==size:
            return path
        nextPaths = G.get(pt, [])
        if nextPaths is not None and all(p is not None for p in nextPaths):
            random.shuffle(nextPaths)
        for pt_next in nextPaths:
            res_path = [i for i in path]
            candidate = hamilton(G, size, pt_next, res_path)
            if candidate is not None:  # skip loop or dead end
                return candidate
        if trace == True:
            print('path {} is a dead end'.format(path))
    else:
        if trace == True:
            print('pt {} already in path {}'.format(pt, path))


def generateStartingSolutions(G, size, seed, max_iter=100):
    random.seed(seed)
    solutions = []
    for i in range(0, size):
        iter = 0
        while True:
            iter += 1
            solution = hamilton(G, len(G), 1, path=[])
            if solution not in solutions:
                solutions.append(solution)
                break
            if iter >= max_iter:
                raise ValueError("Set lower size of starting solutions. Could not find all unique solutions for given graph")
    return solutions

def getCostKey(f: int, t: int) -> str:
    return str(f) + '-' + str(t)

def loadPointsFromFile(fileName):
    graph = {}
    costMap = {}
    fileData = list(csv.reader(open(fileName)))
    for i, p in list(enumerate(fileData)):
        if i == 0:
            continue
        px = float(p[1])
        py = float(p[2])
        graph[i] = []
        for ii, pp in list(enumerate(fileData)):
            if ii == 0:
                continue
            if i == ii:
                continue
            ppx = float(pp[1])
            ppy = float(pp[2])
            graph[i].append(ii)
            costMap[getCostKey(i, ii)] = distance.euclidean((px, py), (ppx, ppy))
    return graph, costMap

def calculateCost(path, costMap):
    totalCost = 0
    for i in range(0, len(path) -1):
        totalCost += costMap[getCostKey(path[i], path[i+1])]
    return totalCost

if __name__ == '__main__':

    graph, costMap = loadPointsFromFile("points.csv")
    paths = generateStartingSolutions(graph, 100, 10)
    costs = [calculateCost(path,costMap) for path in paths]
    print(f"Minimal cost: {min(costs)}")
