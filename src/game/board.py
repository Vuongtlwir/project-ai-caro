from src.game.constants import *
from .win_checker import check_win

class Board:

    def __init__(self):

        self.grid = [
            [EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

        self.current_player = HUMAN

        self.move_history = []

        self.last_move = None

    # TRONG BÀN CỜ

    def in_chess_bound(self, row, col):

        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
        )

    # Ô TRỐNG

    def is_empty(self, row, col):

        return self.grid[row][col] == EMPTY

    # VALID MOVE

    def is_valid_move(self, row, col):

        return (
            self.in_chess_bound(row, col)
            and self.is_empty(row, col)
        )

    # MAKE MOVE

    def make_move(self, row, col):

        if not self.is_valid_move(row, col):
            return False

        self.grid[row][col] = self.current_player

        self.move_history.append((row, col))

        self.last_move = (row, col)

        return True

    
    # UNDO MOVE

    def undo_move(self, row, col):

        if not self.move_history:
            return

        last_row, last_col = self.move_history[-1]
        if (row, col) != (last_row, last_col):
            return

        self.grid[row][col] = EMPTY

        self.move_history.pop()

        if self.move_history:
            self.last_move = self.move_history[-1]
        else:
            self.last_move = None

    # SWITCH PLAYER

    def switch_player(self):

        self.current_player *= -1


    # Tạo nước đi giả lập, và hoàn tác
    def make_move_simulate(self, row, col, player):

        if not self.is_valid_move(row, col):
            return False

        self.grid[row][col] = player

        self.move_history.append((row, col))

        self.last_move = (row, col)

        return True


    # Trả ra 1 người cụ thể thắng 
    def get_winner(self):

        if self.last_move is None:
            return None

        row, col = self.last_move

        player = self.grid[row][col]

        if player == EMPTY:
            return None

        if check_win(self.grid, row, col):
            return player

        return None
    # RESET
    def reset(self):

        self.grid = [
            [EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

        self.current_player = HUMAN

        self.move_history.clear()

        self.last_move = None