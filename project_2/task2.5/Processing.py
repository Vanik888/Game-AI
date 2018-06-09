from A import *
from bresenham import bresenham
from math import sqrt
from math import exp
import operator

# functions check if the path between two points is free of obstacles
def isObstacleFree(grid, x, y):
	for point in list(bresenham(x[0], x[1], y[0], y[1])):
		if grid.obstacleGrid[point[0], point[1]] == True:
			return False
	return True

# function deletes unnecessary points from the path
def smooth(grid, path):
	i = 0
	while i < len(path)-2:
		if isObstacleFree(grid, path[i], path[i+2]):
			del path[i+1]
		else:
			i+=1
	return path


# function computes the euclidean distance between two points
def dist(x, y):
	return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

# function computes one iteration of the waypointing algorithm
def moveToTarget(x, t, speed):
	d = dist(x, t)
	if d > speed/2:
		dx = speed * (t[0] - x[0])/d
		dy = speed * (t[1] - x[1])/d
	 	return tuple(map(operator.add, x, (dx, dy))), False
	else:
		return x, True

# waypointing algorithm that makes a list of waypoints out of the path
def waypointing(path, speed):
	x = path[0]
	waypoints = [x]
	i = 1

	while True:
		if i == len(path):
			break
		while True:
			x, arrived = moveToTarget(x, path[i], speed)
			if arrived:
				break
			waypoints.append(x)
		i += 1
	return waypoints


# function checks if the point is on the grid
def inBounds(i, j, rows, cols):
	return i>=0 and i<rows and j>=0 and j<cols

# function computes a Gaussian
def Gaussian(x, y):
	sigma = 0.3
	d = (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
	if d < 1:
		sigma = 0.5
	if d < 0.7:
		sigma = 0.6
	return exp(-d/(2*sigma))

# function deviates waypoints from obstacles
def forceField(planner, waypoints, neighborhood):
	rows = planner.grid.rows
	cols = planner.grid.cols
	for point in range(len(waypoints)): # force field is only computed for waypoints
		forces = []

		for i in range(-neighborhood, neighborhood+1): # only obstacles close to the waypoint can contribute to the force field
			for j in range(-neighborhood, neighborhood+1):
				centerx = int(round(waypoints[point][0]))
				centery = int(round(waypoints[point][1]))
				x = centerx + i
				y = centery + j
				if not inBounds(x, y, rows, cols):
					continue
				if planner.grid.obstacleGrid[x, y] == True:
					power = Gaussian(waypoints[point], (x, y))
					forceX = power * (waypoints[point][0] - x)
					forceY = power * (waypoints[point][1] - y)
					forces.append((forceX, forceY))
		for force in forces:
			waypoints[point] = tuple(map(operator.add, waypoints[point], force))

	waypoints[0] = planner.goal.tuple # start and finish points remain untouched
	waypoints[-1] = planner.start.tuple

	return waypoints