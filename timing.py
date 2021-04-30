import time
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from statistics import mean
from graph import UndirectedGraph
import prim
import kruskal

NUM_ITERATIONS = 10

DENSE_FILES = ['4Vdense.txt', '16Vdense.txt', '32Vdense.txt', '64Vdense.txt', '128Vdense.txt', '256Vdense.txt', 
    '512Vdense.txt', '1024Vdense.txt', '2048Vdense.txt', '4096Vdense.txt']
SPARSE_FILES = ['4Vsparse.txt'] + [str(16*(2**i)) + 'Vsparse.txt' for i in range(18)]

DENSE_SAVE_FILE_KRUSKAL_LIST = 'Dense Times - Kruskal (list).txt'
DENSE_SAVE_FILE_KRUSKAL_BINHEAP = 'Dense Times - Kruskal (binheap).txt'
DENSE_SAVE_FILE_KRUSKAL_FIBHEAP = 'Dense Times - Kruskal (fibheap).txt'

DENSE_SAVE_FILE_PRIM_LIST = 'Dense Times - Prim (list).txt'
DENSE_SAVE_FILE_PRIM_BINHEAP = 'Dense Times - Prim (binheap).txt'
DENSE_SAVE_FILE_PRIM_FIBHEAP = 'Dense Times - Prim (fibheap).txt'

SPARSE_SAVE_FILE_KRUSKAL_LIST = 'Sparse Times - Kruskal (list).txt'
SPARSE_SAVE_FILE_KRUSKAL_BINHEAP = 'Sparse Times - Kruskal (binheap).txt'
SPARSE_SAVE_FILE_KRUSKAL_FIBHEAP = 'Sparse Times - Kruskal (fibheap).txt'

SPARSE_SAVE_FILE_PRIM_LIST = 'Sparse Times - Prim (list).txt'
SPARSE_SAVE_FILE_PRIM_BINHEAP = 'Sparse Times - Prim (binheap).txt'
SPARSE_SAVE_FILE_PRIM_FIBHEAP = 'Sparse Times - Prim (fibheap).txt'

