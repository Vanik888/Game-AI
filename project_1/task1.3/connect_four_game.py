import numpy as np
from constants import *


class ConnectFourGame:
    def __init__(self):
        self.game_state = np.zeros((n_rows, n_columns), dtype=int)

    def print_game_state(self):
        state_matrix = np.copy(self.game_state.astype(object))

        for n in [-1, 0, 1]:
            state_matrix[state_matrix == n] = symbols[n]
        print state_matrix
        print "\n"

    def make_move(self, p, column=None):
        if column is None:
            column = self.__select_column_at_random()

        chosen_column = self.game_state[:, column]
        desired_row = -1
        for i, e in list(enumerate(chosen_column)):
            if e == 0:
                desired_row = i

        if desired_row != -1:
            self.game_state[desired_row, column] = p

        if self.__move_was_winning_move(p):
            print "last player wins"

    def __move_was_winning_move(self, p):

        x_axis_sums = (np.sum(self.game_state, axis=0)) * p
        for i, x_sum in list(enumerate(x_axis_sums)):
            # if x_sum == winning_sum:
            row_to_check = self.game_state[:, i]
            if (row_to_check == 0).sum() <= 3:
                if self.__check_all_sublists(row_to_check):
                    return True

        y_axis_sums = (np.sum(self.game_state, axis=1)) * p
        for i, y_sum in list(enumerate(y_axis_sums)):
            # if y_sum == winning_sum:
            column_to_check = self.game_state[i, :]
            if (column_to_check == 0).sum() <= 3:
                if self.__check_all_sublists(column_to_check):
                    return True

        for i in diagonal_shifts:
            diagonal = self.game_state.diagonal(i)
            if (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal):
                    return True

        for i in diagonal_shifts:
            diagonal = np.rot90(self.game_state).diagonal(i)
            if (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal):
                    return True
        return False

    def __check_all_sublists(self, list_to_check):
        sublists = [list_to_check[i:i + winning_sum] for i in
                    range(0, len(list_to_check), 1)]

        for sublist in sublists:
            if len(sublist) < winning_sum:
                continue
            if np.sum(sublist) == winning_sum:
                return True

        return False

    def __select_column_at_random(self):
        xs, ys = np.where(self.game_state == 0)
        i = np.random.permutation(np.arange(xs.size))[0]
        return xs[i]

    def move_still_possible(self):
        return not (self.game_state[self.game_state == 0].size == 0)
