import heapq
import fibheap
import random
from Graph import UndirectedGraph

def __prim(graph: UndirectedGraph, initFunc, popfunc, pushfunc) -> float:
    start = random.randint(0,graph.numNodes-1)
    connections = initFunc()
    for end in graph.adjacent(start):
        pushfunc(connections,(graph[start,end],start,end))

    mst = UndirectedGraph()
    while mst.numNodes < graph.numNodes:
        weight,parent,child = popfunc(connections)
        while child in mst: 
            weight,parent,child = popfunc(connections)

        mst[parent,child] = weight

        for gchild in graph.adjacent(child):
            if gchild not in mst:
                pushfunc(connections,(graph[child,gchild],child,gchild))

    return sum(mst[vertex] for vertex in mst)

def primWithList(graph: UndirectedGraph) -> float:
    def popmin(connections: list):
        minIdx = min((i for i in range(len(connections))), key=lambda i:connections[i])
        return connections.pop(minIdx)

    return __prim(graph, list, popmin, lambda x,y:x.append(y))

def primWithBinaryHeap(graph: UndirectedGraph) -> float:
    return __prim(graph, list, heapq.heappop, heapq.heappush)

def primWithFibonacciHeap(graph: UndirectedGraph) -> float:
    return __prim(graph, fibheap.makefheap, fibheap.fheappop, fibheap.fheappush)

if __name__ == '__main__':
    graph = UndirectedGraph('4Vdense.txt')

    print(primWithList(graph))
    print(primWithBinaryHeap(graph))
    print(primWithFibonacciHeap(graph))
