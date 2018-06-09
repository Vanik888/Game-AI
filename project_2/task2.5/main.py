from A import *
from Processing import*
import time

fname = 'simpleMap-1-20x20.txt'

num_rows = sum(1 for line in open(fname, 'r'))
num_cols = sum(1 for symbols in open(fname, 'r').readline())/2

grid = Grid(rows=num_rows, cols=num_cols)
planner = Planner(grid)

grid.setObstacleGrid(fname=fname)
planner.setStart(x=0, y=7)
planner.setGoal(x=14, y=6)

tm = time.time()
planner.plan()
tm = time.time() - tm

print 'nodes expanded:', grid.expandedNodes()
print 'elapsed time:', tm

rawpath = planner.path()


from Draw import *
###################         SMOOTHING
spath = smooth(grid=grid, path=rawpath[:])

###################         WAYPOINTING
waypoints = waypointing(path=spath, speed=0.5)

###################         FORCE FIELD
waypoints = forceField(planner=planner, waypoints=waypoints, neighborhood=2)

###################         WAYPOINTING AGAIN
waypoints = waypointing(path=waypoints, speed=0.5)

###################         DRAWING

d = Draw(rows=grid.rows, cols=grid.cols, cellSize=20)
d.drawGrid()

d.fillCells(grid=grid.obstacleGrid, color='green')
d.fillCells(grid=grid.closedGrid, color='grey')

d.drawLine(path=rawpath, color='red')
d.drawLine(path=spath, color='orange')
d.drawLine(path=waypoints, color='blue')

# d.drawPoints(pointset=waypoints, color='blue')

d.loop()