import numpy as np
import math as m
import copy
from tGame import TGame, TState
from graphviz import Digraph

class TNode(object):
    """ Node of TicTacToe Game Tree representation. Stores current state, links to parent and children. Provides save/open and toGraphViz functionality"""

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

    def save(self, fo):
        def state2string():
            res = ''
            for i in self.state.mat:
                for j in i:
                    res += str(j + 1)
            return res

        fo.write(state2string() + str(self.children.size))

        for c in self.children:
            c.save(fo)


    #def __copy__(self):
    #    st = TState(self.state.mat.copy(), self.state.curPlayer)
    #    return TNode(st, self.parent, self.children.copy)


    #def __repr__(self):
    #    res = '[' + self.children.size + '{ '
    #    for i in range(self.children.size):
    #        res += self.children[i] + ' '
    #    return res + ' }'
        

class TTree(object):
    """ Main Tree class. Stores tree itself, some statistical information and provides build-tree, save/open and toGrtaphViz functionality"""
    
    def __init__(self, maxDepth = float('inf')):
        self.root = TNode()
        self.maxDepth = maxDepth
        self.uidCnt = 0
        self.whoWonCnt = {-1: 0, 0: 0, 1: 0, 2: 0}
        self.branchingFactor = 0.0
        self.branchingCnt = 0
        self.branchingFactorLeaves = 0.0
        self.branchingCntLeaves = 0
    
    # Entry point of recursively building tree
    def buildTree(self, game = None, depth = 0):
        """ Starting point of building tree """

        self.branchingFactor = 0.0
        self.branchingCnt = 0
        self.root = self._buildTree(None, game, depth)
        self.branchingFactorLeaves = self.branchingFactor / self.branchingCntLeaves
        self.branchingFactor /= self.branchingCnt

    # Recursive function for building tree
    def _buildTree(self, parent, game, depth):
        game = game or TGame()
        self.branchingCntLeaves += 1

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
        
        self.branchingFactor += resNode.children.size
        self.branchingCnt += 1
        return resNode

    def toGraphViz(self):
        dot = Digraph(comment='TicTacToe Tree (depth = ' + str(self.maxDepth))
        self.root.toGraphViz(dot)

        #dot.edges(['AB', 'AL'])
        #dot.edge('B', 'L', constraint='false')
        #print(dot.source)

        print('Rendering GraphViz...')
        dot.render('tictactoeTree'+str(self.maxDepth)+'.gv', view=False)

    def save(self, path):
        fo = open(path, 'w')
        self.root.save(fo)
        fo.close()
        
    @staticmethod
    def Open(path, stat = False):
        def readBatch(fo):
            mat = np.zeros(9)
            st = fo.read(9)
            for i, c in enumerate(st):
                mat[i] = int(c) - 1
            return np.reshape(mat, (3, 3)), int(fo.read(1))
        def getNextNode(tree, fo, parent = None, depth = 0):
            m, chN = readBatch(fo)
            node = TNode(tree.uidCnt, TState(m), parent)
            tree.uidCnt += 1
            children = []
            for i in range(chN):
                child = getNextNode(tree, fo, node, depth + 1)
                children = np.append(children, child)
            node.children = children
            if stat:
                g = TGame(node.state)
                tree.whoWonCnt[g.gameStatus] += 1
            if chN > 0:
                tree.branchingFactor += chN
                tree.branchingCnt += 1
            tree.branchingCntLeaves += 1
            if depth > tree.maxDepth:
                tree.maxDepth = depth
            return node

        fo = open(path, 'r')
        tree = TTree()
        
        tree.uidCnt = 0
        tree.branchingFactor = 0.0
        tree.branchingCnt = 0
        tree.branchingCntLeaves = 0
        tree.maxDepth = -1
        tree.whoWonCnt = {0: 0, 1: 0, 2: 0, -1: 0}
        tree.root = getNextNode(tree, fo)
        tree.branchingFactorLeaves = tree.branchingFactor / tree.branchingCntLeaves
        tree.branchingFactor /= tree.branchingCnt


        return tree