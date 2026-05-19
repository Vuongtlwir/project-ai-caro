from src.game.constants import *


def count_direction(board, row, col, dx, dy, player):

    count = 0

    r = row + dx
    c = col + dy

    while (
        0 <= r < BOARD_SIZE
        and 0 <= c < BOARD_SIZE
        and board[r][c] == player
    ):

        count += 1

        r += dx
        c += dy

    return count


def check_win(board, row, col):

    player = board[row][col]

    if player == EMPTY:
        return False

    for dx, dy in DIRECTIONS:

        total = 1

        total += count_direction(
            board,
            row,
            col,
            dx,
            dy,
            player
        )

        total += count_direction(
            board,
            row,
            col,
            -dx,
            -dy,
            player
        )

        if total >= WIN_LENGTH:
            return True

    return False