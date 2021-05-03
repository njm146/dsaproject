import heapq
import fibheap
import random
import sys
from graph import UndirectedGraph

def __prim(graph: UndirectedGraph, initFunc, popFunc, pushFunc) -> float:
    start = random.randint(0,graph.numNodes-1)
    connections = initFunc()
    for end in graph.adjacent(start):
        pushFunc(connections,(graph[start,end],start,end))

    mst = UndirectedGraph()
    while mst.numNodes < graph.numNodes:
        weight,parent,child = popFunc(connections)
        while child in mst: 
            weight,parent,child = popFunc(connections)

        mst[parent,child] = weight

        for gchild in graph.adjacent(child):
            if gchild not in mst:
                pushFunc(connections,(graph[child,gchild],child,gchild))

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
    if len(sys.argv) != 2: exit()

    graph = UndirectedGraph(sys.argv[1])

    print('MST calculated using list: ', primWithList(graph))
    print('MST calculated using binary heap: ', primWithBinaryHeap(graph))
    print('MST calculated using Fibonacci heap: ', primWithFibonacciHeap(graph))
