'''
 class to define and create the board
'''
import numpy as np
from const import INVALID_FIELD


class Board:

    no_players = 2  # number of players
    field_width = 8  # field width
    field_height = 8  # field height
    no_bombs = 0  # number of bombs
    bomb_strength = 0  # strength of bombs
    no_overwritestones = 0  # number of overwritestones
    curr_board = []  # current board status
    transitions = []  # transitions over board edges in format
    # [[from_row, from_col, direction][to_row, to_col, direction]]

    ''' read board specification and incorporate it in this class '''
    def __init__(self, board_def):
        self.no_players = int(board_def[0][0])
        self.no_overwritestones = int(board_def[1][0])
        self.no_bombs = int(board_def[2][0])
        self.bomb_strength = int(board_def[2][2])
        self.field_height = int(board_def[3][0])
        self.field_width = int(board_def[3][2])
        # create empty numpy array with board dimensions
        self.curr_board = np.empty([self.field_height, self.field_width])
        # make numpy array to ints
        self.curr_board = self.curr_board.astype(int)

        # custom index variables for numpy array
        x = 0
        for i in range(4, 4 + self.field_height):
            curr_line = board_def[i].split(" ")
            for j in range(0, self.field_width):
                ''' choicestone (c) = 9, inversion stone (i) = 10, bonus stone (b) = 11, 
                    expansion (x) = 12, invalid field (-) = INVALID_FIELD'''
                curr_item = curr_line[j]
                if curr_item == "-":
                    self.curr_board[x][j] = INVALID_FIELD
                elif curr_item == "c":
                    self.curr_board[x][j] = 9
                elif curr_item == "i":
                    self.curr_board[x][j] = 10
                elif curr_item == "b":
                    self.curr_board[x][j] = 11
                elif curr_item == "x":
                    self.curr_board[x][j] = 12
                else:
                    self.curr_board[x][j] = curr_item
            x = x + 1  # count numpy array to next row
        # import transitions
        i = 4 + self.field_height
        while i < len(board_def):
            curr_line = board_def[i].split(" ")
            self.transitions.append([list(map(int, curr_line[:3])), list(map(int, curr_line[4:]))])
            self.transitions.append([list(map(int, curr_line[4:])), list(map(int, curr_line[:3]))])
            i = i + 1
        print(self.transitions)