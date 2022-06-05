import csv
from scipy.spatial import distance

FILE_BASE_PATH = "C:/Users/Tomasz/Documents/Projects/Studia/Heurystyki/github/hamilton/"


points = []
fileName = "points.csv"
fileData = list(csv.reader(open(FILE_BASE_PATH + fileName)))
connections = []
for i, p in list(enumerate(fileData)):
    px = float(p[1])
    py = float(p[2])
    for ii, pp in list(enumerate(fileData)):
        if i == ii:
            continue
        ppx = float(pp[1])
        ppy = float(pp[2])
        connections.append([i, ii, distance.euclidean((px, py), (ppx, ppy))])

for c in connections:
    print(str(c[0]) + "," + str(c[1]) + "," + str(c[2]))