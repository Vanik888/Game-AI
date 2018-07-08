import numpy as np
import skfuzzy as fuzz
from skfuzzy import control

class BOPlayerFZ(object):
	""" PLayer for Breakout using Fuzzy Logic """

	def __init__(self, DBG = False):
		self.game = None
		self.output = 0
		
		self.action_ctrl = self.action = None

		# Deprecated: left here inly for the compatibility with previous version of breakout
		self.DBG = DBG
		self.maxDepth = 1
		self.freq = 1
		
	def init(self, game):
		self.game = game
		
		width = game.width
		whalf = width / 2
		height = game.height

		g = game.batrect.width / 2
		p = g / 2

		threshold = 0.45 * game.height
		q = 32

		spd = self.game.bat_speed * 6
		s = spd / 4
		t = s / 2
		
		difX = fuzz.control.Antecedent(np.arange(-whalf, whalf, 1), 'difX')
		ballY = fuzz.control.Antecedent(np.arange(-whalf, whalf, 1), 'ballY')
		action = fuzz.control.Consequent(np.arange(-spd, spd, .1), 'action')

		
		difX['left'] = fuzz.trapmf(difX.universe, [-whalf, -whalf, -g-p, -g+p])
		difX['middle'] = fuzz.trapmf(difX.universe, [-g-p, -g+p, g-p, g+p])
		difX['right'] = fuzz.trapmf(difX.universe, [g-p, g+p, whalf, whalf])
		
		ballY['far'] = fuzz.trapmf(ballY.universe, [0, 0, threshold, threshold+q])
		ballY['close'] = fuzz.trapmf(ballY.universe, [threshold-q, threshold, game.height, game.height])
		
		action['left'] = fuzz.trapmf(action.universe, [-spd, -spd, -s-t, -s+t])
		action['wait'] = fuzz.trapmf(action.universe, [-s-t, -s+t, s-t, s+t])
		action['right'] = fuzz.trapmf(action.universe, [s-t, s+t, spd, spd])

		
		rule1 = fuzz.control.Rule(ballY['far'], action['wait'])
		rule2 = fuzz.control.Rule(difX['middle'] & ballY['close'], action['wait'])
		rule3 = fuzz.control.Rule(difX['left'] & ballY['close'], action['left'])
		rule4 = fuzz.control.Rule(difX['right'] & ballY['close'], action['right'])

		
		self.action_ctrl = fuzz.control.ControlSystem([rule1, rule2, rule3, rule4])
		self.action = fuzz.control.ControlSystemSimulation(self.action_ctrl)

	def calculate(self):
		if self.action_ctrl is None or self.action is None: return

		ballY = self.game.ballrect.centery
		difX = self.game.ballrect.centerx - self.game.batrect.centerx
		
		ballY = np.round(np.clip(ballY, 0, self.game.height))
		difX = np.round(np.clip(difX, -self.game.width / 2, self.game.width / 2))

		#ballY = 2.34
		#difX = 1.03

		self.action.input['difX'] = difX
		self.action.input['ballY'] = ballY

		self.action.compute()
		# print self.action.output
	
	def move(self):
		if self.action is None or self.action.output is None: return
		spd = self.action.output['action']
		if np.abs(spd) > self.game.bat_speed:
		   spd = np.sign(spd) * self.game.bat_speed
		
		self.game.batrect = self.game.batrect.move(spd, 0)