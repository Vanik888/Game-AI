import os
import sys
import logging

import numpy as np
import matplotlib.pyplot as plt


plots_folder = 'plots'

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s | %(asctime)s | %(message)s')
logger = logging.getLogger(__name__)


def move_still_possible(S):
    return not (S[S == 0].size == 0)


def move(S, p, stat, strategy):
    if strategy == 'probabilistic':
        return move_at_probabilistic(S, p, stat)

    elif strategy == 'min_max':
        return min_max_move(S, p)

    else:
        return move_at_random(S, p)


def move_at_probabilistic(S, p, stat):
    # (s == 0).astype(int) keeps only empty places in field
    intersection = ((S==0).astype(int) * stat)

    if np.max(intersection) > 0:
        i, j = np.unravel_index(intersection.argmax(), intersection.shape)
        logger.debug('max probability to win in position S[%s][%s]=%s' %
                     (i, j, S[i][j]))
        S[i][j] = p
    else:
        logger.debug('all positions with high probability to win are busy, '
                     'we have to chose the random position')
        S = move_at_random(S, p)

    return S


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


def plot_temperature_map(n, stat, img_name='temperature_map.png'):
    """
    :param n: the number of games
    :param stat: game statistics
    :param img_name: image name
    Plots the temperature map for normalized statistics matrix
    """
    global plots_folder
    img_name = '%s_%s' % (n, img_name)
    img_path = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                            plots_folder, img_name)

    plt.figure(figsize=(20, 10))

    plt.imshow(stat, extent=[0, 3, 0, 3])
    plt.colorbar()
    plt.savefig(img_path, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1)
    plt.close()


def plot_game_stat(n, x_strategy, o_strategy, player_st, img_name=''):
    """
    :param n: number of games
    :param x_strategy: the strategy for x
    :param o_strategy: the strategy for o
    :param player_st: the statistics dict
    :param img_name: the image name
    Plots game statistics diagram
    """
    global plots_folder
    img_name = img_name or '%s_%s_vs_%s.png' % (n, x_strategy, o_strategy)
    img_path = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                           plots_folder, img_name)

    # fig = plt.figure()
    x_win, x_lose = player_st.values()
    draw = n - sum(player_st.values())

    x = np.arange(3)
    data = [x_win, x_lose, draw]
    plt.bar(x, data, color=['r', 'y', 'b'])
    plt.xticks(x, ('X', 'O', 'Draw'))
    plt.title('X uses %s, O uses %s' % (x_strategy, o_strategy))


    plt.savefig(img_path, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1)
    plt.close()


def tournament(n, x_strategy, o_strategy, **kwargs):
    field_st, player_st = play(n, x_strategy, o_strategy, **kwargs)
    plot_game_stat(n, x_strategy, o_strategy, player_st)
    logger.info('Tournament statistics %s, %s vs %s' % (player_st,
                                                        x_strategy,
                                                        o_strategy))


def play(n=10, x_strategy='random', o_strategy='random', x_stat={}, o_stat={}):
    x = 1
    o = -1
    d = 0
    zero = np.zeros((3, 3), dtype=int)
    field_st = {x: zero, o: np.copy(zero)}
    player_st = {x: 0, o: 0}
    for i in xrange(n):
        winner, game_state = game(x_strategy, o_strategy, x_stat, o_stat)
        if winner != d:
            player_st[winner] += 1
            only_winner_field = np.full((3, 3), winner)
            field_st[winner] += np.equal(game_state, only_winner_field).\
                astype(int)
    return field_st, player_st


def train(n=10):
    logger.info('Start training')
    field_st, player_st = play(n)

    plot_game_stat(n, 'random', 'random', player_st, 'training.png')

    # normalize the array with statistic
    for k, v in field_st.items():
        field_st[k] = v / np.sum(v).astype(float)

    plot_temperature_map(n, field_st[-1], 'x_wins_map.png')
    plot_temperature_map(n, field_st[1], 'o_wins_map.png')
    logger.info('Finish training')
    logger.info('Train statistics %s' % player_st)
    return field_st, player_st


def game(x_strategy, o_strategy, x_stat, o_stat):

    inv_symbols = {v: k for k, v in symbols.items()}
    strategy_dict = {inv_symbols['x']: x_strategy, inv_symbols['o']: o_strategy}
    stat_dict = {inv_symbols['x']: x_stat, inv_symbols['o']: o_stat}

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
        logger.debug('%s moves' % name)

        # let player make a move
        game_state = move(game_state, player, stat_dict[player],
                          strategy_dict[player])

        # evaluate game state
        if move_was_winning_move(game_state, player):
            logger.debug('player %s wins after %d moves' % (name, mvcntr))
            noWinnerYet = False
            return player, game_state

        # switch player and increase move counter
        player *= -1
        mvcntr += 1

    if noWinnerYet:
        logger.debug('game ended in a draw')
        return 0, game_state


