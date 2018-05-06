import numpy as np


def move_still_possible(S):
    return not (S[S == 0].size == 0)


def move_at_random(S, p):
    xs, ys = np.where(S == 0)

    i = np.random.permutation(np.arange(xs.size))[0]

    S[xs[i], ys[i]] = p

    return S


def move_was_winning_move(S, p):
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True

    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True

    if (np.sum(np.diag(S)) * p) == 3:
        return True

    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True

    return False


# relate numbers (1, -1, 0) to symbols ('x', 'o', ' ')
symbols = {1: 'x', -1: 'o', 0: ' '}


# print game state matrix using symbols
def print_game_state(S):
    B = np.copy(S).astype(object)
    for n in [-1, 0, 1]:
        B[B == n] = symbols[n]
    print B


def train(n=10):
    x = 1
    o = -1
    d = 0
    zero = np.zeros((3, 3), dtype=int)
    field_st = {x: zero, o: np.copy(zero)}
    player_st = {x: 0, o: 0}
    for i in xrange(n):
        winner, game_state = game()
        if winner != d:
            player_st[winner] += 1
            only_winner_field = np.full((3, 3), winner)
            field_st[winner] += np.equal(game_state, only_winner_field).\
                astype(int)

    # normalize the array with statistic
    for k, v in field_st.items():
        field_st[k] = v / np.sum(v).astype(float)

    return field_st, player_st


def game():
    # initialize 3x3 tic tac toe board
    game_state = np.zeros((3, 3), dtype=int)

    # initialize player number, move counter
    player = 1
    mvcntr = 1

    # initialize flag that indicates win
    noWinnerYet = True

    while move_still_possible(game_state) and noWinnerYet:
        # get player symbol
        name = symbols[player]
        print '%s moves' % name

        # let player move at random
        game_state = move_at_random(game_state, player)

        # print current game state
        print_game_state(game_state)

        # evaluate game state
        if move_was_winning_move(game_state, player):
            print 'player %s wins after %d moves' % (name, mvcntr)
            noWinnerYet = False
            return player, game_state

        # switch player and increase move counter
        player *= -1
        mvcntr += 1

    if noWinnerYet:
        print 'game ended in a draw'
        return 0, game_state


if __name__ == '__main__':
    field_st, player_st = train()




