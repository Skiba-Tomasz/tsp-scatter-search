import time
import os
import matplotlib.pyplot as plt

FOLDER_NAME = str(int(time.time()*100))
DIRECTORY = "C:/Users/Tomasz/Documents/Projects/Studia/Heurystyki/scatter-search/plots/" + FOLDER_NAME + "/"

def plotPath(path, coordinates, show = False, save = False, directory = DIRECTORY):
    x = [coordinates.get(path[i])[0] for i in range (1, len(path))]
    y = [coordinates.get(path[i])[1] for i in range (1, len(path))]
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, y, 'co', markersize=2, linewidth=0.2)

    a_scale = float(max(x)) / float(100)

    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale/3,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale/3,
                  color='g', length_includes_head=True)

    xMargin = max(x)/100 * 5
    yMargin = max(y)/100 * 5

    plt.xlim(min(x) - xMargin, max(x) + xMargin)
    plt.ylim(min(y) - yMargin, max(y) + yMargin)

    if save == True:
        createDirectoryIfNotExists(directory)
        if fName == None:
            fName = str(int(time.time()*1000))
        plt.savefig(directory + fName +".png")
        if show == False:
            plt.clf() # <-- Clear canvas
    if show == True:
        plt.show()

def createDirectoryIfNotExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("Grapths at: " + folder)