from Grid import *
import Queue as Q
from math import sqrt

class Planner:
	def __init__(self, grid):
		self.grid = grid
		self.q = Q.PriorityQueue()

	# functions convert the coordinate origin from the lower left to the upper left corner and switch the axes
	def setStart(self, x=0, y=1):
		self.start = Node(i=self.grid.rows-y-1, j=x)
	def setGoal(self, x=0, y=1):
		self.goal = Node(i=self.grid.rows-y-1, j=x)

	# function runs the path planner according to the algorithm
	def plan(self):
		self.openQ = Q.PriorityQueue()
		self.openQ.put(self.start)
		self.grid.setCost(i=self.start.i, j=self.start.j, cost=0)

		while not self.openQ.empty():

			currentNode = self.openQ.get()
			self.grid.setInClosed(i=currentNode.i, j=currentNode.j)
			
			if currentNode == self.goal:
				break

			if currentNode.i > 0: # check for map borders and add run success function on the neighboring nodes
				self.success(node=Node(i=currentNode.i-1, j=currentNode.j), parent=currentNode)
			if currentNode.i < self.grid.rows-1:
				self.success(node=Node(i=currentNode.i+1, j=currentNode.j), parent=currentNode)
			if currentNode.j > 0:
				self.success(node=Node(i=currentNode.i, j=currentNode.j-1), parent=currentNode)
			if currentNode.j < self.grid.cols-1:
				self.success(node=Node(i=currentNode.i, j=currentNode.j+1), parent=currentNode)

	# function adds new nodes to the Priority Queue or updates the old ones
	def success(self, node, parent):
		if self.grid.getObstacle(node.i, node.j):
			return
		cost = self.grid.getCost(i=parent.i, j=parent.j) + 1
		if not self.grid.isInClosed(i=node.i, j=node.j):
			if self.grid.getCost(i=node.i, j=node.j) > cost:
				self.grid.setPredecessor(i=node.i, j=node.j, node=parent)
				self.grid.setCost(i=node.i, j=node.j, cost=cost)
				heuristic = self.Heuristic(node=node)
				self.grid.setHeuristic(i=node.i, j=node.j, heuristic=heuristic)
				node.setScore(cost + heuristic)
				self.openQ.put(node)

	# function computes heuristic value
	def Heuristic(self, node):
	###################         EUCLIDEAN DISTANCE
		return sqrt((node.i - self.goal.i)**2 + (node.j - self.goal.j)**2)

	###################         EUCLIDEAN DISTANCE SQUARED (GREEDY)
		# return (node.i - self.goal.i)**2 + (node.j - self.goal.j)**2

	###################         MANHATTAN DISTANCE
		# return node.i - self.goal.i + node.j - self.goal.j

	###################         DIJKSTRA
		# return 0

	# function converts nodes with predecessors to a list of tuples of coordinates
	def path(self):
		node = self.goal
		path = [node.tuple]
		while isinstance(self.grid.getPredecessor(node.i, node.j), Node):
			pred = self.grid.getPredecessor(node.i, node.j)
			path.append(pred.tuple)
			node = pred
		return path