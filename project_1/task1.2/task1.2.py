import sys
import pickle
import logging
import numpy as np

from tree_plotter import graphVis
tree_csv = 'tree.dot'
tree_file = 'tree.pickle'

logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                    format='%(levelname)s | %(asctime)s | %(message)s')
logger = logging.getLogger(__name__)


def move_still_possible(S):
    return not (S[S == 0].size == 0)


def move(S, p, stat, strategy):
    if strategy == 'intelligent':
        return move_at_intelligent(S, p, stat)
    elif strategy == 'super_intelligent':
        return intellectual_move(S, p)
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


def tournament(*args, **kwargs):
    field_st, player_st = play(*args, **kwargs)
    logger.info('Tournament statistics %s' % player_st)


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
    field_st, player_st = play(n)

    # normalize the array with statistic
    for k, v in field_st.items():
        field_st[k] = v / np.sum(v).astype(float)

    logger.info('Train statistics %s' % player_st)
    return field_st, player_st


def game(x_strategy, o_strategy, x_stat, o_stat):

    inv_symbols = {v: k for k, v in symbols.items()}
    strategy_dict = {inv_symbols['x']: x_strategy, inv_symbols['o']: o_strategy}
    stat_dict = {inv_symbols['x']: x_stat, inv_symbols['o']: o_stat}

    # initialize 3x3 tic tac toe board
    game_state = np.zeros((3, 3), dtype=int)
    # game_state = np.ones((3, 3), dtype=int)
    # game_state[0][0] = -1
    # game_state[0][2] = -1
    # game_state[2][0] = -1
    # game_state[2][2] = -1
    # game_state[2][1] = 0
    # game_state[1][2] = 0

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
        self.root = Node(p, S)

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

    def post_traverse(self):
        self._post_traverse(self.root, depth=0)

    def _post_traverse(self, node, depth):

        print('%s| %s| %s| %s' % ('   '*depth, node.p, node.winner, depth))
        depth += 1
        if node.child_list:
            for c in node.child_list:
                self._post_traverse(c, depth)
        # else:
        #     print('node in depth=%s' % depth)
        #     print_game_state(node.S)

    def build_tree(self):
        self._build_tree(self.root, count=0)

    def _build_tree(self, node, count):
        count += 1
        # if count > 7:
            # return

        previous_player = node.p * (-1)
        if move_was_winning_move(node.S, previous_player):
            node.winner = previous_player
            logger.info('%s) winner = %s' % (count,previous_player))
            print_game_state(node.S)
            return

        # if not move_was_winning_move(node.S, node.p):
        else:
            xs, ys = np.where(node.S == 0)
            for i in xrange(xs.size):
                Child = np.copy(node.S)
                Child[xs[i], ys[i]] = node.p
                child_node = Node(node.p * (-1), Child, child_list=[])
                node.child_list.append(child_node)
        if not node.child_list:
            # draw
            logger.debug('finished with draw')
            # print_game_state(node.S)
            node.winner = 0
            return

        for c in node.child_list:
            self._build_tree(c, count)

    def mark_nodes(self):
        self._mark_nodes(self.root, d=0)

    def _mark_nodes(self, node, d):
        d += 1
        if node.winner:
            return node.winner

        if node == self.root:
            pass

        result_list = []
        for c in node.child_list:
            winner = self._mark_nodes(c, d)
            if winner and winner not in result_list:
                result_list.append(winner)

        if node == self.root:
            pass

        if node.p in result_list:
            if node == self.root:
                pass
            node.winner = node.p
            logger.info('node %s win, result_list=%s' % (node, result_list))
            logger.info(list(i.winner for i in node.child_list))
        elif 0 in result_list:
            node.winner = 0
            logger.info('node %s draw, result_list=%s' % (node, result_list))
            logger.info(list(i.winner for i in node.child_list))
        elif node.p * (-1) in result_list:
            if node == self.root:
                pass
            node.winner = node.p * (-1)
            logger.info('node %s lose, result_list=%s' % (node, result_list))
            logger.info(list(i.winner for i in node.child_list))
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
            node = self.find_state(c, S)
            if node:
                return node


class IntellectualMove:
    def __init__(self):
        self.tree = None
        self.current_node = None

    def init_tree(self, S, p):
        self.tree = Tree(p, S)
        self.tree.build_tree()
        self.tree.mark_nodes()
        print('=*100')
        print('layer=0')
        self.tree.plot_layer(0)
        print('=*100')
        print('layer=1')
        self.tree.plot_layer(1)
        print('=*100')
        print('layer=2')
        self.tree.plot_layer(2)
        # self.tree.post_traverse()
        # graphVis(self.tree, tree_csv)

    def __call__(self, S, p):
        # build tree if does not exists
        if not self.tree:
            self.init_tree(S, p)

        # find node that represents current game state
        # save it as current node
        if not self.current_node:
            self.current_node = self.tree.find_state(self.tree.root, S)

        # find the max gain node for the next step
        try:
            self.current_node = self.tree.find_state(self.current_node, S).max_gain(p)
        except Exception as e:
            print(e)

        print('current game state')
        print_game_state(S)
        print('current node state')
        print_game_state(self.current_node.S)
        np.copyto(S, self.current_node.S)
        print('current game state after step')
        print_game_state(S)
        return S


if __name__ == '__main__':
    # field_st, player_st = train(n=100000)
    # tournament(n=10000,
    #            x_strategy='intelligent',
    #            o_strategy='random',
    #            x_stat = field_st[1],
    #            o_stat = field_st[-1]
    #            )
    # load_from_file = False
    # dump_to_file = False
    # if load_from_file:
    #     with open(tree_file, 'rb') as f:
    #         tr = pickle.load(f)
    # else:
    #     tr = Tree(p=1)
    #     tr.build_tree()
    #
    # if dump_to_file:
    #     with open(tree_file, 'wb') as f:
    #         pickle.dump(tr, f, protocol=pickle.HIGHEST_PROTOCOL)
    # print('marking nodes')
    # tr.mark_nodes()
    # print('printing tree')
    # tr.print_tree()
    intellectual_move = IntellectualMove()
    tournament(x_strategy='super_intelligent',
               o_strategy='random')




