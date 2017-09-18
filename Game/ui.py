''' Class to incorporate all user interaction '''
from board import Board
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
            row = int(i)
            column = int(j)

            valid, valid_options = validate_turn(self.board, player_no, row, column)
            if valid:
                self.make_move(player_no, row, column, valid_options)
                self.board.curr_board[row][column] = player_no
                if player_no == board.no_players:
                    player_no = 1
                else:
                    player_no = player_no + 1
            else:
                print("Attempted turn not possible")
        return

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