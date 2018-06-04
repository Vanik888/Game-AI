from tGame import TGame

class TPlayer(object):
    """ description of class """

    def __init__(self, game, player):
        self.game = game
        self.player = player
    
    @nextMove
    def nextMove(self):
        """Method documentation"""
        return