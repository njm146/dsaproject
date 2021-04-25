import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from statistics import mean
import dsaProject

NUM_ITERATIONS = 10
DENSE_FILES = ['4Vdense.txt', '16Vdense.txt', '32Vdense.txt', '64Vdense.txt', '128Vdense.txt', '256Vdense.txt', '512Vdense.txt', '1024Vdense.txt', 
    '2048Vdense.txt', '4096Vdense.txt']
DENSE_SAVE_FILE_KRUSKAL = 'Dense Times - Kruskal.txt'
DENSE_SAVE_FILE_PRIM = 'Dense Times - Prim.txt'
SPARSE_FILES = ['4Vsparse.txt'] + [str(16*(2**i)) + 'Vsparse.txt' for i in range(18)]
SPARSE_SAVE_FILE_KRUSKAL = 'Sparse Times - Kruskal.txt'
SPARSE_SAVE_FILE_PRIM = 'Sparse Times - Prim.txt'

def loadGraph(filename):
    with open(filename,'r') as dataset:
        datasetArray = dataset.read().splitlines()
        graph = dsaProject.undirectedGraph(int(datasetArray[0]))
        for i in range(2, len(datasetArray)): #Add all of the edges to the graph
            newEdge = datasetArray[i].split(' ')
            graph.addEdge(int(newEdge[0]), int(newEdge[1]), float(newEdge[2]))
    return graph

def timeFunc(func, *args):
    def timeIter():
        start = time.time_ns()
        func(*args)
        end = time.time_ns()
        return end - start
    times = [timeIter() for _ in range(NUM_ITERATIONS)]
    return mean(times)

def saveTime(filename: str, table: dict) -> None:
    with open(filename,'w+') as file:
        for label,time in sorted(table.items(), key=lambda i:int(i[0])):
            file.write(str(label) + ': ' + str(time) + '\n')

def loadTime(filename):
    with open(filename,'r') as file:
        timeList = [[int(s.split(': ')[0]),float(s.split(': ')[1])] for s in file.read().split('\n') if s]
        timeTable = dict((n,t) for n,t in timeList)
    return timeTable

def makeGraph(filename,tables,labels,k=2,mx=float('inf')):
    handles = []
    for table,label in zip(tables,labels):
        x,y = list(table.keys()),list(table.values())
        while x[-1] > mx:
            x.pop()
            y.pop()
        xnew = np.linspace(min(x),max(x),1000)
        spl = make_interp_spline(x,y,k=k)
        ysmooth = spl(xnew)
        handles.append(plt.plot(xnew,ysmooth,label=label))
    plt.legend(handles=[fig[0] for fig in handles])
    plt.title(filename[:filename.find('.')])
    plt.xlabel('Number of Items')
    plt.ylabel('Average Time Taken (Over ' + str(NUM_ITERATIONS) + ' Trials)')
    plt.savefig(filename)
    plt.close()

def collectData():
    denseGraphs = [loadGraph(filename) for filename in DENSE_FILES]

    denseTimesKruskal = {file[:file.find('V')]: timeFunc(dsaProject.kruskal,graph) for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_KRUSKAL,denseTimesKruskal)

    denseTimesPrim = {file[:file.find('V')]: timeFunc(dsaProject.prim,graph) for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_PRIM,denseTimesPrim)

    sparseGraphs = [loadGraph(filename) for filename in SPARSE_FILES]

    sparseTimesKruskal = {file[:file.find('V')]: timeFunc(dsaProject.kruskal,graph) for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_KRUSKAL,sparseTimesKruskal)

    sparseTimesPrim = {file[:file.find('V')]: timeFunc(dsaProject.prim,graph) for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_PRIM,sparseTimesPrim)

def displayData():
    denseTimesKruskal = loadTime(DENSE_SAVE_FILE_KRUSKAL)
    denseTimesPrim = loadTime(DENSE_SAVE_FILE_PRIM)
    sparseTimesKruskal = loadTime(SPARSE_SAVE_FILE_KRUSKAL)
    sparseTimesPrim = loadTime(SPARSE_SAVE_FILE_PRIM)

    makeGraph('Kruskal Times.png', [denseTimesKruskal,sparseTimesKruskal], ['Dense','Sparse'],mx=2048)
    makeGraph('Prim Times.png', [denseTimesPrim,sparseTimesPrim], ['Dense','Sparse'],mx=2048)
    makeGraph('Kruskal v Prim (Sparse Graph).png', [sparseTimesKruskal,sparseTimesPrim], ['Kruskal','Prim'])
    makeGraph('Kruskal v Prim (Dense Graph).png', [denseTimesKruskal,denseTimesPrim], ['Kruskal','Prim'])
    makeGraph('Kruskal v Prim.png', [denseTimesKruskal,denseTimesPrim,sparseTimesKruskal,sparseTimesPrim], ['Kruskal, Dense','Prim, Dense','Kruskal, Sparse','Prim, Sparse'],mx=2048)

if __name__ == '__main__':
    #collectData()
    displayData()