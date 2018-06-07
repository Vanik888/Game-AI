import numpy as np
from tGame import TGame
from tTree import TNode, TTree
import time, os
import pickle
from treeExplorer import TExplorer

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
    
    DEPTH = 9 # Depth of game tree: 9 - max
    STATISTICS = False # use 'stat=True' to get statistics information during loading (slow)
    
    tree = TTree(DEPTH)
    filename = 'tree' + str(DEPTH) + '.ttt'
    if os.path.isfile(filename):
        # Block for loading tree from disk
        print('Loading tree from file... (depth = ' + str(tree.maxDepth) + ')')
        ts = time.time()
        tree = TTree.Open(path='tree'+str(tree.maxDepth)+'.ttt', stat=STATISTICS) 
        print('-> ' + str(time.time() - ts))
    else:
        # Block for building tree
        g = TGame()
        print('Building tree... (depth = ' + str(tree.maxDepth) + ') This may take a while')
        ts = time.time()
        tree.buildTree(g)
        print('-> ' + str(time.time() - ts))

        # Block for saving tree to disk
        print('Saving tree to the disk... (depth = ' + str(tree.maxDepth) + ')')
        ts = time.time()
        tree.save('tree'+str(tree.maxDepth)+'.ttt')
        print('-> ' + str(time.time() - ts))
    
    if STATISTICS:
        print('Number of nodes: ' + str(tree.uidCnt))
        print('WhoWon histogram: ' + str(tree.whoWonCnt))
        print('AVG branching factor: ' + str(tree.branchingFactor))

    
    # Explore tree in a viewer
    treeViewer = TExplorer(tree)
    treeViewer.run()
    

    ##### <PICKLE> #####
    ## Block for loading tree from disk
    #print('Loading tree from file... (depth = ' + str(tree.maxDepth) + ')')
    #ts = time.time()
    #with open('tree'+str(tree.maxDepth)+'.pkl') as f:
    #    tree = pickle.load(f)
    #print('-> ' + str(time.time() - ts))
    
    ## Block for saving tree to disk
    #print('Saving tree to the disk... (depth = ' + str(tree.maxDepth) + ')')
    #ts = time.time()
    #with open('tree'+str(tree.maxDepth)+'.pkl', 'w') as f:
    #    pickle.dump(tree, f)
    #print('-> ' + str(time.time() - ts))
    ##### </PICKLE> #####
    


    ## Block for creating and saving to disk visualization of tree
    #print('GraphViz...')
    #ts = time.time()
    #tree.toGraphViz()
    #print('-> ' + str(time.time() - ts))

    ## Block for testing game class
    # Game initialization
    #g = TGame()
    #while g.gameStatus == 2: # 2 means 'notFinished' - look into comment of g.gameStatus func
    #    print '%s moves' % symbols[g.state.curPlayer]
    #    g.nextMove(getRandomMove(g)) # randomly choosing next move
    #    print_game_state(g.state.mat)
    
    #if g.gameStatus == 0:
    #    print 'Game ended in a draw'
    #else:
    #    print 'Player %s wins after %s moves' % (symbols[g.state.curPlayer], g.movesCounter)