class MinMaxMove:
    """
    object is called to make a move based on heuristic
    """
    def __init__(self, level):
        """defines the tree depth for predictions"""
        self._level = level

    def _utitlity_function(self, S, p):
        """
        :param S: current state
        :param p: current player
        :return: utility value for stat S and player p
        if x wins, set utility to 1
        if o wins, set utility to -1
        if draw, set utility to 0
        if x moves and game is not finished, set utility to 0.5,
         asuming that x might win later (be positive in predictions)
        if o moves and game is not finished, set utility to -0.5,
         asuming that o might win later (be positive in predictions)
        """
        if move_was_winning_move(S, p):
            return p
        if move_was_winning_move(S, p*(-1)):
            return p * (-1)
        if not move_still_possible(S):
            return 0
        # this state can lead to win as well as to lose, therefore
        return 0.5 * p

    def _build_tree(self, node, S, p, level):
        """
        :param node: node id
        :param S: current state
        :param p: current player
        :param level: current tree depth
        Builds the tree
        """
        child_list = []
        child_p = p * (-1)

        if level == 0:
            self._util_dict[node] = self._utitlity_function(S, p)

        else:
            xs, ys = np.where(S == 0)
            for i in xrange(xs.size):
                new_node = max(self._node_dict.keys()) + 1
                child_state = np.copy(S)
                child_state[xs[i]][ys[i]] = p
                self._node_dict[new_node] = (child_state, child_p)
                child_list.append(new_node)

            self._child_dict[node] = child_list
            for c in child_list:
                child_state, child_p = self._node_dict[c]
                self._build_tree(c, child_state, child_p, level-1)

    def _max_node_util(self, node):
        """
        :param node: node
        :return: min max value
        recursive method to determine the utility function for current node
        """
        if node in self._util_dict:
            self._min_max_dict[node] = self._util_dict[node]
            return self._util_dict[node]

        mmv = -np.inf
        for c in self._child_dict[node]:
            mmv = max(mmv, self._min_node_util(c))

        self._min_max_dict[node] = mmv
        return mmv

    def _min_node_util(self, node):
        """
        :param node: node
        :return: min max value
        recursive method to determine the utility function for current node
        """
        if node in self._util_dict:
            self._min_max_dict[node] = self._util_dict[node]
            return self._util_dict[node]

        mmv = np.inf
        for c in self._child_dict[node]:
            mmv = min(mmv, self._max_node_util(c))

        self._min_max_dict[node] = mmv
        return mmv

    def __call__(self, S, p):
        """
        :param S: current state
        :param p: current player
        Makes a move for player p from state S.
        Actually this method builds the tree for current state S and player p.
        Then, runs the recursive methods to calculate min_max_dict values.
        Depending on current player the algorithm choses the next move.
        """
        self._node_dict = {}
        self._child_dict = {}
        self._util_dict = {}
        self._min_max_dict = {}

        current_node = 0
        self._node_dict[current_node] = S, p
        self._build_tree(current_node, S=S, p=p, level=2)

        if p == 1:
            self._max_node_util(current_node)
            child_min_max = {c: self._min_max_dict[c]
                             for c in self._child_dict[current_node]}
            child_min_max = sorted(child_min_max.items(), key=lambda x: x[1])
            return self._node_dict[child_min_max[-1][0]][0]

        else:
            self._min_node_util(current_node)
            child_min_max = {c: self._min_max_dict[c]
                             for c in self._child_dict[current_node]}
            child_min_max = sorted(child_min_max.items(), key=lambda x: x[1])
            return self._node_dict[child_min_max[0][0]][0]


if __name__ == '__main__':
    min_max_move = MinMaxMove(level=2)

    games = 10000
    trainings = 10000
    field_st, player_st = train(n=trainings)
    for k, v in field_st.items():
        logger.info('Game statistics matrix for %s' % k)
        print_game_state(v)

    tournament(n=games,
               x_strategy='probabilistic',
               o_strategy='probabilistic',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='probabilistic',
               o_strategy='random',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='probabilistic',
               o_strategy='min_max',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='min_max',
               o_strategy='min_max')

    tournament(n=games,
               x_strategy='min_max',
               o_strategy='probabilistic',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='min_max',
               o_strategy='random')

    tournament(n=games,
               x_strategy='random',
               o_strategy='random')

    tournament(n=games,
               x_strategy='random',
               o_strategy='probabilistic',
               x_stat=field_st[1],
               o_stat=field_st[-1])


    tournament(n=games,
               x_strategy='random',
               o_strategy='min_max')




