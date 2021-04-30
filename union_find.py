
class UF:
    def __init__(self):
        self.unions = {}
        self.sizes = {}
        self.maxSize = 0

    def add(self,i):
        self.unions[i] = i
        self.sizes[i] = 1
        if not self.maxSize: self.maxSize = 1

    def root(self,i):
        if i != self.unions[i]: 
            self.unions[i] = self.root(self.unions[i])
        return self.unions[i]

    def find(self,p,q):
        if p not in self.unions: self.add(p)
        if q not in self.unions: self.add(q)
        return self.root(p) == self.root(q)

    def union(self,p,q):
        if p not in self.unions: self.add(p)
        if q not in self.unions: self.add(q)
        i = self.root(p)
        j = self.root(q)
        if self.sizes[i] < self.sizes[j]:
            self.unions[i] = j
            self.sizes[j] += self.sizes[i]
        else:
            self.unions[j] = i
            self.sizes[i] += self.sizes[j]
        self.maxSize = max(self.maxSize,self.sizes[i],self.sizes[j])
