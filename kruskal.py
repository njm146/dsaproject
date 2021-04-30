import heapq
import fibheap
from graph import UndirectedGraph
from union_find import UF

def __kruskal(graph: UndirectedGraph, initFunc, popFunc, pushFunc) -> float:
    connections = initFunc()
    for nodeA,nodeB in graph:
        pushFunc(connections,(graph[nodeA,nodeB],nodeA,nodeB))

    uf = UF()
    mst = UndirectedGraph()
    while uf.maxSize < graph.numNodes:
        weight,nodeA,nodeB = popFunc(connections)
        while uf.find(nodeA,nodeB): 
            weight,nodeA,nodeB = popFunc(connections)

        uf.union(nodeA,nodeB)
        mst[nodeA,nodeB] = weight

    return sum(mst[vertex] for vertex in mst)

def kruskalWithList(graph: UndirectedGraph) -> float:
    def popmin(connections: list):
        minIdx = min((i for i in range(len(connections))), key=lambda i:connections[i])
        return connections.pop(minIdx)

    return __kruskal(graph, list, popmin, lambda x,y:x.append(y))

def kruskalWithBinaryHeap(graph: UndirectedGraph) -> float:
    return __kruskal(graph, list, heapq.heappop, heapq.heappush)

def kruskalWithFibonacciHeap(graph: UndirectedGraph) -> float:
    return __kruskal(graph, fibheap.makefheap, fibheap.fheappop, fibheap.fheappush)

if __name__ == '__main__':
    graph = UndirectedGraph('4Vdense.txt')

    print(kruskalWithList(graph))
    print(kruskalWithBinaryHeap(graph))
    print(kruskalWithFibonacciHeap(graph))