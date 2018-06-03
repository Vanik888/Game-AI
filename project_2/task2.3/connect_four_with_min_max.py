import numpy as np
from constants import *


class ConnectFourGame:
    def __init__(self,
                 level=2,
                 x_stat=np.zeros((n_rows, n_columns), dtype=int),
                 o_stat=np.zeros((n_rows, n_columns), dtype=int)):
        self.game_state = np.zeros((n_rows, n_columns), dtype=int)
        self.last_inserted_column = -1
        self.last_inserted_row = -1
        self.level = level
        self.x_stat = x_stat
        self.o_stat = o_stat

    """Prints current game state"""
    def print_game_state(self):
        state_matrix = np.copy(self.game_state.astype(object))

        for n in [-1, 0, 1]:
            state_matrix[state_matrix == n] = symbols[n]
        print state_matrix
        print "\n"

    @staticmethod
    def print_matrix(s):
        state_matrix = np.copy(s.astype(object))

        for n in [-1, 0, 1]:
            state_matrix[state_matrix == n] = symbols[n]
        print state_matrix
        print "\n"

    """
    If parameter column is equal to None, that means, that
    move is made at random.
    """
    def make_move(self, p, column=None, win_pos=None):
        if column is None:
            if win_pos is not None:
                column = self.__select_best_move(win_pos)
            else:
                column = self.__select_column_at_random()
        # Slicing the whole target column and finding first available
        # row for insertion of a new element.
        chosen_column = self.game_state[:, column]
        desired_row = -1
        for i, e in list(enumerate(chosen_column)):
            if e == 0:
                desired_row = i
        # If an empty cell was found
        if desired_row != -1:
            self.game_state[desired_row, column] = p
            self.last_inserted_column = column
            self.last_inserted_row = desired_row

        return desired_row

    def make_move_for_children(self, s, p, column=None):

        # Slicing the whole target column and finding first available
        # row for insertion of a new element.
        chosen_column = s[:, column]
        desired_row = -1
        for i, e in list(enumerate(chosen_column)):
            if e == 0:
                desired_row = i
        # If an empty cell was found
        if desired_row != -1:
            s[desired_row, column] = p
        else:
            print "not found"
            self.print_game_state()
            self.print_matrix(s)
        return s

    """This method chooses best possible move
    based on statistics of 100000 games"""
    def __select_best_move(self, win_pos):
        best_pos = -1
        best_value = 0
        for i, j in zip(*np.where(self.game_state == 0)):
            if win_pos[i, j] > best_value:
                best_value = win_pos[i, j]
                best_pos = j
        if best_pos == -1:
            best_pos = self.__select_column_at_random()
        return best_pos

    """This method checks whether one player has won the game"""
    def move_was_winning_move(self, p):

        # Check all rows if there is a winning combination
        # for i in range(n_rows):
        row_to_check = self.game_state[self.last_inserted_row, :]
        if (row_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(row_to_check, p):
                return True

        # Check all columns if there is a winning combination
        # for i in range(n_columns):
        column_to_check = self.game_state[:, self.last_inserted_column]
        if (column_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(column_to_check, p):
                return True

        # Check diagonal, where item was inserted
        diag_to_check = self.last_inserted_column - self.last_inserted_row
        diagonal = self.game_state.diagonal(diag_to_check)
        if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
            if self.__check_all_sublists(diagonal, p):
                return True

        # Check diagonal of rotated matrix, where item was inserted
        rot_diag_to_check = (self.last_inserted_column +
                             self.last_inserted_row -
                             n_columns + 1)
        diagonal = np.rot90(self.game_state).diagonal(rot_diag_to_check)
        if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
            if self.__check_all_sublists(diagonal, p):
                return True
        return False

    """This method checks whether one player has won the game"""
    def move_was_winning_move_for_matrix(self, S, p):

        # Check all rows if there is a winning combination
        # for i in range(n_rows):
        for i in xrange(S.shape[0]):
            row_to_check = S[i, :]
            if (row_to_check == 0).sum() <= 3:
                if self.__check_all_sublists(row_to_check, p):
                    return True

        # Check all columns if there is a winning combination
        # for i in range(n_columns):
        for i in xrange(S.shape[1]):
            column_to_check = S[:, i]
            if (column_to_check == 0).sum() <= 3:
                if self.__check_all_sublists(column_to_check, p):
                    return True

        # Check diagonal, where item was inserted
        for i in diagonal_shifts:
            diagonal = self.game_state.diagonal(i)
            if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal, p):
                    return True

        # Check diagonal of rotated matrix, where item was inserted
        for i in diagonal_shifts:
            diagonal = np.rot90(S).diagonal(i - 1)
            if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal, p):
                    return True
        return False

    """This method checks whether one player has won the game"""

    def move_was_winning_move_for_whole_matrix(self, p):

        # Check all rows if there is a winning combination
        # for i in range(n_rows):
        row_to_check = self.game_state[self.last_inserted_row, :]
        if (row_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(row_to_check, p):
                return True

        # Check all columns if there is a winning combination
        # for i in range(n_columns):
        column_to_check = self.game_state[:, self.last_inserted_column]
        if (column_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(column_to_check, p):
                return True

        # Check diagonal, where item was inserted
        diag_to_check = self.last_inserted_column - self.last_inserted_row
        diagonal = self.game_state.diagonal(diag_to_check)
        if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
            if self.__check_all_sublists(diagonal, p):
                return True

        # Check diagonal of rotated matrix, where item was inserted
        rot_diag_to_check = (self.last_inserted_column +
                             self.last_inserted_row -
                             n_columns + 1)
        diagonal = np.rot90(self.game_state).diagonal(rot_diag_to_check)
        if len(diagonal) >= winning_sum and (diagonal == 0).sum() <= 3:
            if self.__check_all_sublists(diagonal, p):
                return True
        return False

    """Constructs sublists of given list and
    check whether there is a winning combination for sublists with length 4"""
    def __check_all_sublists(self, list_to_check, p):
        sublists = [list_to_check[i:i + winning_sum] for i in
                    range(0, len(list_to_check), 1)]

        for sublist in sublists:
            if len(sublist) < winning_sum:
                continue
            if np.sum(sublist) * p == winning_sum:
                return True

        return False

    """Checks whether there are still empty cells in matrix"""
    def move_still_possible(self):
        return not (self.game_state[self.game_state == 0].size == 0)

    """Checks whether there are still empty cells in matrix"""
    def move_still_possible_for_matrix(self, S):
        return not (S[S == 0].size == 0)

    """Returns index of randomly chosen column for element insertion"""
    def __select_column_at_random(self):
        xs, ys = np.where(self.game_state == 0)
        i = np.random.permutation(np.arange(ys.size))[0]
        return ys[i]

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
        if self.move_was_winning_move_for_matrix(S, p):
            return p
        if self.move_was_winning_move_for_matrix(S, p * (-1)):
            return p * (-1)
        if not self.move_still_possible_for_matrix(S):
            return 0
        # this state can lead to win as well as to lose, therefore
        max_sum = 0.0
        min_sum = 0.0
        xs_max, ys_max = np.where(S == 1)
        for i in xrange(len(xs_max)):
            max_sum += self.x_stat[xs_max[i]][ys_max[i]]
        xs_min, ys_min = np.where(S == -1)
        for i in xrange(len(xs_min)):
            min_sum += self.x_stat[xs_min[i]][ys_min[i]]
        return max_sum - min_sum
        # this state can lead to win as well as to lose, therefore
        # return 0.5 * p

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
            columns = np.unique(ys)
            for i in xrange(len(columns)):
                new_node = max(self._node_dict.keys()) + 1
                child_state = np.copy(S)
                child_state1 = self.make_move_for_children(child_state, p, columns[i])
                self._node_dict[new_node] = (child_state1, child_p)
                child_list.append(new_node)

            self._child_dict[node] = child_list
            for c in child_list:
                child_state, child_p = self._node_dict[c]
                self._build_tree(c, child_state, child_p, level - 1)

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

    def make_min_max_move(self, p):
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

        S = self.game_state
        current_node = 0
        self._node_dict[current_node] = S, p
        self._build_tree(current_node, S=S, p=p, level=self.level)

        if p == 1:
            self._max_node_util(current_node)
            child_min_max = {c: self._min_max_dict[c]
                             for c in self._child_dict[current_node]}
            child_min_max = sorted(child_min_max.items(), key=lambda x: x[1])
            self.game_state = self._node_dict[child_min_max[-1][0]][0]
            return self._node_dict[child_min_max[-1][0]][0]

        else:
            self._min_node_util(current_node)
            child_min_max = {c: self._min_max_dict[c]
                             for c in self._child_dict[current_node]}
            child_min_max = sorted(child_min_max.items(), key=lambda x: x[1])
            self.game_state = self._node_dict[child_min_max[0][0]][0]
            return self._node_dict[child_min_max[0][0]][0]
