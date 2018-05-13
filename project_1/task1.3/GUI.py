#! /usr/bin/env python3

# GUI taken from https://github.com/uroshekic/connect-four

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
    singlePlayer = False
    
    def __init__(self, master):
        self.master = master

        master.title('Connect Four')

        w = Checkbutton(master, text="Single player", command=self._singlePlayer)
        w.grid(row=0)

        # label = Label(master, text="")
        # label.grid(row=0)

        button = Button(master, text="New Game!", command=self._newGameButton)
        button.grid(row=1)
        
        self.canvas = Canvas(master, width=200, height=50, background=self.backgroundColor, highlightthickness=0)
        self.canvas.grid(row=2)

        self.currentPlayerVar = StringVar(self.master, value="")
        self.currentPlayerLabel = Label(self.master, textvariable=self.currentPlayerVar, anchor=W)
        self.currentPlayerLabel.grid(row=3)

        self.canvas.bind('<Button-1>', self._canvasClick)
        self.newGame()

    """Update UI according to current game state"""
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
                                        self.canvas.winfo_height() - (y0 - 2),
                                        x1 - 2,
                                        self.canvas.winfo_height() - (y1 + 2),
                                        fill = fill, outline=self.gridColor)

    """Draw game grid"""
    def drawGrid(self):
        x0, x1 = 0, self.canvas.winfo_width()
        for r in range(1, self.game.game_state.shape[0]):
            y = r*self.elementSize
            self.canvas.create_line(x0, y, x1, y, fill=self.gridColor)

        y0, y1 = 0, self.canvas.winfo_height()
        for c in range(1,self.game.game_state.shape[1]):
            x = c*self.elementSize
            self.canvas.create_line(x, y0, x, y1, fill=self.gridColor)

    """Make a move"""
    def drop(self, column):
        return self.game.make_move(self.player, column)

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

        self.gameOn = True
        self._updateCurrentPlayer()

    """Change current player"""
    def _updateCurrentPlayer(self):
        if self.gameOn:
            p = self.p1 if self.player == 1 else self.p2
            self.currentPlayerVar.set('Current player: ' + p)
        else:
            self.currentPlayerVar.set('')

    """Handle user clicks to certain column"""
    def _canvasClick(self, event):
        if not self.gameOn: return
        if not self.game.move_still_possible(): return
        
        c = event.x // self.elementSize

        # One of the columns was clicked
        if (0 <= c < self.game.game_state.shape[1]):
            desired_row = self.drop(c)
            if desired_row == -1:
                return
            self.draw()
        # Checking is there a winner
        if self.game.move_was_winning_move():
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2

            winner = self.p1 if self.player == 1 else self.p2
            t = winner + ' won!'
            self.gameOn = False
            self.canvas.create_text(x, y, text=t, font=("Helvetica", 32), fill="#333")
            return
        # Checking whether all cells of the game matrix are occupied
        if not self.game.move_still_possible():
            x = self.canvas.winfo_width() // 2
            y = self.canvas.winfo_height() // 2
            self.gameOn = False
            self.canvas.create_text(x, y, text="DRAW", font=("Helvetica", 32),
                                    fill="#333")
            return

        self.player *= -1
        self._updateCurrentPlayer()
        if self.singlePlayer:

            self.game.make_move(self.player)
            self.draw()
            if self.game.move_was_winning_move():
                x = self.canvas.winfo_width() // 2
                y = self.canvas.winfo_height() // 2

                winner = self.p1 if self.player == 1 else self.p2
                t = winner + ' won!'
                self.gameOn = False
                self.canvas.create_text(x, y, text=t, font=("Helvetica", 32),
                                        fill="#333")
                return

            if not self.game.move_still_possible():
                x = self.canvas.winfo_width() // 2
                y = self.canvas.winfo_height() // 2
                self.gameOn = False
                self.canvas.create_text(x, y, text="DRAW",
                                        font=("Helvetica", 32),
                                        fill="#333")
                return

            self.player *= -1
            self._updateCurrentPlayer()

    def _newGameButton(self):
        self.newGame()

    def _singlePlayer(self):
        self.singlePlayer = not self.singlePlayer

root = Tk()
app = GUI(root)

root.mainloop()
