from src.game.constants import *


class Board:

    def __init__(self):

        self.grid = [
            [EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

        self.current_player = HUMAN

        self.move_history = []

    # =====================================
    # VALID MOVE
    # =====================================

    # Trong bàn cờ
    def in_chess_bound(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    # Ô trống
    def is_empty(self, row, col):
        return self.grid[row][col] == EMPTY
        

    # =====================================
    # MAKE MOVE
    # =====================================

    def make_move(self, row, col):

        if not self.in_chess_bound(row, col ) or not self.is_empty(row, col):
            return False

        self.grid[row][col] = self.current_player

        self.move_history.append((row, col))

        return True

    # =====================================
    # UNDO MOVE
    # =====================================

    def undo_move(self):

        if not self.move_history:
            return

        row, col = self.move_history.pop()

        self.grid[row][col] = EMPTY

    # =====================================
    # SWITCH PLAYER
    # =====================================

    def switch_player(self):

        self.current_player *= -1

    # =====================================
    # AVAILABLE NEIGHBORS
    # =====================================

    def available_neighbors(self):

        moves = set()

        # bàn cờ trống
        if len(self.move_history) == 0:

            center = BOARD_SIZE // 2

            return [(center, center)]

        for row in range(BOARD_SIZE):

            for col in range(BOARD_SIZE):

                # có quân cờ
                if self.grid[row][col] != EMPTY:

                    # xét 8 hướng xung quanh
                    for dr in [-1, 0, 1]:

                        for dc in [-1, 0, 1]:

                            if dr == 0 and dc == 0:
                                continue

                            nr = row + dr
                            nc = col + dc

                            
                            if ( self.in_chess_bound(nr, nc) and self.is_empty(nr, nc)):
                                    moves.add((nr, nc))

        return list(moves)

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        self.grid = [
            [EMPTY for _ in range(BOARD_SIZE)]
            for _ in range(BOARD_SIZE)
        ]

        self.current_player = HUMAN

        self.move_history.clear()