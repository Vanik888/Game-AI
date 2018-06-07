#!/usr/bin/env python

#
#   Breakout V 0.1 June 2009
#
#   Copyright (C) 2009 John Cheetham    
#
#   web   : http://www.johncheetham.com/projects/breakout
#   email : developer@johncheetham.com
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#    
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, pygame, random
from BOPlayer import BOPlayer as bp
import multiprocessing
import numpy as np
import pygbutton

class Breakout():
    def __init__(self, pl):
        self.player = pl
   
    # Main function
    def main(self):
        # Restarts ball when 'reset'/ball_fell_down/game_over
        def restartBall():
            self.lives -= 1
            # start a new ball
            self.xspeed = xspeed_init
            rand = random.random()                
            if random.random() > 0.5:
                self.xspeed = -self.xspeed 
            self.yspeed = yspeed_init            
            self.ballrect.center = self.width * random.random(), self.height / 3

        # Called when game_over/'reset'
        def gameOver(reset = True):
            if reset:
                msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)
                self.screen.blit(msg, msg.get_rect().move(self.width / 2 - (msg.get_rect().center[0]), self.height / 3))
                
                msg2 = pygame.font.Font(None,35).render("Press any key to restart", True, (0,255,255), bgcolour)
                self.screen.blit(msg2, msg2.get_rect().move(self.width / 2 - (msg2.get_rect().center[0]), self.height / 3 + msg.get_rect().bottom + 32))

                pygame.display.flip()
            # Loop to detect 'press any key'
            restart = True
            while reset:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                    	    sys.exit()
                        if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                            reset = False
                            break      
                        
            self.screen.fill(bgcolour)
            self.wall.build_wall(self.width, self.yFreeShift + self.panelHeight)
            self.lives = self.max_lives + 1
            self.score = 0
            restartBall()
            pause(0)

        def tick():
            self.clock.tick(60)

        # Handle keyboard/mouse events
        def eventHandlerLoop():
            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if not self.bot:
                        if event.key == pygame.K_LEFT:                        
                            self.batrect = self.batrect.move(-self.bat_speed, 0)     
                            if (self.batrect.left < 0):                           
                                self.batrect.left = 0      
                        if event.key == pygame.K_RIGHT:                    
                            self.batrect = self.batrect.move(self.bat_speed, 0)
                            if (self.batrect.right > self.width):                            
                                self.batrect.right = self.width 
                    if event.key == pygame.K_p:  
                        #self.player.debug()
                        pygame.time.wait(100)
                        pause()
                    if event.key == pygame.K_b:
                        pygame.time.wait(100)
                        bot()
                    if event.key == pygame.K_r:
                        pygame.time.wait(100)
                        gameOver(False)
                    if event.key == pygame.K_l:
                        pygame.time.wait(100)
                        self.player.DBG = 0 if self.player.DBG else 1
                if 'click' in self.btnLines.handleEvent(event):
                    self.player.DBG = 0 if self.player.DBG else 1
                    if not self.player.DBG:
                        self.DBGlines = []
                if 'click' in self.btnReset.handleEvent(event):
                    gameOver(False)
                if 'click' in self.btnPause.handleEvent(event):
                    pause()
                if 'click' in self.btnBot.handleEvent(event):
                    bot()
                if 'click' in self.btnAccLess.handleEvent(event):
                    acc(-1)
                if 'click' in self.btnAccMore.handleEvent(event):
                    acc(1)
                if 'click' in self.btnDepthLess.handleEvent(event):
                    depth(-1)
                if 'click' in self.btnDepthMore.handleEvent(event):
                    depth(1)

        # Toggle pause
        def pause(state = -1):
            if state == -1:
                self.pause = 0 if self.pause else 1
            else:
                self.pause = state
            self.btnPause.caption = 'Resume' if self.pause else 'Pause'
            
        # Toggle bot
        def bot(state = -1):
            if state == -1:
                self.bot = 0 if self.bot else 1
            else:
                self.bot = state
            self.btnBot.caption = 'Bot OFF' if self.bot else 'Bot ON'
            #self.DBGlines = []
            
        # Change acceleration
        def acc(dir):
            if dir < 0:
                self.acc /= self.accStep
                if self.acc < 0.005: self.acc = 0
            else:
                if self.acc < 0.005: self.acc = 0.005
                else: self.acc *= self.accStep
            if self.acc > 0.16: self.acc = 0.16
            
        # Change depth
        def depth(dir):
            if dir < 0:
                self.player.maxDepth -= 1
            else:
                self.player.maxDepth += 1
            if self.player.maxDepth < 0: self.player.maxDepth = 0
            if self.player.maxDepth > 10: self.player.maxDepth = 10

        xspeed_init = 4
        yspeed_init = 4
        self.acc = 1e-2
        self.accStep = 2
        self.max_lives = 5
        self.bat_speed = 6
        self.score = 0 
        bgcolour = 0x2F, 0x4F, 0x4F  # darkslategrey    
        panelcolour = (100, 100, 100)
        self.yFreeShift = 60
        self.panelHeight = 45
        self.size = self.width, self.height = 800, 600
        self.frames = 0
        self.pause = False
        self.bot = True

        pygame.init()            
        self.screen = pygame.display.set_mode(self.size)
        #self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)

        bat = pygame.image.load("bat.png").convert()
        self.batrect = bat.get_rect()

        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey((255, 255, 255))
        self.ballrect = ball.get_rect()
       
        pong = pygame.mixer.Sound('Blip_1-Surround-147.wav')
        pong.set_volume(0)        
        
        self.wall = Wall()
        self.wall.build_wall(self.width, self.yFreeShift + self.panelHeight)

        self.player.game = self

        self.DBGlines = []

        ####### UI-Button Initialization Block #########
        self.btnFont = pygame.font.Font('freesansbold.ttf', 14)
        self.btnLines = pygbutton.PygButton(rect=(130, 0, 60, 25), caption='Lines', font=self.btnFont)
        self.btnReset = pygbutton.PygButton(rect=(self.btnLines.rect.right, 0, 60, 25), caption='Restart', font=self.btnFont)
        self.btnPause = pygbutton.PygButton(rect=(self.btnReset.rect.right, 0, 80, 25), caption='Pause', font=self.btnFont)
        self.btnBot = pygbutton.PygButton(rect=(self.btnPause.rect.right, 0, 90, 25), caption='Bot OFF', font=self.btnFont)
        self.btnAccLess = pygbutton.PygButton(rect=(self.btnBot.rect.right, 19, 30, 20), caption='<<', font=self.btnFont)
        self.btnAccMore = pygbutton.PygButton(rect=(self.btnAccLess.rect.right+62, self.btnAccLess.rect.top, 30, 20), caption='>>', font=self.btnFont)
        self.btnDepthLess = pygbutton.PygButton(rect=(self.btnAccMore.rect.right, 19, 30, 20), caption='<<', font=self.btnFont)
        self.btnDepthMore = pygbutton.PygButton(rect=(self.btnDepthLess.rect.right+30, self.btnDepthLess.rect.top, 30, 20), caption='>>', font=self.btnFont)


        # Initialise ready for game loop
        self.batrect = self.batrect.move((self.width / 2) - (self.batrect.right / 2), self.height - 20)
        self.ballrect = self.ballrect.move(self.width / 2, self.height / 2)
        self.xspeed = xspeed_init
        self.yspeed = yspeed_init
        self.lives = self.max_lives
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1,1)
        #pygame.mouse.set_visible(0)       # turn off mouse pointer

        while 1:

            # 60 frames per second
            tick()
            
            eventHandlerLoop()

            if not self.pause:

                # check if bat has hit ball    
                if self.ballrect.bottom >= self.batrect.top and \
                   self.ballrect.bottom <= self.batrect.bottom and \
                   self.ballrect.right >= self.batrect.left and \
                   self.ballrect.left <= self.batrect.right:
                    self.yspeed = -self.yspeed                
                    pong.play(0)                
                    offset = self.ballrect.center[0] - self.batrect.center[0]                          
                     #offset > 0 means ball has hit RHS of bat                   
                     #vary angle of ball depending on where ball hits bat  
                                     
                    if offset > 0:
                        if offset > 30:  
                            self.xspeed = 7
                        elif offset > 23:                 
                            self.xspeed = 6
                        elif offset > 17:
                            self.xspeed = 5 
                    else:  
                        if offset < -30:                             
                            self.xspeed = -7
                        elif offset < -23:
                            self.xspeed = -6
                        elif self.xspeed < -17:
                            self.xspeed = -5     

                      
                # move bat/ball
                self.ballrect = self.ballrect.move(self.xspeed, self.yspeed)
                if self.ballrect.left < 0 or self.ballrect.right > self.width:
                    self.xspeed = -self.xspeed                
                    pong.play(0)        
                if self.ballrect.top < self.panelHeight:
                    self.yspeed = -self.yspeed                
                    pong.play(0)               

                # check if ball has gone past bat - lose a life
                if self.ballrect.top > self.height:
                    restartBall()
                    if self.lives == 0:
                        gameOver()
            
                if self.xspeed < 0 and self.ballrect.left < 0:
                    self.xspeed = -self.xspeed                                
                    pong.play(0)

                if self.xspeed > 0 and self.ballrect.right > self.width:
                    self.xspeed = -self.xspeed                               
                    pong.play(0)
           
                # check if ball has hit wall
                # if yes yhen delete brick and change ball direction
                index = self.ballrect.collidelist(self.wall.brickrect)       
                if index != -1: 
                    if self.ballrect.center[0] > self.wall.brickrect[index].right or \
                       self.ballrect.center[0] < self.wall.brickrect[index].left:
                        self.xspeed = -self.xspeed
                    else:
                        self.yspeed = -self.yspeed                
                    pong.play(0)              
                    self.wall.brickrect[index:index + 1] = []
                    self.score += 10
                

            
                # Let player move bat
                if self.bot or self.player.DBG:
                    if self.frames % self.player.freq == 0:
                        self.player.calculate()

                if self.bot:
                    self.player.move()
                     
                if self.batrect.left < 0:
                    self.batrect.x = 0
                if self.batrect.right > self.width:
                    self.batrect.right = self.width
                
                self.frames += 1
                self.xspeed = (np.abs(self.xspeed) + self.acc) * np.sign(self.xspeed)
                self.yspeed = (np.abs(self.yspeed) + self.acc) * np.sign(self.yspeed)


            self.screen.fill(bgcolour)

            pygame.draw.rect(self.screen, panelcolour, (0, 0, self.width, 45), 0)

            for i in range(0, len(self.wall.brickrect)):
                self.screen.blit(self.wall.brick, self.wall.brickrect[i])    

            # if wall completely gone then rebuild it
            if self.wall.brickrect == []:              
                self.wall.build_wall(self.width, self.yFreeShift + self.panelHeight)                
                self.xspeed = xspeed_init
                self.yspeed = yspeed_init                
                self.ballrect.center = self.width / 2, self.height / 3
         
            self.screen.blit(ball, self.ballrect)
            self.screen.blit(bat, self.batrect)



            ######### HUGE draw-text-on-screen block #########
            scoretext = pygame.font.Font(None,40).render('Score: ' + str(self.score), True, (0,255,255), panelcolour)
            scoretextrect = scoretext.get_rect()
            scoretextrect = scoretextrect.move(self.width - scoretextrect.right, 0)
            self.screen.blit(scoretext, scoretextrect)

            livestext = pygame.font.Font(None,40).render('Lives: ' + str(self.lives), True, (0,255,255), panelcolour)
            livestextrect = livestext.get_rect()
            livestextrect = livestextrect.move(0, 8)
            self.screen.blit(livestext, livestextrect)
            
            fpstext = pygame.font.Font(None,14).render('FPS: ' + str(int(self.clock.get_fps())), True, (0,255,255), panelcolour)
            self.screen.blit(fpstext, fpstext.get_rect().move(0, 0))

            accstr = str(self.acc)
            accfont = pygame.font.Font(None,28)
            acctext = accfont.render(accstr, True, (0,255,255), panelcolour)
            accw, acch = accfont.size(accstr)
            self.screen.blit(acctext, acctext.get_rect().move(self.btnAccLess.rect.right + (62 - accw)/2, 19))
            
            acctstr = 'Acceleration'
            acctfont = pygame.font.Font(None,24)
            accttext = acctfont.render(acctstr, True, (0,255,255), panelcolour)
            acctw, accth = acctfont.size(acctstr)
            self.screen.blit(accttext, accttext.get_rect().move(self.btnAccLess.rect.left + (self.btnAccMore.rect.right - self.btnAccLess.rect.left - acctw)/2, 2))
            
            depthstr = str(self.player.maxDepth)
            depthfont = pygame.font.Font(None,28)
            depthtext = accfont.render(depthstr, True, (0,255,255), panelcolour)
            depthw, depthh = depthfont.size(depthstr)
            self.screen.blit(depthtext, depthtext.get_rect().move(self.btnDepthLess.rect.right + (30 - depthw)/2, 19))
            
            depthtstr = 'Depth'
            depthtfont = pygame.font.Font(None,24)
            depthttext = depthtfont.render(depthtstr, True, (0,255,255), panelcolour)
            depthtw, depthth = depthtfont.size(depthtstr)
            self.screen.blit(depthttext, depthttext.get_rect().move(self.btnDepthLess.rect.left + (self.btnDepthMore.rect.right - self.btnDepthLess.rect.left - depthtw)/2, 2))

            ##### <DEBUG> #####
            for l in self.DBGlines:
                pygame.draw.line(self.screen, (255, 255, 0), l[0], l[1])
            ##### </DEBUG> #####

            self.btnLines.draw(self.screen)
            self.btnReset.draw(self.screen)
            self.btnPause.draw(self.screen)
            self.btnBot.draw(self.screen)
            self.btnAccLess.draw(self.screen)
            self.btnAccMore.draw(self.screen)
            self.btnDepthLess.draw(self.screen)
            self.btnDepthMore.draw(self.screen)

            pygame.display.flip()

class Wall():

    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width, yshift = 0):        
        xpos = 0
        ypos = yshift
        adj = 0
        self.brickrect = []
        for i in range (0, 52):           
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
    pl = bp(3, 1)
    br = Breakout(pl)
    br.main()
    Parallel
