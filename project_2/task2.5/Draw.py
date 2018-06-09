from Tkinter import *


class Draw:
	def __init__(self, rows, cols, cellSize=20):
		self.rows = rows
		self.cols = cols

		self.cellSize = cellSize # parameter stands for the size of the window
		self.canvas_width = (self.cols + 1) * cellSize
		self.canvas_height = (self.rows + 1) * cellSize
		self.offset = int(cellSize/2)

		self.w = Canvas(Tk(), 
		   width=self.canvas_width,
		   height=self.canvas_height)
		self.w.pack()

	def drawGrid(self): # draws the lines of the grid
		for i in range(self.rows + 1):
			self.w.create_line(self.offset, self.offset + self.cellSize*i, self.canvas_width - self.offset, self.offset + self.cellSize*i, fill='#000000')
		for i in range(self.cols + 1):
			self.w.create_line(self.offset + self.cellSize*i, self.offset, self.offset + self.cellSize*i, self.canvas_height - self.offset, fill='#000000')

	def mat2grid(self, x): # converts matrix coordinates to grid coordinates
		return x*self.cellSize + self.offset

	def mat2cell(self, x): # converts matrix coordinates to cell coordinates
		return (x + 1)*self.cellSize

	def rekt(self, x, y, color): # draws a specified rectangle
		self.w.create_rectangle(x, y, x + self.cellSize, y + self.cellSize, fill=color)

	def fillCells(self, grid, color): # fills cells with specified colors
		for i in range(self.rows):
			for j in range(self.cols):
				if grid[i, j] == True:
					self.rekt(x=self.mat2grid(j), y=self.mat2grid(i), color=color)

	def drawLine(self, path, color='black', width=3): # draws a path with lines by specified list
		for i in range(len(path) - 1):
			x = path[i]
			y = path[i+1]
			self.w.create_line(self.mat2cell(x[1]), self.mat2cell(x[0]), self.mat2cell(y[1]), self.mat2cell(y[0]), fill=color, width=width)

	def drawPoints(self, pointset, color='black', size=4): # draws a path with points by specified list
		for i in pointset:
			self.w.create_oval(self.mat2cell(i[1])-size, self.mat2cell(i[0])-size, self.mat2cell(i[1])+size, self.mat2cell(i[0])+size, fill=color, outline='')

	def loop(self):
		mainloop()