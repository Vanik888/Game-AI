import pygame, sys
from tGame import TGame

class TExplorerNode:
    """ Representation of each board (game state) on the screeen """

    def __init__(self, explorer, tnode):
        self.parent = explorer
        self.node = tnode
        self.rect = pygame.Rect(0, 0, self.parent.nodeWidth, self.parent.nodeWidth)
        self.bgColorMouseOver = (230, 230, 200)
        self.bgColorWinCross = (200, 255, 200)
        self.bgColorWinNought = (255, 200, 200)
        self.bgColorWinDraw = (150, 150, 150)
        self.chosen = False if tnode.parent else True
        self.mouseOver = False
        self.gameStatus = TGame(self.node.state).gameStatus

    def draw(self, screen):
        w = self.parent.nodeWidth
        iw = (w - 2) / 3
        iw2 = iw * 2
        iwh = iw / 2
        p = self.parent.nodePadding
        pO = int(1.6 * p / 2)
        x = self.rect.left
        y = self.rect.top

        def fillBG(clr):
            pygame.draw.rect(screen, clr, (x, y, w, w), 0)
        def drawGrid():
            pygame.draw.line(screen, (0, 0, 0), (x + iw, y), (x + iw, y + w - 1))
            pygame.draw.line(screen, (0, 0, 0), (x + iw2, y), (x + iw2, y + w - 1))
            pygame.draw.line(screen, (0, 0, 0), (x, y + iw), (x + w - 1, y + iw))
            pygame.draw.line(screen, (0, 0, 0), (x, y + iw2), (x + w - 1, y + iw2))
        def drawCross(i, j):
            pygame.draw.line(screen, (0, 0, 0), (x + iw * i + p, y + iw * j + p), (x + iw * (i + 1) - p, y + iw * (j + 1) - p))
            pygame.draw.line(screen, (0, 0, 0), (x + iw * i + p, y + iw * (j + 1) - p), (x + iw * (i + 1) - p, y + iw * j + p))
        def drawNought(i, j):
            pygame.draw.circle(screen, (0, 0, 0), (x + iw * i + i + iwh, y + iw * j + j + iwh), iwh - pO, 1)

        if self.mouseOver or self.chosen: fillBG(self.bgColorMouseOver)
        else:
            if self.gameStatus == 1:
                fillBG(self.bgColorWinCross)
            elif self.gameStatus == -1:
                fillBG(self.bgColorWinNought)
            elif self.gameStatus == 0:
                fillBG(self.bgColorWinDraw)

        drawGrid()
        for i in range(3):
            for j in range(3):
                s = self.node.state.mat[i, j]
                if s == 1: drawCross(i, j)
                elif s == -1: drawNought(i, j)
        return

    def onMouseOver(self, pos):
        self.mouseOver = self.rect.collidepoint(pos)
        return self

    def onMouseClick(self, pos):
        self.mouseOver = self.rect.collidepoint(pos)
        return self

class TExplorerLayer:
    """ Representation of layer (collection of nodes of the same depth) """
    
    # Creates layer of children of tnode
    @staticmethod
    def CreateLayer(explorer, tnode, number, y):
        l = TExplorerLayer(explorer, number, y)
        for i, c in enumerate(tnode.children):
            l.addNode(TExplorerNode(explorer, c))
        return l
    
    def __init__(self, explorer, number, y):
        self.parent = explorer
        self.id = number
        self.nodes = []
        self.y = y
        self.itemShift = (self.parent.width - 2 * self.parent.shiftInitX)

        self.centerNodes()

    def addNode(self, node):
        self.nodes.append(node)
        self.centerNodes()

    # Organizes nodes on the screen
    def centerNodes(self):
        self.itemShift = ((self.parent.width - 2 * self.parent.shiftInitX) - (len(self.nodes) * self.parent.nodeWidth)) / (len(self.nodes) + 1)
        for i, n in enumerate(self.nodes):
            n.rect.left = self.parent.shiftInitX + self.itemShift + i * (self.parent.nodeWidth + self.itemShift)
            n.rect.top = self.y

    def draw(self, screen):
        for n in self.nodes:
            n.draw(screen)
            
    def onMouseOver(self, pos):
        for i, n in enumerate(self.nodes):
            exnode = n.onMouseOver(pos)
            if exnode.mouseOver:
                return exnode
        return None
            
    def onMouseClick(self, pos):
        for i, n in enumerate(self.nodes):
            exnode = n.onMouseClick(pos)
            if exnode.mouseOver:
                for j, m in enumerate(self.nodes):
                    m.chosen = False
                if exnode.gameStatus == 2:
                    exnode.chosen = True
                return exnode
        return None

class TExplorer:
    """ Simple viewer of TicTacToe Game tree """
    # Everything here 'node' can be either node of tree or its representation (class 'TExplorerNode')
    
    # Constructor
    def __init__(self, t):
        self.tree = t

        self.size = self.width, self.height = (1024, 768)
        self.bgcolor = (255, 255, 230)
        self.nodeBGColor = (200, 255, 200)
        
        self.shiftInitX = 15
        self.shiftInitY = 15
        self.shiftY = 15

        self.nodeWidth = 56
        self.nodePadding = 4

        self.layers = []
        
    # Handle keyboard/mouse events
    def eventHandlerLoop(self):
        # process key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
        	        sys.exit()
            if event.type == pygame.MOUSEMOTION:
                self.render()
                pos = pygame.mouse.get_pos()
                for i, l in enumerate(self.layers):
                    exnode = l.onMouseOver(pos)
                    if exnode and exnode.mouseOver:
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                self.render()
                pos = pygame.mouse.get_pos()
                for i, l in enumerate(self.layers):
                    exnode = l.onMouseClick(pos)
                    if exnode:
                        self.updateLayers(exnode.node)
                        break
    
    # It is called from mouse clicks on explorerNodes. Removes unnecessary layers and adds layer of children of current node
    def updateLayers(self, node):
        if len(node.children) == 0: return

        depth = 0
        par = node.parent
        while par:
            par = par.parent
            depth += 1

        if len(self.layers) > depth + 1:
            self.layers = self.layers[:depth + 1]
            
        self.layers.append(TExplorerLayer.CreateLayer(self, node, 0, self.shiftInitY + (depth + 1) * (self.nodeWidth + self.shiftY)))

        return

    # Main function, which starts viewer
    def run(self):
        pygame.init()            
        self.screen = pygame.display.set_mode(self.size)

        self.clock = pygame.time.Clock()
        #pygame.key.set_repeat(1,1)

        self.layers.append(TExplorerLayer(self, 0, self.shiftInitY))
        self.layers[-1].addNode(TExplorerNode(self, self.tree.root))
        
        self.updateLayers(self.tree.root)
        
        while 1:
            self.clock.tick(60)
            self.eventHandlerLoop()
            

            ############ <Main loop> ############
            ############ </Main loop> ############
            


            # No need to redraw everything at each tick. render() 'hooks' are placed in eventHandler function
            ############ <Render> ############
            #self.render()
            ############ </Render> ############

    # Render function - draw BG and layers
    def render(self):
        self.screen.fill(self.bgcolor)
                
        for l in self.layers:
            l.draw(self.screen)

        pygame.display.flip()