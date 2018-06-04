import numpy as np
from tGame import TGame
from tTree import TNode, TTree
import time
import pickle

# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1:'X', -1:'O', 0:'--'}

# print game state matrix using symbols
def gameState2Symbols(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    return B

def print_game_state(S):
    print gameState2Symbols(S)
    
def getGameStateString(S):
    B = gameState2Symbols(S)
    res = ''
    for i in range(3):
        for j in range(3):
            res += B[i,j] + ' '
        res += '\n'
    return res

# Returns [x, y] - random position of next move
# (taking into account only free places on the board)
def getRandomMove(g):
    xs, ys = np.where(g.state.mat == 0)
    i = np.random.permutation(np.arange(xs.size))[0]
    return [xs[i], ys[i]]

if __name__ == '__main__':
    # Game initialization
    g = TGame()
    tree = TTree(2)

    # Block for building tree
    print('Building tree...')
    ts = time.time()
    tree.buildTree(g)
    print('-> ' + str(time.time() - ts))
    
    ## Block for loading tree from disk
    #print('Loading tree from file...')
    #ts = time.time()
    #with open('tree'+str(tree.maxDepth)+'.pkl') as f:
    #    tree = pickle.load(f)
    #print('-> ' + str(time.time() - ts))

    print('Number of nodes: ' + str(tree.uidCnt))
    print('WhoWon histogram: ' + str(tree.whoWonCnt))
    
    ## Block for saving tree to disk
    #print('Saving tree to the disk...')
    #ts = time.time()
    #with open('tree'+str(tree.maxDepth)+'.pkl', 'w') as f:
    #    pickle.dump(tree, f)
    #print('-> ' + str(time.time() - ts))
    
    ## Block for creating and saving to disk visualization of tree
    #print('GraphViz...')
    #ts = time.time()
    #tree.toGraphViz()
    #print('-> ' + str(time.time() - ts))

    ## Block for testing game class
    #while g.gameStatus == 2: # 2 means 'notFinished' - look into comment of g.gameStatus func
    #    print '%s moves' % symbols[g.state.curPlayer]
    #    g.nextMove(getRandomMove(g)) # randomly choosing next move
    #    print_game_state(g.state.mat)
    
    #if g.gameStatus == 0:
    #    print 'Game ended in a draw'
    #else:
    #    print 'Player %s wins after %s moves' % (symbols[g.state.curPlayer], g.movesCounter)