def timeFunc(func, *args):
    def timeIter():
        start = time.time_ns()
        func(*args)
        end = time.time_ns()
        return end - start
    times = [timeIter() for _ in range(NUM_ITERATIONS)]
    return times

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
    denseGraphs = [UndirectedGraph(filename) for filename in DENSE_FILES]

    denseTimesKruskalList = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithList,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_KRUSKAL_LIST,denseTimesKruskalList)

    denseTimesKruskalBinHeap = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithBinaryHeap,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_KRUSKAL_BINHEAP,denseTimesKruskalBinHeap)

    denseTimesKruskalFibHeap = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithFibonacciHeap,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_KRUSKAL_FIBHEAP,denseTimesKruskalFibHeap)


    denseTimesPrimList = {file[:file.find('V')]: timeFunc(prim.primWithList,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_PRIM_LIST,denseTimesPrimList)

    denseTimesPrimBinHeap = {file[:file.find('V')]: timeFunc(prim.primWithBinaryHeap,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_PRIM_BINHEAP,denseTimesPrimBinHeap)

    denseTimesPrimFibHeap = {file[:file.find('V')]: timeFunc(prim.primWithFibonacciHeap,graph) 
        for file,graph in zip(DENSE_FILES,denseGraphs)}
    saveTime(DENSE_SAVE_FILE_PRIM_FIBHEAP,denseTimesPrimFibHeap)


    sparseGraphs = [UndirectedGraph(filename) for filename in SPARSE_FILES]

    sparseTimesKruskalList = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithList,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_KRUSKAL_LIST,sparseTimesKruskalList)

    sparseTimesKruskalBinHeap = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithBinaryHeap,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_KRUSKAL_BINHEAP,sparseTimesKruskalBinHeap)

    sparseTimesKruskalFibHeap = {file[:file.find('V')]: timeFunc(kruskal.kruskalWithFibonacciHeap,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_KRUSKAL_FIBHEAP,sparseTimesKruskalFibHeap)


    sparseTimesPrimList = {file[:file.find('V')]: timeFunc(prim.primWithList,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_PRIM_LIST,sparseTimesPrimList)

    sparseTimesPrimBinHeap = {file[:file.find('V')]: timeFunc(prim.primWithBinaryHeap,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_PRIM_BINHEAP,sparseTimesPrimBinHeap)

    sparseTimesPrimFibHeap = {file[:file.find('V')]: timeFunc(prim.primWithFibonacciHeap,graph) 
        for file,graph in zip(SPARSE_FILES,sparseGraphs)}
    saveTime(SPARSE_SAVE_FILE_PRIM_FIBHEAP,sparseTimesPrimFibHeap)

def displayData():
    denseTimesKruskalList = loadTime(DENSE_SAVE_FILE_KRUSKAL_LIST)
    denseTimesKruskalBinHeap = loadTime(DENSE_SAVE_FILE_KRUSKAL_BINHEAP)
    denseTimesKruskalFibHeap= loadTime(DENSE_SAVE_FILE_KRUSKAL_FIBHEAP)

    denseTimesPrimList = loadTime(DENSE_SAVE_FILE_PRIM_LIST)
    denseTimesPrimBinHeap = loadTime(DENSE_SAVE_FILE_PRIM_BINHEAP)
    denseTimesPrimFibHeap = loadTime(DENSE_SAVE_FILE_PRIM_FIBHEAP)

    sparseTimesKruskalList = loadTime(SPARSE_SAVE_FILE_KRUSKAL_LIST)
    sparseTimesKruskalBinHeap = loadTime(SPARSE_SAVE_FILE_KRUSKAL_BINHEAP)
    sparseTimesKruskalFibHeap = loadTime(SPARSE_SAVE_FILE_KRUSKAL_FIBHEAP)

    sparseTimesPrimList = loadTime(SPARSE_SAVE_FILE_PRIM_LIST)
    sparseTimesPrimBinHeap = loadTime(SPARSE_SAVE_FILE_PRIM_BINHEAP)
    sparseTimesPrimFibHeap = loadTime(SPARSE_SAVE_FILE_PRIM_FIBHEAP)

    makeGraph('Dense Kruskal Times.png', [denseTimesKruskalList,denseTimesKruskalBinHeap,denseTimesKruskalFibHeap], 
        ['List','Binary Heap', 'Fibonacci Heap'])
    makeGraph('Sparse Kruskal Times.png', [sparseTimesKruskalList,sparseTimesKruskalBinHeap,sparseTimesKruskalFibHeap], 
        ['List','Binary Heap', 'Fibonacci Heap'])
    makeGraph('Kruskal Times.png', [denseTimesKruskalList,denseTimesKruskalBinHeap,denseTimesKruskalFibHeap,
        sparseTimesKruskalList,sparseTimesKruskalBinHeap,sparseTimesKruskalFibHeap], ['Dense - List',
        'Dense - Binary Heap', 'Dense - Fibonacci Heap', 'Sparse - List','Sparse - Binary Heap', 
        'Sparse - Fibonacci Heap'],mx=2048)

    makeGraph('Dense Prim Times.png', [denseTimesPrimList,denseTimesPrimBinHeap,denseTimesPrimFibHeap], 
        ['List','Binary Heap', 'Fibonacci Heap'])
    makeGraph('Sparse Prim Times.png', [sparseTimesPrimList,sparseTimesPrimBinHeap,sparseTimesPrimFibHeap], 
        ['List','Binary Heap', 'Fibonacci Heap'])
    makeGraph('Prim Times.png', [denseTimesPrimList,denseTimesPrimBinHeap,denseTimesPrimFibHeap,sparseTimesPrimList,
        sparseTimesPrimBinHeap,sparseTimesPrimFibHeap], ['Dense - List','Dense - Binary Heap', 'Dense - Fibonacci Heap', 
        'Sparse - List','Sparse - Binary Heap', 'Sparse - Fibonacci Heap'],mx=2048)

    makeGraph('Kruskal v Prim (List - Sparse Graph).png', [sparseTimesKruskalList,sparseTimesPrimList], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Binary Heap - Sparse Graph).png', [sparseTimesKruskalBinHeap,sparseTimesPrimBinHeap], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Fibonacci Heap - Sparse Graph).png', [sparseTimesKruskalFibHeap,sparseTimesPrimFibHeap], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Sparse Graph).png', [sparseTimesKruskalList,sparseTimesKruskalBinHeap,
        sparseTimesKruskalFibHeap,sparseTimesPrimList,sparseTimesPrimBinHeap,sparseTimesPrimFibHeap], 
        ['Kruskal - List','Kruskal - Binary Heap', 'Kruskal - Fibonacci Heap', 'Prim - List',
        'Prim - Binary Heap', 'Prim - Fibonacci Heap'])
    
    makeGraph('Kruskal v Prim (List - Dense Graph).png', [denseTimesKruskalList,denseTimesPrimList], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Binary Heap - Dense Graph).png', [denseTimesKruskalBinHeap,denseTimesPrimBinHeap], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Fibonacci Heap - Dense Graph).png', [denseTimesKruskalFibHeap,denseTimesPrimFibHeap], 
        ['Kruskal', 'Prim'])
    makeGraph('Kruskal v Prim (Dense Graph).png', [denseTimesKruskalList,denseTimesKruskalBinHeap,
        denseTimesKruskalFibHeap,denseTimesPrimList,denseTimesPrimBinHeap,denseTimesPrimFibHeap], 
        ['Kruskal - List','Kruskal - Binary Heap', 'Kruskal - Fibonacci Heap', 'Prim - List',
        'Prim - Binary Heap', 'Prim - Fibonacci Heap'])
    
    makeGraph('Kruskal v Prim.png', [sparseTimesKruskalList,sparseTimesKruskalBinHeap,sparseTimesKruskalFibHeap,
        sparseTimesPrimList,sparseTimesPrimBinHeap,sparseTimesPrimFibHeap,denseTimesKruskalList,
        denseTimesKruskalBinHeap,denseTimesKruskalFibHeap,denseTimesPrimList,denseTimesPrimBinHeap,
        denseTimesPrimFibHeap], ['Dense - Kruskal - List','Dense - Kruskal - Binary Heap', 
        'Dense - Kruskal - Fibonacci Heap', 'Dense - Prim - List','Dense - Prim - Binary Heap', 
        'Dense - Prim - Fibonacci Heap', 'Sparse - Kruskal - List','Sparse - Kruskal - Binary Heap', 
        'Sparse - Kruskal - Fibonacci Heap', 'Sparse - Prim - List','Sparse - Prim - Binary Heap', 
        'Sparse - Prim - Fibonacci Heap'],mx=2048)

if __name__ == '__main__':
    collectData()
    #displayData()