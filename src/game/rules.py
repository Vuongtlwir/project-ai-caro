from src.game.constants import *
from src.game.win_checker import check_win


def get_game_result(board, row, col):

    # check win
    if check_win(board, row, col):
        return board[row][col]

    # check draw
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            if board[r][c] == EMPTY:
                return None

    return DRAW