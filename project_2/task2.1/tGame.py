import numpy as np
from enum import Enum

class TState(object):
    """ description of class """
    
    def __init__(self, m = np.zeros((3,3), dtype=int), cp = 1):
        self.mat = m
        self.curPlayer = cp
        
    def __repr__(self):
        return 'State: %s' % self.mat

class TGame(object):
    """ description of class """

    def __init__(self, st = TState(), mc = 0, gs = 2):
        self.state = st
        self.movesCounter = mc
        self.gameStatus = gs

    def __repr__(self):
        return 'State: %s' % self.state.mat

    def __copy__(self):
        st = TState(self.state.mat.copy(), self.state.curPlayer)
        return TGame(st, self.movesCounter, self.gameStatus)

    # Return TRUE if there is no more place to move
    def _boardIsFull(self):
        S = self.state.mat
        return S[S == 0].size == 0
    
    # Return TRUE if player 'p' won and FALSE otherwise
    def _ifPlayerWon(self, p):
        S = self.state.mat
        if np.max((np.sum(S, axis=0)) * p) == 3:
            return True
        if np.max((np.sum(S, axis=1)) * p) == 3:
            return True
        if (np.sum(np.diag(S)) * p) == 3:
            return True
        if (np.sum(np.diag(np.rot90(S))) * p) == 3:
            return True
        return False
        
    # Return 1 if 'X' won, -1 if 'O' won and 0 if there is no winning combination
    def _whoWon(self):
        S = self.state.mat
        if self._ifPlayerWon(1): return 1
        if self._ifPlayerWon(-1): return -1
        if self._boardIsFull(): return 0
        return 2    

    # Return 1 if 'X' won, -1 if 'O' won, 0 for a draw and 2 if the game is not finished yet
    def _curPlayerWon(self):
        if self._ifPlayerWon(self.state.curPlayer): return self.state.curPlayer
        if self._boardIsFull(): return 0
        return 2

    # Implementation of making turns by tic-tac-toe rules
    # Returns FALSE if the move is invalid
    def nextMove(self, pos):
        if self.state.mat[pos[0], pos[1]] == 0:
            self.state.mat[pos[0], pos[1]] = self.state.curPlayer
            self.movesCounter += 1
            self.gameStatus = self._curPlayerWon()
            if self.gameStatus == 2:
                self.state.curPlayer *= -1
            return True
        return False