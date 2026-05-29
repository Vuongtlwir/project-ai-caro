import math
import time

from typing import Dict, List, Optional

from src.game.board import Board
from src.game.constants import *

from .heuristic import WIN_SCORE
from .types import Move

from .iterative_deepening import IterativeDeepening
from .heuristic import HeuristicsMixin
from .killer_heuristic import KillerHeuristic
from .move_ordering import MoveOrdering


class Minimax(
    HeuristicsMixin,
    KillerHeuristic,
    MoveOrdering,
    IterativeDeepening
):
    def __init__(self, max_depth=4, time_limit_sec=1.8):

        self.max_depth = max_depth
        self.time_limit_sec = time_limit_sec

        self.start_time = 0.0
        self.time_up = False

        # Killer heuristic
        self.killer_moves: Dict[int, List[Move]] = {}
        self.max_killers_per_depth = 2

        # Cache score move
        self.move_scores: Dict[Move, int] = {}

        # Stats
        self.nodes_evaluated = 0

    def search_root(self, board: Board, depth):

        self.start_time = time.perf_counter()
        self.time_up = False

        alpha = -math.inf
        beta = math.inf

        best_score = -math.inf
        best_move: Optional[Move] = None

        moves = self.order_moves(
            board,
            depth,
            is_maximizing=True
        )
        if not moves:
            return None, 0

        # AI THẮNG NGAY
        for move in moves:

            row, col = move

            board.make_move_simulate(row, col, AI)
            if board.get_winner() == AI:
                board.undo_move_simulate(row, col)
                return move, WIN_SCORE

            board.undo_move_simulate(row, col)

        # CHẶN HUMAN THẮNG NGAY
        for move in moves:

            row, col = move

            board.make_move_simulate(row, col, HUMAN)

            if board.get_winner() == HUMAN:
                board.undo_move_simulate(row, col)
                return move, WIN_SCORE*100 - 1

            board.undo_move_simulate(row, col)

        # =========================================
        # MINIMAX
        # =========================================

        for move in moves:

            if self.is_time_up():
                break

            row, col = move

            board.make_move_simulate(row, col, AI)

            score = self.minimax(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )

            board.undo_move_simulate(row, col)

            self.move_scores[move] = score

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

            if beta <= alpha:
                break

        return best_move, int(best_score)

    def minimax(
        self,
        board: Board,
        depth,
        alpha,
        beta,
        maximizing
    ):

        self.nodes_evaluated += 1

        if self.is_time_up():
            return self.evaluate(board)

        winner = board.get_winner()

        if winner == AI:
            return WIN_SCORE + depth

        if winner == HUMAN:
            return -WIN_SCORE - depth

        if (
            depth == 0
            or len(board.move_history) == BOARD_SIZE * BOARD_SIZE
        ):
            return self.evaluate(board)

        current_player = AI if maximizing else HUMAN

        moves = self.order_moves(
            board,
            depth,
            is_maximizing=maximizing
        )

        if maximizing:

            value = -math.inf

            for row, col in moves:

                board.make_move_simulate(
                    row,
                    col,
                    current_player
                )

                value = max(
                    value,
                    self.minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False
                    )
                )

                board.undo_move_simulate(row, col)

                alpha = max(alpha, value)

                if beta <= alpha:

                    self.store_killer(
                        depth,
                        (row, col)
                    )

                    break

                if self.is_time_up():
                    break

            return int(value)

        else:

            value = math.inf

            for row, col in moves:

                board.make_move_simulate(
                    row,
                    col,
                    current_player
                )

                value = min(
                    value,
                    self.minimax(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True
                    )
                )

                board.undo_move_simulate(row, col)

                beta = min(beta, value)

                if beta <= alpha:

                    self.store_killer(
                        depth,
                        (row, col)
                    )

                    break

                if self.is_time_up():
                    break

            return int(value)

    def is_time_up(self):

        if self.time_up:
            return True

        if (
            time.perf_counter() - self.start_time
        ) >= self.time_limit_sec:

            self.time_up = True
            return True

        return False
