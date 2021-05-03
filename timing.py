import time
import sys
from graph import UndirectedGraph
import prim
import kruskal

DENSE_FILES = ['4Vdense.txt', '16Vdense.txt', '32Vdense.txt', '64Vdense.txt', '128Vdense.txt', '256Vdense.txt', 
    '512Vdense.txt', '1024Vdense.txt', '2048Vdense.txt', '4096Vdense.txt']
SPARSE_FILES = ['4Vsparse.txt'] + [str(16*(2**i)) + 'Vsparse.txt' for i in range(18)]

def timeFunc(func, numIterations, *args):
    def timeIter():
        start = time.time_ns()
        func(*args)
        end = time.time_ns()
        return end - start
    times = [timeIter() for _ in range(numIterations)]
    return times

def saveTime(filename: str, table: dict) -> None:
    with open(filename,'w+') as file:
        for label,time in sorted(table.items(), key=lambda i:i[0]):
            file.write(str(label) + ': ' + str(time) + '\n')

def collectData(numIterations, outputFile, graphFiles):
    graphs = [UndirectedGraph(filename) for filename in graphFiles]

    times = {}
    for file,graph in zip(graphFiles,graphs):
        times[file] = {}
        times[file]['primWithList'] = timeFunc(prim.primWithList, numIterations, graph)
        times[file]['primWithBinaryHeap'] = timeFunc(prim.primWithBinaryHeap, numIterations, graph)
        times[file]['primWithFibonacciHeap'] = timeFunc(prim.primWithFibonacciHeap, numIterations, graph)
        times[file]['kruskalWithList'] = timeFunc(kruskal.kruskalWithList, numIterations, graph)
        times[file]['kruskalWithBinaryHeap'] = timeFunc(kruskal.kruskalWithBinaryHeap, numIterations, graph)
        times[file]['kruskalWithFibonacciHeap'] = timeFunc(kruskal.kruskalWithFibonacciHeap, numIterations, graph)
        saveTime(outputFile, times)    

if __name__ == '__main__':
    if len(sys.argv) < 4: exit()

    numIterations = int(sys.argv[1])
    outputFile = sys.argv[2]
    graphFiles = sys.argv[3:]
    collectData(numIterations, outputFile, graphFiles)