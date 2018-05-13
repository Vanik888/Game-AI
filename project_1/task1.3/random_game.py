from connect_four_game import ConnectFourGame
from constants import *


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


if __name__ == '__main__':
    run_random_game()
