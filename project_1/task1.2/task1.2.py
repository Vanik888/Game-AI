import os
import sys
import logging

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


from tree_plotter import graphVis
plots_folder = 'plots'

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s | %(asctime)s | %(message)s')
logger = logging.getLogger(__name__)


def move_still_possible(S):
    return not (S[S == 0].size == 0)


def move(S, p, stat, strategy):
    if strategy == 'intelligent':
        return move_at_intelligent(S, p, stat)

    elif strategy == 'full_tree':
        return full_tree_move(S, p)

    elif strategy == 'min_max':
        return min_max_move(S, p)

    else:
        return move_at_random(S, p)


def move_at_intelligent(S, p, stat):
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
    global plots_folder
    img_name = '%s_%s' % (n, img_name)
    img_path = os.path.join(os.path.abspath(os.path.dirname(__name__)),
                            plots_folder, img_name)

    plt.figure(figsize=(20, 10))
    coef = 100.0/stat.max()
    plt.imshow(stat * coef, vmin=0, vmax=100)
    plt.colorbar()
    plt.savefig(img_path, facecolor='w', edgecolor='w',
                    papertype=None, format='png', transparent=False,
                    bbox_inches='tight', pad_inches=0.1)
    plt.close()


def plot_game_stat(n, x_strategy, o_strategy, player_st, img_name=''):
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
    plot_temperature_map(n, field_st[-1], 'x_wins_map.png')
    plot_temperature_map(n, field_st[1], 'o_wins_map.png')
    # normalize the array with statistic
    for k, v in field_st.items():
        field_st[k] = v / np.sum(v).astype(float)
    logger.info('Finish training')
    logger.info('Train statistics %s' % player_st)
    return field_st, player_st


def game(x_strategy, o_strategy, x_stat, o_stat):
    global full_tree_move

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

    # new tutorial should look for state from root
    full_tree_move.current_node = None

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


class Node:
    def __init__(self, p, S=None, child_list=[], winner=None):
        self.S = np.zeros((3, 3), dtype=int) if S is None else S
        self.child_list = child_list
        self.p = p
        self.winner = winner

    def __repr__(self):
        return 'Node, Player=%s, Winner=%s, Childs=%s' % \
               (self.p, self.winner, len(self.child_list))

    def max_gain(self, p):
        # if player is o then reverse the child list
        # if player is x then do not reverse child list
        reverse = p != (-1)
        # sort child list by max gain
        # the max gain children should be in the beginning
        for c in sorted(self.child_list, key=lambda n: n.winner, reverse=reverse):
            # next move leads to win
            if c.winner == p:
                return c
            # next move leads to draw
            if c.winner == 0:
                return c
            # player loses for sure, no chances to win or draw
            return c


class Tree:
    def __init__(self, p, S=None):
        self.root = Node(p, np.copy(S))

    def plot_layer(self, max_depth):
        self._plot_layer(self.root, 0, max_depth)

    def _plot_layer(self, node, current_depth, max_depth):
        current_depth += 1
        if current_depth < max_depth:
            for c in node.child_list:
                self._plot_layer(c, current_depth, max_depth)
        if current_depth == max_depth:
            print(node)
        if current_depth > max_depth:
            return

    def pre_traverse(self):
        self._pre_traverse(self.root, depth=0)

    def _pre_traverse(self, node, depth):

        print('%s| %s| %s| %s' % ('   '*depth, node.p, node.winner, depth))
        depth += 1
        if node.child_list:
            for c in node.child_list:
                self._pre_traverse(c, depth)

    def build_tree(self):
        self._build_tree(self.root)

    def _build_tree(self, node):

        previous_player = node.p * (-1)
        if move_was_winning_move(node.S, previous_player):
            node.winner = previous_player
            return

        else:
            xs, ys = np.where(node.S == 0)
            for i in xrange(xs.size):
                Child = np.copy(node.S)
                Child[xs[i], ys[i]] = node.p
                child_node = Node(node.p * (-1), Child, child_list=[])
                node.child_list.append(child_node)
        if not node.child_list:
            # draw
            node.winner = 0
            return

        for c in node.child_list:
            self._build_tree(c)

    def mark_nodes(self):
        """
        Sets winner to node.
        winner = 1 for x
        winner = 0 for draw
        winner = -1 for o
        """
        self._mark_nodes(self.root)

    def _mark_nodes(self, node):

        if node.winner:
            return node.winner

        result_list = []
        for c in node.child_list:
            winner = self._mark_nodes(c)
            if winner and winner not in result_list:
                result_list.append(winner)

        if node.p in result_list:
            node.winner = node.p

        elif 0 in result_list:
            node.winner = 0

        elif node.p * (-1) in result_list:
            node.winner = node.p * (-1)

        return node.winner

    def print_tree(self):
        self._print_tree(self.root)

    @classmethod
    def _print_tree(cls, node):
        print_game_state(node.S)
        for c in node.child_list:
            cls._print_tree(c)

    def find_state(self, node, S):
        if np.array_equal(node.S, S):
            return node

        for c in node.child_list:
            if np.array_equal(c.S, S):
                return node

        for c in node.child_list:
            node = self.find_state(c, S)
            if node:
                return node


