import numpy as np
import math as m
import copy
from tGame import TGame
from graphviz import Digraph

class TNode(object):
    """description of class"""

    def __init__(self, uid = -1, s = None, p = None, ch = np.empty(0, dtype=object)):
        self.uid = uid
        self.state = s
        self.parent = p
        self.children = ch

    def toGraphViz(self, dot, depth = 0):
        def getGameStateString(S):
            symbols = {1:'X', -1:'O', 0:'--'}
            B = np.copy(S).astype(object)
            for n in [-1, 0, 1]:
                B[B==n] = symbols[n]
            res = ''
            for i in range(3):
                for j in range(3):
                    res += B[i,j] + ' '
                res += '\n'
            return res

        dot.node(str(self.uid), getGameStateString(self.state.mat))
        for c in self.children:
            c.toGraphViz(dot, depth + 1)
            dot.edge(str(self.uid), str(c.uid))

    #def __copy__(self):
    #    st = TState(self.state.mat.copy(), self.state.curPlayer)
    #    return TNode(st, self.parent, self.children.copy)


    #def __repr__(self):
    #    res = '[' + self.children.size + '{ '
    #    for i in range(self.children.size):
    #        res += self.children[i] + ' '
    #    return res + ' }'
        

class TTree(object):
    """description of class"""
    
    def __init__(self, maxDepth = float('inf')):
        self.root = TNode()
        self.maxDepth = maxDepth
        self.uidCnt = 0
        self.whoWonCnt = {-1: 0, 0: 0, 1: 0, 2: 0}
       
    def buildTree(self, game = None, depth = 0):
        """ Starting point of building tree """
        self.root = self._buildTree(None, game, depth)

    def _buildTree(self, parent, game, depth):
        game = game or TGame()

        whoWon = game._whoWon()
        self.whoWonCnt[whoWon] += 1
        if whoWon != 2 or depth >= self.maxDepth:
            leaf = TNode(self.uidCnt, game.state, parent)
            self.uidCnt += 1
            return leaf

        resNode = TNode(self.uidCnt, game.state, parent, np.empty(0, dtype=object))
        self.uidCnt += 1

        xs, ys = np.where(game.state.mat == 0)
        cnt = 0
        while cnt < xs.size:
            g = copy.copy(game)
            g.nextMove([xs[cnt], ys[cnt]])
            cnt += 1
            resNode.children = np.append(resNode.children, self._buildTree(resNode, g, depth + 1))
        
        return resNode

    def toGraphViz(self):
        dot = Digraph(comment='TicTacToe Tree (depth = ' + str(self.maxDepth))
        self.root.toGraphViz(dot)

        #dot.edges(['AB', 'AL'])
        #dot.edge('B', 'L', constraint='false')
        #print(dot.source)

        print('Rendering GraphViz...')
        dot.render('tictactoeTree'+str(self.maxDepth)+'.gv', view=False)
