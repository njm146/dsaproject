'''
DSA Project Code: Prim's and Kruskal's Algorithms
Code by: Christopher Rosenberger and Nicholas Meegan

TO EXECUTE CODE: py dsaProject.py <inputFileName>

'inputFileName' specifies the dataset being used this run, ensure to specify file type along with name (ex: dense4vert.txt)
'''

#Standard Library Imports
import os
import sys
import time
import heapq #Used for implementing the priority queue

#CLASS DEFINITIONS


class undirectedGraph: #Class for creating an undirected graph, which is implemented as an adjacency list

	def __init__(self, numVertices): #Setup for the graph object, which contains the number of vertices in the graph, the number of edges in the graph, as well as the adjacency list which contains the vertices connected to the given vertex along with the edge weight
		self.numVertices = numVertices #Intially the number of vertices in the graph exist, with no edges connecting them.
		self.numEdges = 0 #Initially zero edges in the graph
		self.adjacencyList = [None] * numVertices #Initialize the adjacency list; at the start, no edges so the adjacency list is empty


	#Method for adding a vertex to the adjacency list of another vertex - effectively creating a directed edge between the two along with the edge weight
	def putInAdjacency(self, vertexOne, vertexTwo, edgeWeight):
		if(self.adjacencyList[vertexOne] == None): #If there is no neighboring vertices at the vertex, create a new linked list at this node
			self.adjacencyList[vertexOne] = Node(vertexTwo, edgeWeight) #Create an edge between the two vertices
		else:
			curr = self.adjacencyList[vertexOne]
			while(curr.next != None): #Otherwise, loop through the linked list until an empty location is found at the end of the chain
				curr = curr.next

			curr.next = Node(vertexTwo, edgeWeight) #Insert the edge at the end of the current chain
		return

	#Method for adding an edge to the undirected graph, which just consists of adding the vertices in each other's positions in the adjacency list
	def addEdge(self, vertexOne, vertexTwo, edgeWeight):
		self.putInAdjacency(vertexOne, vertexTwo, edgeWeight)
		self.putInAdjacency(vertexTwo, vertexOne, edgeWeight)
		self.numEdges = self.numEdges + 1 #Update the total number of edges in the graph
		return

	#Method for printing the graph along with important information regarding the graph, used strictly for testing
	def printGraph(self):
		print("Number of Vertices in Graph:", self.numVertices)
		print("Number of Edges in Graph:", self.numEdges)
		print("")


		for i in range(self.numVertices): #Loops through the adjacency lists to obtain the edges
			firstVertex = i
			secondVertex = self.adjacencyList[i]
			while(secondVertex != None):
				print(firstVertex, "-->", secondVertex.vertex, "with edge weight", secondVertex.edgeWeight)
				secondVertex = secondVertex.next

		return



class Node: #Class for creating a Linked List Node, which contains links to the next element in the list for the adjacency list, as well as the vertex and corresponding edge weight

	def __init__(self, vertex, edgeWeight): #Setup for the Linked List Node object, which contains the vertex to be inserted into the linked list along with its edge weight, as well as references to the next node (initially none)
		self.vertex = vertex
		self.edgeWeight = edgeWeight
		self.next = None
	

class QuickUnionWeight: #Class for implementing the Union Find algorithm, which is made use of in Kruskal's algorithm
	pairID = [] #List which keeps track of all of the pairs in the array of size N through the values at each index
	sizeID = []

	def __init__(self, N): #Setup for the QuickFind object, including the size of the array and the initialization of the array which keeps track of connections as well as an array that keeps track of size for tree balancing
		self.N = N
		i = 0

		for i in range(1, N+1):
			self.pairID.append(i) #Set each index to the corresponding value ranging from 1 - N (i.e. index 0 gets value 1... index N gets value N+1)
			self.sizeID.append(1) #Initialize the size array to be all ones, to be incremented throughout the union process to ensure trees are balanced

	def getRoot(self, element): #Obtains the root index of a particular element by looping through all values until the root is reached
		while(element != self.pairID[element-1]): #The root of an index is reached when the index position of the element equals the element value itself
			element = self.pairID[element-1] #Continously set the next index to be searched as the value of the previous element
		return element

	def find(self, elementOne, elementTwo): #Method for determining whether two elements are connected by observing the elements' roots
		if(self.getRoot(elementOne) == self.getRoot(elementTwo)): #If the two elements share the same root, then the two elements are connected
			return True
		else:
			return False

	def	union(self, elementOne, elementTwo): #To perform the union of two elements in the Quick Union operation, set the root of one tree to the other. Ensures balancing by appending smaller size value root to the root of the larger tree 
		rootOne = self.getRoot(elementOne)
		rootTwo = self.getRoot(elementTwo)
		if(self.sizeID[rootOne-1] < self.sizeID[rootTwo-1]): #If the size value of the tree with root one is smaller than that of root two, then append that to the tree with the larger size, balancing the tree
			self.pairID[rootOne-1] = rootTwo
			self.sizeID[rootTwo-1] = self.sizeID[rootTwo-1] + self.sizeID[rootOne-1]
		else:
			self.pairID[rootTwo-1] = rootOne
			self.sizeID[rootOne-1] = self.sizeID[rootOne-1] + self.sizeID[rootTwo-1]
		return self.pairID

