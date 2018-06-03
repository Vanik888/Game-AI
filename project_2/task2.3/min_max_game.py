from connect_four_with_min_max import ConnectFourGame
from constants import *
import numpy as np


def run_random_game():
    game = ConnectFourGame()

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    no_winner_yet = True

    while game.move_still_possible() and no_winner_yet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        game.make_move(player)

        # print current game state
        game.print_game_state()

        # evaluate game state
        if game.move_was_winning_move():
            print 'player %s wins after %d moves' % (name, mvcntr)
            no_winner_yet = False

        # switch player and increase move counter
        player *= -1
        mvcntr += 1

    if no_winner_yet:
        print 'game ended in a draw'


def make_min_max_move():

    x_stat = [[0.0015, 0.0015, 0.0013, 0.0013, 0.0014, 0.0015, 0.0015],
 [0.0058, 0.0058, 0.0059, 0.0062, 0.0058, 0.0059, 0.0059],
 [0.0177, 0.0172, 0.0176, 0.0193, 0.0179, 0.0176, 0.0176],
 [0.0255, 0.028, 0.0299, 0.0312, 0.0299, 0.0283, 0.0254],
 [0.035, 0.0379, 0.0412, 0.0447, 0.0409, 0.0382, 0.0352],
 [0.0455, 0.0488, 0.0525, 0.0597, 0.0521, 0.0486, 0.0453]]

    o_stat = [[0.0018, 0.0018, 0.0017, 0.0017, 0.0017, 0.0017, 0.0018],
 [0.0068, 0.0069, 0.0067, 0.007, 0.0071, 0.0069, 0.0071],
 [0.0196, 0.02, 0.0197, 0.0217, 0.0198, 0.0198, 0.0197],
 [0.0275, 0.0304, 0.0326, 0.0344, 0.0325, 0.0306, 0.027],
 [0.0363, 0.0393, 0.0433, 0.0476, 0.0432, 0.0395, 0.036],
 [0.0368, 0.0412, 0.0447, 0.0536, 0.0448, 0.0412, 0.0369]]

    game = ConnectFourGame(2, x_stat)

    # initialize player number, move counter
    player = 1
    mvcntr = 1


    game.make_min_max_move(None, player)
    game.print_game_state()
    # game.make_min_max_move(None, player * -1)
    # game.print_game_state()
    game.make_move(player * -1, 4)
    game.print_game_state()
    game.make_min_max_move(None, player)
    game.print_game_state()
    game.make_min_max_move(None, player * -1)
    game.print_game_state()
    game.make_min_max_move(None, player)
    game.print_game_state()
    game.make_min_max_move(None, player * -1)
    game.print_game_state()
    game.make_min_max_move(None, player)
    game.print_game_state()
    game.make_min_max_move(None, player * -1)
    game.print_game_state()
    game.make_min_max_move(None, player)
    game.print_game_state()


def play_min_max_game(depth=2):
    global x_wins
    global o_wins
    global draws
    global win_pos_x
    global win_pos_o

    x_stat = [[0.0015, 0.0015, 0.0013, 0.0013, 0.0014, 0.0015, 0.0015],
              [0.0058, 0.0058, 0.0059, 0.0062, 0.0058, 0.0059, 0.0059],
              [0.0177, 0.0172, 0.0176, 0.0193, 0.0179, 0.0176, 0.0176],
              [0.0255, 0.028, 0.0299, 0.0312, 0.0299, 0.0283, 0.0254],
              [0.035, 0.0379, 0.0412, 0.0447, 0.0409, 0.0382, 0.0352],
              [0.0455, 0.0488, 0.0525, 0.0597, 0.0521, 0.0486, 0.0453]]

    game = ConnectFourGame(depth, x_stat)
    player = 1
    mvcntr = 1
    no_winner_yet = True

    while game.move_still_possible() and no_winner_yet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        if player == 1:
            prev_state = game.game_state
            game.make_min_max_move(player)
            cur_state = game.game_state
            lastInserted_x, lastInserted_y = np.where(
                np.not_equal(prev_state, cur_state))
            game.last_inserted_row = lastInserted_x[0]
            game.last_inserted_column = lastInserted_y[0]
        else:
            game.make_move(player)

        # print current game state
        game.print_game_state()

        # evaluate game state

        if game.move_was_winning_move(player):
            print 'player %s wins after %d moves' % (name, mvcntr)
            no_winner_yet = False
            if player == 1:
                x_wins +=1
            else:
                o_wins += 1

        # switch player and increase move counter
        player *= -1
        mvcntr += 1

    if no_winner_yet:
        print 'game ended in a draw'
        draws+=1

if __name__ == '__main__':
    x_wins = 0
    o_wins = 0
    draws = 0
    # win_pos_x = 0
    # win_pos_o = 0
    # for i in xrange(10000):
    #     play_min_max_game(1)
    # print x_wins
    # print o_wins
    # print draws

    play_min_max_game(1)
    # print x_wins
    # print o_wins
    # print draws
