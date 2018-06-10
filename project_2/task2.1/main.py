import numpy as np
from tGame import TGame
from tTree import TNode, TTree
import time, os
import pickle
from treeExplorer import TExplorer
import matplotlib.pyplot as plt

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

# Function to show pie charts
def showHistogram(h, title):
    labels = np.array(['Draw', 'Cross', 'Not finished', 'Nought'])
    sizes = np.array(h)
    colors = np.array(['gold', 'yellowgreen', 'lightcoral', 'lightskyblue'])

    nEmpty = np.where(sizes > 0)
    sizes = sizes[nEmpty]
    labels = labels[nEmpty]
    colors = colors[nEmpty]

    plt.pie(sizes, labels=labels, colors=colors,
            autopct=lambda(p): '{:.0f} ({:.0f}%)'.format(p * np.sum(sizes) / 100, p), shadow=True, startangle=140)
    plt.axis('equal')
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    
    DEPTH = 9 # Depth of game tree: 9 - max
    STATISTICS = False # use 'stat=True' to retrieve statistics information during loading from disk (slow)
    
    wasBuilt = False
    tree = TTree(DEPTH)
    filename = 'tree' + str(DEPTH) + '.ttt'
    if os.path.isfile(filename):
        # Block for loading tree from disk
        print('Loading tree from file... (depth = ' + str(tree.maxDepth) + ')')
        ts = time.time()
        tree = TTree.Open(path='tree'+str(tree.maxDepth)+'.ttt', stat=STATISTICS) 
        print('-> ' + str(time.time() - ts))
    else:
        wasBuilt = True
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
    
    if wasBuilt or STATISTICS:
        print('Number of nodes: ' + str(tree.uidCnt))
        print('WhoWon histogram: ' + str(tree.whoWonCnt))
        print('AVG branching factor (wo\leaves): ' + str(tree.branchingFactor))

        h = tree.whoWonCnt
        showHistogram([h[0], h[1], h[2], h[-1]], 'All nodes')
        showHistogram([h[0], h[1], 0, h[-1]], 'Leaves')
    
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
