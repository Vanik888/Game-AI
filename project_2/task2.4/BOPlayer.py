import numpy as np

class BOPlayer(object):
    """ PLayer for Breakout """
    
    def __init__(self, maxDepth = 3, freq = 10, DBG = False):
        self.game = None
        self.maxDepth = maxDepth
        self.lastBallRect = None
        self.freq = np.inf if freq is None else freq
        self.dir = 0
        self.DBG = DBG

    def debug(self):
        return

    def move(self):
        if self.game is None: return

        if self.lastBallRect is not None:
            if (np.absolute(self.dir) > self.game.bat_speed):
                self.game.batrect = self.game.batrect.move(self.game.bat_speed * np.sign(self.dir), 0)
    
    # This function starts recursively tracing rays and saves the last x coordinate in self.dir
    def calculate(self):
        if self.lastBallRect is not None:
            self.game.DBGlines = []
            self.dir = self.traceBall() - self.game.batrect.centerx
        self.lastBallRect = self.game.ballrect

    # Entry point of recursion
    def traceBall(self):
        ray = {'o': [self.lastBallRect.centerx, self.lastBallRect.centery], \
               'p': [self.game.ballrect.centerx, self.game.ballrect.centery] }
        return self.game.ballrect.centerx if self.maxDepth == 0 else self.traceRay(ray, 0)[0]
    
    # Recursion function
    def traceRay(self, ray, depth):
        if depth >= self.maxDepth: return None
        
        normal = [0, 1]
        # Check intersection with bat line
        point = self.intersectRayInterval(ray, [[0, self.game.batrect.top], [self.game.width, self.game.batrect.top]])
        if point is not None:
            if self.DBG:
                self.game.DBGlines.append([ray['o'], point])
            return point
        
        # Check intersection with bricks
        if point is None: 
            point, normal = self.intersectionPointBallWalls(ray)

        # Check intersection with boundaries
        if point is None: point, normal = self.intersectRayInterval(ray, [[0, self.game.panelHeight], [self.game.width, self.game.panelHeight]]), [0, -1] # top
        if point is None: point, normal = self.intersectRayInterval(ray, [[0, 0], [0, self.game.height]]), [1, 0] # left
        if point is None: point, normal = self.intersectRayInterval(ray, [[self.game.width, 0], [self.game.width, self.game.height]]), [-1, 0] # right

        if point is None:
            return self.game.batrect.center

        if self.DBG:
            self.game.DBGlines.append([ray['o'], point])

        d = np.array(ray['p'])-np.array(ray['o'])
        n = np.array(normal)
        newDir = d - 2 * np.dot(d, n) * n
        newRay = {'o': point, 'p': (point + np.array(newDir)).tolist()}
        p = self.traceRay(newRay, depth + 1)
        return point if p is None else p

    def dstSqr(self, p1, p2):
        return np.power(p2[0] - p1[0], 2) + np.power(p2[1] - p1[1], 2)

    # Intersect ray with walls (collection of bricks). Returns point of intersection and normal
    def intersectionPointBallWalls(self, ray):
        n = None
        pt = None
        dst = np.inf
        for brick in self.game.wall.brickrect:
            point, normal = self.intersectRayBrick(ray, brick)
            if point is None: continue
            t = self.dstSqr(ray['o'], point)
            if t < dst: pt, dst, n = point, t, normal

        return pt, n

    # Intersect ray with brick
    def intersectRayBrick(self, ray, brick):
        # intersecting all edges of rectangle
        top = self.intersectRayInterval(ray, [brick.topleft, brick.topright])
        left = self.intersectRayInterval(ray, [brick.topleft, brick.bottomleft])
        bottom = self.intersectRayInterval(ray, [brick.bottomleft, brick.bottomright])
        right = self.intersectRayInterval(ray, [brick.topright, brick.bottomright])

        if top is None and left is None and bottom is None and right is None: return None, None

        # pick closest point
        pt, n = top, [0, 1]
        dst = np.inf if top is None else self.dstSqr(top, ray['o'])

        t = np.inf if left is None else self.dstSqr(left, ray['o'])
        if t < dst: pt, dst, n = left, t, [-1, 0]
            
        t = np.inf if bottom is None else self.dstSqr(bottom, ray['o'])
        if t < dst: pt, dst, n = bottom, t, [0, -1]
            
        t = np.inf if right is None else self.dstSqr(right, ray['o'])
        if t < dst: pt, dst, n = right, t, [1, 0]

        return pt, n

    # Intersect ray with interval
    def intersectRayInterval(self, ray, interval, tmin = 1e0):
        def getLineMlts(r):
            return {'a': r['p'][1] - r['o'][1],\
                    'b': r['o'][0] - r['p'][0],\
                    'c': r['o'][1]*(r['p'][0]-r['o'][0])-r['o'][0]*(r['p'][1]-r['o'][1])\
                    }

        # Get intersection point between 2 lines
        pos = self.intersectLineLine(getLineMlts(ray), getLineMlts({'o': interval[0], 'p': interval[1]}))
        if pos is None: return None # lines are parallel

        # Check if point in interval
        v1 = np.array(interval[0]) - np.array(pos)
        v2 = np.array(interval[1]) - np.array(pos)
        if np.dot(v1, v2) > 0: return None # out of interval

        # Check if point in front of ray
        v = np.array(pos) - np.array(ray['o'])
        if np.dot(np.array(ray['p']) - np.array(ray['o']), v) < 0: return None # behind the ray

        dst = np.array(pos) - np.array(ray['o'])
        if dst.dot(dst) < tmin * tmin: return None # it is the same edge!

        return pos
            
    # Intersect 2 lines
    def intersectLineLine(self, l1, l2):
        def det(a, b, c, d):
            return a * d - b * c
        zn = det(l1['a'], l1['b'], l2['a'], l2['b']);
        if np.abs(zn) < 1e-6: return None
        return [-det(l1['c'], l1['b'], l2['c'], l2['b']) / zn, -det(l1['a'], l1['c'], l2['a'], l2['c']) / zn]