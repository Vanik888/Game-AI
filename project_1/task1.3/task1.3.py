import numpy as np
from connect_four_game import ConnectFourGame


if __name__ == '__main__':

    game = ConnectFourGame()
    game.print_game_state()

    game.make_move(1, 0)
    game.make_move(1, 0)
    game.make_move(1, 1)
    game.make_move(1, 1)
    game.make_move(1, 1)
    game.make_move(-1, 2)
    game.make_move(1, 2)
    game.make_move(1, 2)
    game.make_move(1, 2)
    game.make_move(-1, 3)
    game.make_move(-1, 3)
    game.make_move(1, 3)
    game.make_move(1, 3)
    game.make_move(1, 3)
    # game.make_move(1, 4)
    # game.make_move(1, 5)
    # game.make_move(1, 6)
    game.print_game_state()