class FullTreeMove:
    def __init__(self):
        self.tree = None
        self.current_node = None

    def init_tree(self, S, p):
        self.tree = Tree(p, S)
        self.tree.build_tree()
        self.tree.mark_nodes()
        # self.tree.pre_traverse()
        # graphVis(self.tree, tree_csv)

    def __call__(self, S, p):
        # build tree if does not exists
        if not self.tree:
            self.init_tree(S, p)

        # find node that represents current game state
        # save it as current node
        if not self.current_node:
            self.current_node = self.tree.find_state(self.tree.root, S)
        # if np.array_equal(S, np.zeros((3,3), ))
        # find the max gain node for the next step

        try:
            self.current_node = self.tree.\
                find_state(self.current_node, S).max_gain(p)
        except Exception as e:
            logger.warning('Not found state for root')
            logger.warning(p)
            logger.warning(self.tree.root.S)
            print_game_state(S)
            print(e)

        np.copyto(S, self.current_node.S)
        return S


class MinMaxMove:
    def __init__(self, level):
        self._level = level

    def _utitlity_function(self, S, p):
        if move_was_winning_move(S, p):
            return p
        if move_was_winning_move(S, p*(-1)):
            return p * (-1)
        if not move_still_possible(S):
            return 0
        # this state can lead to win as well as to lose, therefore
        return 0.5 * p

    def _build_tree(self, node, S, p, level):
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
        if node in self._util_dict:
            self._min_max_dict[node] = self._util_dict[node]
            return self._util_dict[node]

        mmv = -np.inf
        for c in self._child_dict[node]:
            mmv = max(mmv, self._min_node_util(c))

        self._min_max_dict[node] = mmv
        return mmv

    def _min_node_util(self, node):
        if node in self._util_dict:
            self._min_max_dict[node] = self._util_dict[node]
            return self._util_dict[node]

        mmv = np.inf
        for c in self._child_dict[node]:
            mmv = min(mmv, self._max_node_util(c))

        self._min_max_dict[node] = mmv
        return mmv

    def __call__(self, S, p):
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
    full_tree_move = FullTreeMove()
    min_max_move = MinMaxMove(level=2)

    games = 100
    trainings = 1000
    field_st, player_st = train(n=trainings)
    tournament(n=games,
               x_strategy='intelligent',
               o_strategy='intelligent',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='intelligent',
               o_strategy='random',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='intelligent',
               o_strategy='min_max',
               x_stat=field_st[1],
               o_stat=field_st[-1])

    tournament(n=games,
               x_strategy='min_max',
               o_strategy='min_max')

    tournament(n=games,
               x_strategy='min_max',
               o_strategy='intelligent',
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
               o_strategy='intelligent',
               x_stat=field_st[1],
               o_stat=field_st[-1])


    tournament(n=games,
               x_strategy='random',
               o_strategy='min_max')



    # tournament(n=games,
    #            x_strategy='intelligent',
    #            o_strategy='full_tree',
    #            x_stat=field_st[1],
    #            o_stat=field_st[-1])

    # tournament(n=games,
    #            x_strategy='min_max',
    #            o_strategy='full_tree')

    #
    # tournament(n=games,
    #            x_strategy='full_tree',
    #            o_strategy='random')

    # tournament(n=games,
    #            x_strategy='full_tree',
    #            o_strategy='min_max')

    # tournament(n=games,
    #            x_strategy='min_max',
    #            o_strategy='full_tree')

    # tournament(n=games,
    #            x_strategy='full_time',
    #            o_strategy='intelligent',
    #            x_stat=field_st[1],
    #            o_stat=field_st[-1])



