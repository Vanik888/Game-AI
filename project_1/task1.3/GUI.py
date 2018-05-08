#! /usr/bin/env python3

from Tkinter import *
from connect_four_game import ConnectFourGame

class GUI:
    elementSize = 50
    gridBorder = 3
    gridColor = "#AAA"
    p1Color = "#4096EE"
    p2Color = "#FF1A00"
    backgroundColor = "#FFFFFF"
    gameOn = False
    
    def __init__(self, master):
        self.master = master

        master.title('Connect Four')
        
        label = Label(master, text="Connect Four")
        label.grid(row=0)

        button = Button(master, text="New Game!", command=self._newGameButton)
        button.grid(row=1)
        
        self.canvas = Canvas(master, width=200, height=50, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=2)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=3)

        self.canvas.bind('<Button-1>', self._canvasClick)
        self.newGame()

    def draw(self):       
        for c in range(self.game.game_state.shape[1]):
            for r in range(self.game.game_state.shape[0]):
                if r >= self.game.game_state.shape[1]: continue

                if self.game.game_state[r,c] == 0: continue
                x0 = c*self.elementSize
                y0 = (6 - r)*self.elementSize
                x1 = (c+1)*self.elementSize
                y1 = (6 - r-1)*self.elementSize
                fill = self.p1Color if self.game.game_state[r, c] == 1 else self.p2Color
                self.canvas.create_oval(x0 + 2,
                                        self.canvas.winfo_height() - (y0 + 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 - 2),
                                        fill = fill, outline=self.gridColor)

    def drawGrid(self):
        x0, x1 = 0, self.canvas.winfo_width()
        for r in range(1, self.game.game_state.shape[0]):
            y = r*self.elementSize
            self.canvas.create_line(x0, y, x1, y, fill=self.gridColor)

        y0, y1 = 0, self.canvas.winfo_height()
        for c in range(1,self.game.game_state.shape[1]):
            x = c*self.elementSize
            self.canvas.create_line(x, y0, x, y1, fill=self.gridColor)

    def drop(self, column):
        self.game.make_move(self.player, column)

    def newGame(self):
        # Ask for players' names
        self.p1 = 'Blue'
        self.p2 = 'Red'

        self.player = 1

        self.game = ConnectFourGame()

        self.canvas.delete(ALL)
        self.canvas.config(width=(self.elementSize)*self.game.game_state.shape[1],
                           height=(self.elementSize)*self.game.game_state.shape[0])

        self.master.update() # Rerender window
        self.drawGrid()
        self.draw()

        self._updateCurrentPlayer()

        self.gameOn = True

    def _updateCurrentPlayer(self):
        p = self.p1 if self.player == 1 else self.p2
        self.currentPlayerVar.set('Current player: ' + p)

    def _canvasClick(self, event):
        if not self.gameOn: return
        if not self.game.move_still_possible(): return
        
        c = event.x // self.elementSize
        
        if (0 <= c < self.game.game_state.shape[1]):
            self.drop(c)
            self.draw()

        if self.game.move_was_winning_move():
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2

            winner = self.p1 if self.player == 1 else self.p2
            t = winner + ' won!'
            self.gameOn = False
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")

        if not self.game.move_still_possible():
            self.gameOn = False
            self.canvas.create_text(x, y, text="DRAW", font=("Helvetica", 32),
                                    fill="#333")

        self.player *= -1
        self._updateCurrentPlayer()

    def _newGameButton(self):
        self.newGame()

root = Tk()
app = GUI(root)

root.mainloop()
