import numpy as np
from sys import maxsize as inf
from const import INVALID_FIELD

'''
:param curr_board: current board
:param player_no: Number of the player at the current turn
:param i: row of the attempted turn
:param j: column of the attempted turn
:return whether a attempted turn is valid or not (true/false)
'''


def validate_turn(board, player_no, row, col):
    curr_board = board.curr_board
    # attempted turnparameters not inside the field
    if (row > board.field_height or col > board.field_width) and not (row > 0 and col > 0):
        print("Numbers specified not inside the field")
        return False, None
    # player tried to set on a field already owned
    if curr_board[row][col] in range(1, 9):
        print("Field is already owned by player " + str(curr_board[row][col]))
        return False, None
    elif curr_board[row][col] == INVALID_FIELD:
            print("Not a valid field")
            return False, None
    elif curr_board[row][col] == 9:
        # TODO choice stone logic
        return False, None
    elif curr_board[row][col] == 10:
        # TODO inversion stone logic
        return False, None
    elif curr_board[row][col] == 11:
        # TODO bonus stone logic
        return False, None
    elif curr_board[row][col] == 12:
        # TODO expasion stone logic
        return False, None
    # empty Field
    elif curr_board[row][col] == 0:
        return validate_reversi_logic(board, player_no, row, col)

    return False


def validate_reversi_logic(board, player_no, row, col):
    # player range that does not include the currently active player
    opponent_player_range = [x for x in range(1, 9) if x != player_no]

    valid_turn = False

    possibilities = [
        check_north(board, player_no, row, col, opponent_player_range),
        check_northeast(board, player_no, row, col, opponent_player_range),
        check_east(board, player_no, row, col, opponent_player_range),
        check_southeast(board, player_no, row, col, opponent_player_range),
        check_south(board, player_no, row, col, opponent_player_range),
        check_southwest(board, player_no, row, col, opponent_player_range),
        check_west(board, player_no, row, col, opponent_player_range),
        check_northwest(board, player_no, row, col, opponent_player_range)
    ]

    # check if turn is valid at all
    for p in possibilities:
            if p[0]:
                valid_turn = True
                break

    return valid_turn, possibilities


def transition(board, player_no, opponent_player_range, from_row, from_col, direction):

    # search for existing transition
    for t in board.transitions:
        if [from_row, from_col, direction] == t[0]:
            # get direction after transitioning
            new_direction = t[1][2]
            # get target coordinates of transition
            to_transition = t[1][0:2]

            # continue checking in new transition's direction
            if new_direction == 0:
                return check_south(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 1:
                return check_southwest(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 2:
                return check_west(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 3:
                return check_northwest(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 4:
                return check_north(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 5:
                return check_northeast(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 6:
                return check_east(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
            elif new_direction == 7:
                return check_southeast(board, player_no, to_transition[0], to_transition[1], opponent_player_range)
    return [False, -inf, -inf]


def check_north(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row > 0:
        i = 0
        # Opponent stone present?
        if curr_board[row - 1][col] in opponent_player_range:
            for i in range(row - 2, -1, -1):
                # find another opponent stone, just continue searching
                if curr_board[i][col] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[i][col] == player_no:
                    return [True, i, col]
                # Found a hole
                elif curr_board[i][col] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, i + 1, col, 0)
                # Found empty Field
                elif curr_board[i][col] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, i, col, 0)
        # Found hole in board
        elif curr_board[row - 1][col] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 0)
        # Found empty Field
        elif curr_board[row - 1][col] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 0)


def check_northeast(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row > 0 and col < board.field_width - 1:
        # Opponent stone present?
        if curr_board[row - 1][col + 1] in opponent_player_range:
            i = 1
            while row - i > 0 and col + i < board.field_width - 1:
                i = i + 1
                # find another opponent stone, just continue searching
                if curr_board[row - i][col + i] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row - i][col + i] == player_no:
                    return [True, row - i, col + i]
                # Found a hole
                elif curr_board[row - i][col + i] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row - i + 1, col + i - 1, 1)
                # Found empty Field
                elif curr_board[row - i][col + i] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row - i, col + i, 1)
        # Found hole in board
        elif curr_board[row - 1][col + 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 1)
        # Found empty Field
        elif curr_board[row - 1][col + 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 1)


def check_east(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if col < board.field_width - 1:
        j = 0
        # Opponent stone present?
        if curr_board[row][col + 1] in opponent_player_range:
            for j in range(col + 2, board.field_width):
                # find another opponent stone, just continue searching
                if curr_board[row][j] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row][j] == player_no:
                    return [True, row, j]
                # Found a hole
                elif curr_board[row][j] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row, j - 1, 2)
                # Found empty Field
                elif curr_board[row][j] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row, j, 2)
        # Found hole in board
        elif curr_board[row][col + 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 2)
        # Found empty Field
        elif curr_board[row][col + 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 2)


