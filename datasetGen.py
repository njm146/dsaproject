'''
DSA Project Code: Weighted Undirected Graph Dataset Generator
Code by: Nicholas Meegan

TO EXECUTE CODE: py datasetGen.py <number of vertices> <'sparse'/'dense'> <filename>

Type 'sparse' for a graph with few edges, 'dense' for a graph with many edges
Filename gives the name of the file that the dataset should be saved to
'''

#Standard Library Imports
import os
import sys
import time
import random

def main(numVert, graphType, filename):
	

	try: #Check if the file that is to be opened exists in the working directory, otherwise throw an error
		numVert = int(numVert)
	except:
		print("Error. Number of vertices should be an integer value")
		exit()

	file = open(filename, "w")

	file.write(str(numVert))

	file.write("\n") 

	if(graphType.lower() == 'sparse'):
		numEdges = numVert - 1
		file.write(str(int(numEdges)))
		file.write("\n")
		for i in range(int(numVert-1)):
			string = str(i) + " " + str(i+1) + " " + str(random.uniform(1, 5)) + "\n"
			file.write(string)

		for i in range(int(numVert-1)):
			randNum = random.uniform(0, 1)
			if(randNum <= 0.2):
				numEdges += 1
				vert1 = random.randint(0, numVert-1)
				vert2 = random.randint(0, numVert-1)
				while(vert2 == vert1 or vert2 - 1 == vert1 or vert1 -1 == vert2):
					vert2 = random.randint(0, numVert-1)
				string = str(vert1) + " " + str(vert2) + " " + str(random.uniform(1, 5)) + "\n"
				file.write(string)
		file = open(filename, "r")
		lines = file.readlines()
		lines[1] = str(numEdges) + "\n"
		file = open(filename, "w")
		file.writelines(lines)
		file.close()

	else:
		numEdges = numVert*(numVert-1)/2
		file.write(str(int(numEdges)))
		file.write("\n") 
		for i in range(int(numVert)):
			for j in range(i+1, int(numVert)):
				string = str(i) + " " + str(j) + " " + str(random.uniform(1, 5)) + "\n"
				file.write(string)
		file.close()

if __name__ == '__main__':
	try:
		numVert = sys.argv[1] #Get the number of vertices to be present in the graph
		graphType = sys.argv[2] 
		filename = sys.argv[3]
		main(numVert,graphType,filename)
	except:
		numVerts = [16384*(2**i) for i in range(8)]
		for numVert in numVerts: 
			main(numVert, 'sparse', str(numVert) + 'Vsparse.txt')
			#main(numVert, 'dense', str(numVert) + 'Vdense.txt')


