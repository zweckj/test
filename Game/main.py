from board import Board
from ui import UI
import numpy as np
with open("standard_board.txt") as f:
    lines = [line.rstrip('\n') for line in f]
board = Board(lines)
ui = UI(board)