def check_southeast(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row < board.field_height - 1 and col < board.field_width - 1:
        # Opponent stone present?
        if curr_board[row + 1][col + 1] in opponent_player_range:
            i = 1
            while row + i < board.field_height - 1 and col + i < board.field_width - 1:
                i = i + 1
                # find another opponent stone, just continue searching
                if curr_board[row + i][col + i] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row + i][col + i] == player_no:
                    return [True, row + i, col + i]
                # Found a hole
                elif curr_board[row + i][col + i] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row + i - 1, col + i - 1, 3)
                # Found empty Field
                elif curr_board[row + i][col + i] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row + i, col + i, 3)
        # Found hole in board
        elif curr_board[row + 1][col + 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 3)
        # Found empty Field
        elif curr_board[row + 1][col + 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 3)


def check_south(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row < board.field_height - 1:
        i = 0
        # Opponent stone present?
        if curr_board[row + 1][col] in opponent_player_range:
            for i in range(row + 2, board.field_height):
                # find another opponent stone, just continue searching
                if curr_board[i][col] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[i][col] == player_no:
                    return [True, i, col]
                # Found a hole
                elif curr_board[i][col] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, i - 1, col, 4)
                # Found empty Field
                elif curr_board[i][col] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, i, col, 4)
        # Found hole in board
        elif curr_board[row + 1][col] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 4)
        # Found empty Field
        elif curr_board[row + 1][col] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 4)


def check_southwest(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row < board.field_height - 1 and col > 0:
        # Opponent stone present?
        if curr_board[row + 1][col - 1] in opponent_player_range:
            i = 1
            while row + i < board.field_height - 1 and col - i > 0:
                i = i + 1
                # find another opponent stone, just continue searching
                if curr_board[row + i][col - i] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row + i][col - i] == player_no:
                    return [True, row + i, col - i]
                # Found a hole
                elif curr_board[row + i][col - i] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row + i - 1, col - i + 1, 5)
                # Found empty Field
                elif curr_board[row + i][col - i] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row + i, col - i, 5)
        # Found hole in board
        elif curr_board[row + 1][col - 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 5)
        # Found empty Field
        elif curr_board[row + 1][col - 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 5)


def check_west(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if col > 0:
        j = 0
        # Opponent stone present?
        if curr_board[row][col - 1] in opponent_player_range:
            for j in range(col - 2, -1, -1):
                # find another opponent stone, just continue searching
                if curr_board[row][j] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row][j] == player_no:
                    return [True, row, j]
                # Found a hole
                elif curr_board[row][j] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row, j + 1, 6)
                # Found empty Field
                elif curr_board[row][j] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row, j, 6)
        # Found hole in board
        elif curr_board[row][col - 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 6)
        # Found empty Field
        elif curr_board[row][col - 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 6)


def check_northwest(board, player_no, row, col, opponent_player_range):
    curr_board = board.curr_board
    # Check for board edge
    if row > 0 and col > 0:
        # Opponent stone present?
        if curr_board[row - 1][col - 1] in opponent_player_range:
            i = 1
            while row - i > 0 and col - i > 0:
                i = i + 1
                # find another opponent stone, just continue searching
                if curr_board[row - i][col - i] in opponent_player_range:
                    continue
                # Found a player stone after continuous opponent stones => valid turn
                if curr_board[row - i][col - i] == player_no:
                    return [True, row - i, col - i]
                # Found a hole
                elif curr_board[row - i][col - i] == INVALID_FIELD:
                    return transition(board, player_no, opponent_player_range, row - i + 1, col - i + 1, 7)
                # Found empty Field
                elif curr_board[row - i][col - i] == 0:
                    return [False, -inf, -inf]
            # edge of board reached, search for transition
            return transition(board, player_no, row - i, col - i, 7)
        # Found hole in board
        elif curr_board[row - 1][col - 1] == INVALID_FIELD:
            return transition(board, player_no, opponent_player_range, row, col, 7)
        # Found empty Field
        elif curr_board[row - 1][col - 1] == 0:
            return [False, -inf, -inf]
    # search for outgoing transition
    else:
        return transition(board, player_no, row, col, 7)
