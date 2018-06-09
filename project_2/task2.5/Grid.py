import numpy as np

# class that represents a node of the graph
class Node:
	def __init__(self, i=0, j=0):
		self.i = i
		self.j = j
		self.tuple = (i, j)

		self.score = float('inf') # initially the score is infinite

	def __cmp__(self, other): # within the priority queue the nodes are compared by their score
		return cmp(self.score, other.score)

	def __eq__(self, other): # the nodes are equal if their coordinates are equal
		return self.i == other.i and self.j == other.j

	def setScore(self, score):
		self.score = score

class Grid:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.obstacleGrid = np.zeros((self.rows, self.cols), dtype = bool) # grid that represents obstacles
		self.costGrid = np.zeros((self.rows, self.cols), dtype = float) # grid that contains cost function values
		self.heuristicGrid = np.zeros((self.rows, self.cols), dtype = float) # grid that contains heuristic values
		self.openGrid = np.zeros((self.rows, self.cols), dtype = bool) # grid that shows if the node is in open list
		self.closedGrid = np.zeros((self.rows, self.cols), dtype = bool) # grid that shows if the node is in closed list
		self.predecessorGrid = np.zeros((self.rows, self.cols), dtype=np.object) # grid that contains pointer to the node's predecessor

		self.costGrid.fill(float('inf')) # cost grid is initialized with the highest value possible


	# reads the file and sets up the obstacle grid
	def setObstacleGrid(self, fname):
		f = open(fname, 'r')
		for i, line in enumerate(f):
			for j, symbol in enumerate(line):
				if j%2 == 0: # %2 and /2 because of spaces between symbols in the file
					if symbol == '1':
						self.obstacleGrid[i, j/2] = True
					elif symbol == '0':
						self.obstacleGrid[i, j/2] = False
		f.close()

	def setCost(self, i, j, cost):
		self.costGrid[i, j] = cost
	def setHeuristic(self, i, j, heuristic):
		self.heuristicGrid[i, j] = heuristic
	def setInOpen(self, i, j):
		self.openGrid[i, j] = True
	def setInClosed(self, i, j):
		self.closedGrid[i, j] = True
	def setPredecessor(self, i, j, node):
		self.predecessorGrid[i, j] = node

	def getObstacle(self, i, j):
		return self.obstacleGrid[i, j]
	def getCost(self, i, j):
		return self.costGrid[i, j]
	def getHeuristic(self, i, j):
		return self.heuristicGrid[i, j]
	def isInOpen(self, i, j):
		return self.openGrid[i, j]
	def isInClosed(self, i, j):
		return self.closedGrid[i, j]
	def getPredecessor(self, i, j):
		return self.predecessorGrid[i, j]

	# function computes amount of expanded nodes
	def expandedNodes(self):
		counter = 0
		for i in range(self.rows):
			for j in range(self.cols):
				if self.isInClosed(i, j):
					counter += 1
		return counter