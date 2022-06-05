from scipy.spatial import distance
from plot import plotPath
import csv
import random
import copy

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

def randomWeightedLowCostSort(position, nextPaths, costMap):
    if len(nextPaths) == 1:
        return nextPaths[0]
    weights = [1/costMap.get(getCostKey(position, move)) for move in nextPaths]
    # for i, w in list(enumerate(weights)):
    #     if weights[i] == max(weights):
    #         weights[i] = weights[i] * 100
    selected = random.choices(nextPaths, weights)[0]
    nextPaths.remove(selected)
    nextPaths.insert(0, selected)

def hamiltonLowCostPrefered(G, costMap, size, pt, path=[], trace = False):
    if trace == True:
        print('hamilton called with pt={}, path={}'.format(pt, path))
    if pt not in set(path):
        path.append(pt)
        if len(path)==size:
            return path
        nextPaths = G.get(pt, [])
        if nextPaths is not None and all(p is not None for p in nextPaths):
            randomWeightedLowCostSort(pt, nextPaths, costMap)
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

def generateStartingSolutions(G, costMap, size, seed = None, max_iter=100, strategy=hamiltonLowCostPrefered):
    if seed == None:
        seed = int(random.uniform(1,10**5))
    print(f"Current run seed is {seed}")
    random.seed(seed)
    solutions = []
    for i in range(0, size):
        iter = 0
        while True:
            iter += 1
            solution = strategy(G, costMap, len(G), 1, path=[])
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
    points = {}
    fileData = list(csv.reader(open(fileName)))
    for i, p in list(enumerate(fileData)):
        if i == 0:
            continue
        px = float(p[1])
        py = float(p[2])
        points[i] = [px, py]
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
    return graph, costMap, points

def calculateCost(path, costMap):
    totalCost = 0
    for i in range(0, len(path) -1):
        totalCost += costMap[getCostKey(path[i], path[i+1])]
    return totalCost

def selectBestSolutions(paths, costs, topPercent):
    if len(paths) != len(costs):
        raise ValueError("Path list is not the same size as costs list")

    costsCoppy = copy.deepcopy(costs)
    topPathsCount = int((len(paths)*topPercent)/100)
    print(f"Selecting best {topPercent}% of paths - {topPathsCount} in total")
    topPaths = []
    lowestCosts = []
    for i in range(0, topPathsCount):
        minCostElement = min(costsCoppy)
        topPaths.append(paths[costsCoppy.index(minCostElement)])
        lowestCosts.append(minCostElement)
        costsCoppy.remove(minCostElement)
    return topPaths, lowestCosts


def combinePaths(p1, p2, n, costMap):
    """
        p1 - path that will be combined, p1 should be lower cost path than p2 
        p2 - path that will be combined
        n - element count that local optimialization will take place

        pc - combined path
    """
    if len(p1) != len(p2):
        raise ValueError("Can not combine paths. They are not the same length")
    if calculateCost(p1, costMap) > calculateCost(p2, costMap):
        raise ValueError("p1 has higher cost than p2")
    
    print("Combining paths:")
    print(f"{p1}")
    print(f"{p2}")

    combinedPath = []
    combinedPath.append(p1[0]) 
    l = len(p1)
    for i in range (1, len(p1)):
        if p1[i-1] == p2[i-1] and p1[i] == p2[i]:
            combinedPath.append(p1[i])
            continue
        if i + n < l:
            print(f"Reducing n value - {n} would be out of range. Setting {l - i}")
            n = l - i
        print(f"Path choice differ at i={i}, stepping back")
        combinedPath.remove(combinedPath[i])
        i -= 1
        p1Fragment = p1[i: i+n]
        p2Fragment = p2[i: i+n]
        bestFragment = None
        if calculateCost(p1Fragment, costMap) < calculateCost(p2Fragment, costMap):
            bestFragment = p1Fragment
            print(f"Best fragment is from path 1: {bestFragment}")
        else:
            bestFragment = p2Fragment
            print(f"Best fragment is from path 2: {bestFragment}")
        if bestFragment not in combinedPath:
            for element in bestFragment:
                combinedPath.append(element)
            i += n
        else:
            print(f"Could not combine fragment. Elements of bestFragment {list(set(combinedPath).intersection(bestFragment))} are in current path")
            combinedPath.append(p1[i])



if __name__ == '__main__':

    # for i in range(0, 20):
    # Initialize phase 
    graph, costMap, points = loadPointsFromFile("points-10.csv")
    paths = generateStartingSolutions(graph, costMap, 10, seed = 54840)
    costs = [calculateCost(path,costMap) for path in paths]

    bestPaths, lowestCosts = selectBestSolutions(paths, costs, 50)
    # End of initialize phase 
