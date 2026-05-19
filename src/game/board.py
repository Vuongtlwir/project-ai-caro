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

    def is_valid_move(self, row, col):

        # ngoài bàn cờ
        if (
            row < 0
            or row >= BOARD_SIZE
            or col < 0
            or col >= BOARD_SIZE
        ):
            return False

        # ô đã có quân
        if self.grid[row][col] != EMPTY:
            return False

        return True

    # =====================================
    # MAKE MOVE
    # =====================================

    def make_move(self, row, col):

        if not self.is_valid_move(row, col):
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

                            # trong bàn cờ
                            if (
                                0 <= nr < BOARD_SIZE
                                and 0 <= nc < BOARD_SIZE
                            ):

                                # ô trống
                                if self.grid[nr][nc] == EMPTY:

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