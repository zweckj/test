import numpy as np
from sys import maxsize as inf

'''
:param curr_board: current board
:param player_no: Number of the player at the current turn
:param i: row of the attempted turn
:param j: column of the attempted turn
:return whether a attempted turn is valid or not (true/false)
'''


def validate_turn(board, player_no, row, column):
    curr_board = board.curr_board
    # attempted turnparameters not inside the field
    if (row > board.field_height or column > board.field_width) and not (row > 0 and column > 0):
        print("Numbers specified not inside the field")
        return False, None
    # player tried to set on a field already owned
    if curr_board[row][column] in range(1, 9):
        print("Field is already owned by player " + str(curr_board[row][column]))
        return False, None
    elif curr_board[row][column] == 99:
            print("Not a valid field")
            return False, None
    elif curr_board[row][column] == 9:
        # TODO choice stone logic
        return False, None
    elif curr_board[row][column] == 10:
        # TODO inversion stone logic
        return False, None
    elif curr_board[row][column] == 11:
        # TODO bonus stone logic
        return False, None
    elif curr_board[row][column] == 12:
        # TODO expasion stone logic
        return False, None
    # empty Field
    elif curr_board[row][column] == 0:
        return validate_reversi_logic(board, player_no, row, column)

    return False


def validate_reversi_logic(board, player_no, row, column):
    curr_board = board.curr_board
    # player range that does not include the currently active player
    opponent_player_range = [x for x in range(1, 9) if x != player_no]

# TODO transition logic!!!!

# TODO not rectangular boards

    valid_turn = False
    north_possible = [False, -inf, -inf]
    south_possible = [False, -inf, -inf]
    east_possible = [False, -inf, -inf]
    west_possible = [False, -inf, -inf]
    northwest_possible = [False, -inf, -inf]
    northeast_possible = [False, -inf, -inf]
    southwest_possible = [False, -inf, -inf]
    southeast_possible = [False, -inf, -inf]

    # check north
    if row > 0:
        if curr_board[row - 1][column] in opponent_player_range:
            for i in range(row - 2, -1, -1):
                if curr_board[i][column] == player_no:
                    north_possible = [True, i, column]
                    valid_turn = True
    # check south
    if row < board.field_height - 1:
        if curr_board[row+1][column] in opponent_player_range:
            for i in range(row + 2, board.field_height):
                if curr_board[i][column] == player_no:
                    south_possible = [True, i, column]
                    valid_turn = True
    # check west
    if column > 0:
        if curr_board[row][column - 1] in opponent_player_range:
            for j in range(column - 2, -1, -1):
                if curr_board[row][j] == player_no:
                    west_possible = [True, row, j]
                    valid_turn = True
    # check east
    if column < board.field_width - 1:
        if curr_board[row][column + 1] in opponent_player_range:
            for j in range(column + 2, board.field_width):
                if curr_board[row][j] == player_no:
                    east_possible = [True, row, j]
                    valid_turn = True

    # check north-east
    if row > 0 and column < board.field_width - 1:
        if curr_board[row - 1][column + 1] in opponent_player_range:
            i = 2
            while row - i >= 0 and column + i < board.field_width:
                if curr_board[row - i][column + i] == player_no:
                    northeast_possible = [True, row - i, column + i]
                    valid_turn = True
                i = i + 1

    # check south-east
    if row < board.field_height - 1 and column < board.field_width - 1:
        if curr_board[row + 1][column + 1] in opponent_player_range:
            i = 2
            while row + i < board.field_height and column + i < board.field_width:
                if curr_board[row + i][column + i] == player_no:
                    southeast_possible = [True, row + i, column + i]
                    valid_turn = True
                i = i + 1

    # check south-west
    if row < board.field_height - 1 and column > 0:
        if curr_board[row + 1][column - 1] in opponent_player_range:
            i = 2
            while row + i < board.field_height and column - i >= 0:
                if curr_board[row + i][column - i] == player_no:
                    southwest_possible = [True, row + i, column - i]
                    valid_turn = True
                i = i + 1

    # check north-west
    if row > 0 and column > 0:
        if curr_board[row - 1][column - 1] in opponent_player_range:
            i = 2
            while row - i >= 0 and column - i >= 0:
                if curr_board[row - i][column - i] == player_no:
                    northwest_possible = [True, row - i, column - i]
                    valid_turn = True
                i = i + 1

    return valid_turn, [north_possible, northeast_possible, east_possible, southeast_possible, south_possible,
                        southwest_possible, west_possible, northwest_possible]
