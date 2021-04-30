
class UndirectedGraph:
    def __init__(self,filename=None):
        self.numNodes = 0
        self.numVertices = 0
        self.graph = {}
        self.vertices = {}
        if filename:
            with open(filename,'r') as fd:
                lines = [s for s in fd.read().split('\n')[2:] if s]
                for line in lines:
                    nodeA, nodeB, weight = line.split(' ')
                    self.add(int(nodeA),int(nodeB),float(weight))
            
    def __contains__(self, vw):
        if type(vw) is tuple:
            v, w = vw[0], vw[1]
            return (v,w) in self.vertices or (w,v) in self.vertices
        else:
            return vw in self.graph

    def __getitem__(self, vw):
        v, w = vw[0], vw[1]
        if (v,w) in self.vertices: return self.vertices[v,w]
        elif (w,v) in self.vertices: return self.vertices[w,v]
        else: return None

    def __setitem__(self, vw, weight):
        v, w = vw[0], vw[1]

        if v not in self: self.numNodes += 1
        if w not in self: self.numNodes += 1
        if (v,w) not in self: self.numVertices += 1

        if v not in self.graph: self.graph[v] = {}
        if w not in self.graph: self.graph[w] = {}
        self.graph[v][w] = weight
        self.graph[w][v] = weight

        if (w,v) in self.vertices: self.vertices[w,v] = weight
        else: self.vertices[v,w] = weight

    def add(self, v, w, weight=0):
        self[v, w] = weight

    def __delitem__(self, vw):
        if vw not in self: return

        v, w = vw[0], vw[1]
        del self.graph[v][w]
        del self.graph[w][v]

        if (v,w) in self.vertices: del self.vertices[v,w]
        else: del self.vertices[w,v]

        self.numVertices -= 1
        if not self.graph[v]: 
            del self.graph[v]
            self.numNodes -= 1
        if not self.graph[w]: 
            del self.graph[w]
            self.numNodes -= 1

    def remove(self, v, w):
        del self[v, w]

    def __iter__(self):
        return ((v,w) for v,w in self.vertices)

    def adjacent(self, v):
        return (w for w in self.graph[v])

    def __str__(self):
        out = ['Number of Nodes: ', str(self.numNodes), 
            '\nNumber of Edges: ', str(self.numVertices), '\n']
        for v,w in self:
            out.extend([str(v),'-',str(w),': ',str(self[v,w]),'\n'])
        return ''.join(out)

if __name__ == '__main__':
    graph = UndirectedGraph('4Vdense.txt')

    del graph[3,1]
    del graph[2,1]

    print(graph)
    print(graph[3,2])
    print(graph[3,1])
    print(1 in graph)
    print(graph.numNodes)
    print(graph.numVertices)