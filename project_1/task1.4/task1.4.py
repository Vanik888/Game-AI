from Tkinter import Tk, Canvas, BOTH
from math import sin, cos, radians
from random import choice, randint

class Breakout(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('400x400')
        self.resizable(0,0)

        # game screen
        self.canvas = Canvas(self, bg='black', width=400, height=400)
        self.canvas.pack(expand=1, fill=BOTH)

        # ball
        self._initiate_new_ball()

        # paddle
        self.canvas.create_rectangle(175,375,225,385, fill='black',
                                     outline='white', tags='paddle')
        self.bind('<Key>', self._move_paddle)

        # bricks
        self.bricks = {}
        brick_coords = [5,5,35,15]
        for i in range(39):
            self.canvas.create_rectangle(*brick_coords, outline='white',
                                         fill=('#{}'.format(randint(100000,999999))),
                                         tags='brick' + str(i))
            self.bricks['brick' + str(i)] = None
            brick_coords[0] += 30; brick_coords[2] += 30
            if brick_coords[2] > 395:
                brick_coords[0] = 5; brick_coords[2] = 35
                brick_coords[1] += 10; brick_coords[3] += 10

    def _initiate_new_ball(self):
        if self.canvas.find_withtag('ball'):
            self.canvas.delete('ball')
        self.x = 60; self.y = 100
        self.angle = 140; self.speed = 5
        self.canvas.create_oval(self.x,self.y,self.x+10,self.y+10,
                                fill='lawn green', outline='white', tags='ball')
        self.after(1000, self._move_ball)

    def _move_paddle(self, event):
        if event.keysym == 'Left':
            if self.canvas.coords('paddle')[0] > 0:
                self.canvas.move('paddle', -10, 0)
        elif event.keysym == 'Right':
            if self.canvas.coords('paddle')[2] < 400:
                self.canvas.move('paddle', +10, 0)

    def _move_ball(self):

        # variables to determine where ball is in relation to other objects
        ball = self.canvas.find_withtag('ball')[0]
        bounds = self.canvas.find_overlapping(0,0,400,400)
        paddle = self.canvas.find_overlapping(*self.canvas.coords('paddle'))
        for brick in self.bricks.iterkeys():
            self.bricks[brick] = self.canvas.find_overlapping(*self.canvas.bbox(brick))

        # calculate change in x,y values of ball
        angle = self.angle - 90 # correct for quadrant IV
        increment_x = cos(radians(angle)) * self.speed
        increment_y = sin(radians(angle)) * self.speed

        # finite state machine to set ball state
        if ball in bounds:
            self.ball_state = 'moving'
            for brick, hit in self.bricks.iteritems():
                if ball in hit:
                    self.ball_state = 'hit_brick'
                    delete_brick = brick
                elif ball in paddle:
                    self.ball_state = 'hit_wall'
        elif ball not in bounds:
            if self.canvas.coords('ball')[1] < 400:
                self.ball_state = 'hit_wall'
            else:
                self.ball_state = 'out_of_bounds'
                self._initiate_new_ball()

        # handler for ball state
        if self.ball_state is 'moving':
            self.canvas.move('ball', increment_x, increment_y)
            self.after(15, self._move_ball)
        elif self.ball_state is 'hit_brick' or self.ball_state is 'hit_wall':
            if self.ball_state == 'hit_brick':
                self.canvas.delete(delete_brick)
                del self.bricks[delete_brick]
            self.canvas.move('ball', -increment_x, -increment_y)
            self.angle += choice([119, 120, 121])
            self._move_ball()

game = Breakout()
game.mainloop()