#Helper Functions

#Prim's Algorithm - O(E lg V), due to priority queue implementation scheme. Finds the minimum spanning tree, works best on dense graphs
def prim(graph):
	sortedVertexList = [] #Initialize the priority queue, which will hold the vertices along with the edge weights to reach the vertex along
	heapq.heapify(sortedVertexList)
	edgeList = [None]*graph.numVertices #Store a list of the parent vertices to compute the edges
	costList = [float('inf')]*graph.numVertices #Make a list of the costs to reach each of the vertices, initialized to infinity at the start 
	MST = [] #Stores the edges that will make up the minimum spanning tree
	MSTWeight = 0 #Stores the total cost to traverse the minimum spanning tree
	isInMST = [False]*graph.numVertices #Keeps track of the vertices that have already been added to the MST

	heapq.heappush(sortedVertexList, [0, 0]) #First, push the vertex 0 along with edge weight 0 to reach the vertex

	while(len(MST) < graph.numVertices -1): #Continue to loop until all vertices have been added to the MST
		checkVertex = True
		while(checkVertex): #Make sure that the vertex is not already in the MST
			vert = heapq.heappop(sortedVertexList) #If the vertex with the smallest edge weight is not in the MST, pop it from the priority queue 
			if(not isInMST[vert[1]]):
				checkVertex = False
		isInMST[vert[1]] = True #Mark the vertex as part of the MST
		MSTWeight += vert[0] #Increase the weight of the MST by adding the edge weight cost to travel to this vertex
		if(edgeList[vert[1]] is not None):
			MST.append([vert[0], vert[1], edgeList[vert[1]]]) #Append the vertex along with its parent and edge weight to the list of edges to traverse the MST

		neighbor = graph.adjacencyList[vert[1]] #Get all of the neighbors of the current vertex by observing the adjacency list
		while(neighbor != None): #Keep looping until all of the neighbors of the current vertex have been seen
			if(not isInMST[neighbor.vertex]): #If the current neighboring vertex is not in the MST, add it to the prioriy queue
				costList[neighbor.vertex] = neighbor.edgeWeight
				edgeList[neighbor.vertex] = vert[1]
				heapq.heappush(sortedVertexList, [neighbor.edgeWeight, neighbor.vertex])
			neighbor = neighbor.next

	#print(MST) #Displays the edges that make up the minimum spanning tree, given [edgeWeight, vertexOne, vertexTwo]
	return MSTWeight

def kruskal(graph):
	unionFind = QuickUnionWeight(graph.numVertices) #Initialize a union find object which keeps track if a path between two vertices exists already or not
	sortedEdgeList = [] #Initialize the priority queue, which will hold the edges along with the edge weights between two vertices
	MST = [] #Stores the edges that will make up the minimum spanning tree
	MSTWeight = 0 #Stores the total cost to traverse the minimum spanning tree
	for i in range(graph.numVertices): #Continue to loop until all vertices have been visited
		neighbor = graph.adjacencyList[i] #Get all of the neighbors of the input vertex by observing the adjacency list
		while(neighbor != None):
			sortedEdgeList.append([neighbor.edgeWeight, i, neighbor.vertex]) #Add the edge to the priority queue
			neighbor = neighbor.next
	sortedEdgeList.sort(reverse = True)
	while(len(MST) < graph.numVertices -1): #Continue looping through until the MST contains all of the vertices
		edge = sortedEdgeList.pop() #Obtain the edge with the smallest edge cost
		if(not unionFind.find(edge[1], edge[2])): #Check to see if the two vertices already form a union along some path
			unionFind.union(edge[1], edge[2]) #If they do not, perform the union operation and add the edge to the MST
			MST.append(edge)
			MSTWeight += edge[0]
	#print(MST) #Displays the edges that make up the minimum spanning tree, given [edgeWeight, vertexOne, vertexTwo]
	return MSTWeight


#MAIN METHOD
datasetFile = sys.argv[1] #Get the dataset file to be used from the command line

try: #Check if the file that is to be opened exists in the working directory, otherwise throw an error
	dataset = open(datasetFile, 'r')
except:
	print("Error: File name '", datasetFile, "' does not exist.", sep = '')
	exit()

datasetArray = dataset.read().splitlines() #Get an array made up of all of the lines in the file (Reference: https://www.geeksforgeeks.org/python-string-splitlines/)

graph = undirectedGraph(int(datasetArray[0])) #Create an undirected graph with input of the number of vertices in the graph

for i in range(2, len(datasetArray)): #Add all of the edges to the graph
	newEdge = datasetArray[i].split(' ')
	graph.addEdge(int(newEdge[0]), int(newEdge[1]), float(newEdge[2]))

#graph.printGraph()

#Run Kruskal's algorithm and print out the total weight of the MST
start = time.time_ns()
print(kruskal(graph))
end = time.time_ns()
totalTimeKruskal = end - start

#Run Prim's algorithm and print out the total weight of the MST
start = time.time_ns()
print(prim(graph))
end = time.time_ns()
totalTimePrim = end - start

#Get the time to complete both algorithms
print("")
print("Time to compute MST on graph using Kruskal: ", totalTimeKruskal, " nanoseconds", sep = '')
print("Time to compute MST on graph using Prim:    ", totalTimePrim, " nanoseconds", sep = '')