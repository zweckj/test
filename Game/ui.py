''' Class to incorporate all user interaction '''
from turn_validation import validate_turn


class UI:

    board = None

    def __init__(self, board):
        self.board = board
        player_no = 1
        while True:
            print("Player's " + str(player_no) + " turn!")
            print(board.curr_board)
            i = input("Please enter row: ")
            j = input("Please enter column: ")

            try:
                row = int(i)
                column = int(j)
            except (TypeError, ValueError):
                print("Please enter a number")
                continue

            valid, valid_options = validate_turn(self.board, player_no, row, column)

            if valid:
                self.make_move_2(player_no, row, column, valid_options)
                self.board.curr_board[row][column] = player_no
                if player_no == board.no_players:
                    player_no = 1
                else:
                    player_no = player_no + 1
            else:
                print("Attempted turn not possible")

    '''
        function to actually execute the turn, and switch opponent players stones
        :param player_no 
    '''
    def make_move(self, player_no, row, column, valid_options):

        # north
        if valid_options[0][0]:
            i = 0
            while row - i >= valid_options[0][1]:
                self.board.curr_board[row - i][column] = player_no
                i = i + 1
        # north east
        if valid_options[1][0]:
            i = 0
            while row - i >= valid_options[1][1] and column + i <= valid_options[1][2]:
                self.board.curr_board[row - i][column + i] = player_no
                i = i + 1
        # east
        if valid_options[2][0]:
            i = 0
            while column + i <= valid_options[2][2]:
                self.board.curr_board[row][column + i] = player_no
                i = i + 1
        # southeast
        if valid_options[3][0]:
            i = 0
            while row + i <= valid_options[3][1] and column + i <= valid_options[3][2]:
                self.board.curr_board[row + i][column + i] = player_no
                i = i + 1
        # south
        if valid_options[4][0]:
            i = 0
            while row + i <= valid_options[4][1]:
                self.board.curr_board[row + i][column] = player_no
                i = i + 1
        # south west
        if valid_options[5][0]:
            i = 0
            while row + i <= valid_options[5][1] and column - i >= valid_options[5][2]:
                self.board.curr_board[row + i][column - i] = player_no
                i = i + 1
        # west
        if valid_options[6][0]:
            i = 0
            while column - i >= valid_options[6][2]:
                self.board.curr_board[row][column - i] = player_no
                i = i + 1
        # north west
        if valid_options[7][0]:
            i = 0
            while row - i >= valid_options[7][1] and column - i >= valid_options[7][2]:
                self.board.curr_board[row - i][column - i] = player_no
                i = i + 1

    def make_move_2(self, player_no, row, col, valid_options):

        if valid_options[0][0]:
            self.move_north(player_no, valid_options[0][1:], row, col)
        elif valid_options[1][0]:
            self.move_northeast(player_no, valid_options[1][1:], row, col)
        elif valid_options[2][0]:
            self.move_east(player_no, valid_options[2][1:], row, col)
        elif valid_options[3][0]:
            self.move_southeast(player_no, valid_options[3][1:], row, col)
        elif valid_options[4][0]:
            self.move_south(player_no, valid_options[4][1:], row, col)
        elif valid_options[5][0]:
            self.move_southwest(player_no, valid_options[5][1:], row, col)
        elif valid_options[6][0]:
            self.move_west(player_no, valid_options[6][1:], row, col)
        elif valid_options[7][0]:
            self.move_northwest(player_no, valid_options[7][1:], row, col)

    def transition(self, player_no, target, from_row, from_col, direction):

        to_transition = []
        # search matching transition
        for t in self.board.transitions:
            if t[0] == [from_row, from_col, direction]:
                to_transition = t[1]
                break
        # find a transition, continue moving in given direction
        if not to_transition == []:
            if to_transition[2] == 0:
                self.move_south(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 1:
                self.move_southwest(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 2:
                self.move_west(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 3:
                self.move_northwest(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 4:
                self.move_north(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 5:
                self.move_northeast(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 6:
                self.move_east(player_no, target, to_transition[0], to_transition[1])
            elif to_transition[2] == 7:
                self.move_southeast(player_no, target, to_transition[0], to_transition[1])

    def move_north(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row - i >= 0:
            # found opponent stone => overwrite
            if self.board.curr_board[row - i][col] in opponent_player_range:
                self.board.curr_board[row - i][col] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row - i, col] == target:
                self.transition(player_no, target, row - i + 1, col, 0)
            elif [row - i, col] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [0, col] == target:
            self.transition(player_no, target, 0, col, 0)

    def move_northeast(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row - i >= 0 and col + i < self.board.field_width:
            # found opponent stone => overwrite
            if self.board.curr_board[row - i][col + i] in opponent_player_range:
                self.board.curr_board[row - i][col + i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row - i, col + i] == target:
                self.transition(player_no, target, row - i + 1, col + i - 1, 1)
            elif [row - i, col + i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row - i - 1, col -i - 1] == target:
            self.transition(player_no, target, row - i + 1, col + i - 1, 1)

    def move_east(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while col + i < self.board.field_width:
            # found opponent stone => overwrite
            if self.board.curr_board[row][col + i] in opponent_player_range:
                self.board.curr_board[row][col + i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row, col + i] == target:
                self.transition(player_no, target, row, col + i - 1, 2)
            elif [row, col + i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row, col + i - 1] == target:
            self.transition(player_no, target, row, col + i - 1, 2)

    def move_southeast(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row + i < self.board.field_height and col + i < self.board.field_width:
            # found opponent stone => overwrite
            if self.board.curr_board[row + i][col + i] in opponent_player_range:
                self.board.curr_board[row + i][col + i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row + i, col + i] == target:
                self.transition(player_no, target, row + i - 1, col + i - 1, 3)
            elif [row + i, col + i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row + i - 1, col + i - 1] == target:
            self.transition(player_no, target, row + i - 1, col + i - 1, 3)

    def move_south(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row + i < self.board.field_height:
            # found opponent stone => overwrite
            if self.board.curr_board[row + i][col] in opponent_player_range:
                self.board.curr_board[row + i][col] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row + i, col] == target:
                self.transition(player_no, target, row + i - 1, col, 4)
            elif [row + i, col] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [self.board.field_height - 1, col] == target:
            self.transition(player_no, target, self.board.field_height - 1, col, 4)

    def move_southwest(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row + i < self.board.field_height and col - i >= 0:
            # found opponent stone => overwrite
            if self.board.curr_board[row + i][col - i] in opponent_player_range:
                self.board.curr_board[row + i][col - i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row + i, col - i] == target:
                self.transition(player_no, target, row + i - 1, col - i + 1, 5)
            elif [row + i, col - i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row + i - 1, col - i + 1] == target:
            self.transition(player_no, target, row + i - 1, col - i + 1, 5)

    def move_west(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while col - i >= 0:
            # found opponent stone => overwrite
            if self.board.curr_board[row][col - i] in opponent_player_range:
                self.board.curr_board[row][col - i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row, col - i] == target:
                self.transition(player_no, target, row, col - i + 1, 6)
            elif [row, col - i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row, col - i + 1] == target:
            self.transition(player_no, target, row, col - i + 1, 6)

    def move_northwest(self, player_no, target, row, col):
        opponent_player_range = [x for x in range(1, 9) if x != player_no]

        self.board.curr_board[row][col] = player_no
        i = 1
        # go step
        while row - i >= 0 and col - i >= 0:
            # found opponent stone => overwrite
            if self.board.curr_board[row - i][col - i] in opponent_player_range:
                self.board.curr_board[row - i][col - i] = player_no
            # found something that is not opponent and not target stone => transition
            elif not [row - i, col - i] == target:
                self.transition(player_no, target, row - i + 1, col - i + 1, 7)
            elif [row - i, col - i] == target:
                return
            i = i + 1
        # at board edge => transition
        if not [row - i + 1, col - i + 1] == target:
            self.transition(player_no, target, row - i + 1, col - i + 1, 7)



