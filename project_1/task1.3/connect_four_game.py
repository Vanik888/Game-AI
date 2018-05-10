import numpy as np
from constants import *


class ConnectFourGame:
    def __init__(self):
        self.game_state = np.zeros((n_rows, n_columns), dtype=int)
        self.last_inserted_column = -1
        self.last_inserted_row = -1

    """Prints current game state"""
    def print_game_state(self):
        state_matrix = np.copy(self.game_state.astype(object))

        for n in [-1, 0, 1]:
            state_matrix[state_matrix == n] = symbols[n]
        print state_matrix
        print "\n"

    """
    If parameter column is equal to None, that means, that
    move is made at random.
    """
    def make_move(self, p, column=None):
        if column is None:
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

    """This method checks whether one player has won the game"""
    def move_was_winning_move(self):

        # Check all rows if there is a winning combination
        # for i in range(n_rows):
        row_to_check = self.game_state[self.last_inserted_row, :]
        if (row_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(row_to_check):
                return True

        # Check all columns if there is a winning combination
        # for i in range(n_columns):
        column_to_check = self.game_state[:, self.last_inserted_column]
        if (column_to_check == 0).sum() <= 3:
            if self.__check_all_sublists(column_to_check):
                return True

        # TODO proper naming in comments required

        # Check all diagonals of length at least 4
        # if there is a winning combination
        for i in diagonal_shifts:
            diagonal = self.game_state.diagonal(i)
            if (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal):
                    return True

        # Check all non-main diagonals of length at least 4
        # if there is a winning combination
        for i in diagonal_shifts:
            # matrix is rotated. diagonals are shifted
            diagonal = np.rot90(self.game_state).diagonal(i - 1)
            if (diagonal == 0).sum() <= 3:
                if self.__check_all_sublists(diagonal):
                    return True
        return False

    """Constructs sublists of given list and
    check whether there is a winning combination for sublists with length 4"""
    def __check_all_sublists(self, list_to_check):
        sublists = [list_to_check[i:i + winning_sum] for i in
                    range(0, len(list_to_check), 1)]

        for sublist in sublists:
            if len(sublist) < winning_sum:
                continue
            if np.abs(np.sum(sublist)) == winning_sum:
                return True

        return False

    """Checks whether there are still empty cells in matrix"""
    def move_still_possible(self):
        return not (self.game_state[self.game_state == 0].size == 0)

    """Returns index of randomly chosen column for element insertion"""
    def __select_column_at_random(self):
        xs, ys = np.where(self.game_state == 0)
        i = np.random.permutation(np.arange(ys.size))[0]
        return ys[i]
