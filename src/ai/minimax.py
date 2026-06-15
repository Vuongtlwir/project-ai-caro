import math
import time

from typing import Dict, List, Optional

from src.game.board import Board
from src.game.constants import *

from .heuristic import WIN_SCORE, BROKEN_FOUR_SCORE, BROKEN_THREE_SCORE
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
            depth
        )
        if not moves:
            return None, 0
     
        # AI THẮNG NGAY
        for move in moves:

            row, col = move

            board.make_move_simulate(row, col, AI)
            if board.get_winner() == AI:
                board.undo_move(row, col)
                return move, WIN_SCORE

            board.undo_move(row, col)

        # CHẶN PLAYER THẮNG NGAY
        for move in moves:

            row, col = move

            board.make_move_simulate(row, col, HUMAN)

            if board.get_winner() == HUMAN:
                board.undo_move(row, col)
                return move, WIN_SCORE*100 - 1

            board.undo_move(row, col)

        # TẠO THREAT MẠNH CHO AI trước, nhưng vẫn chặn nếu player có threat tức thời
        attack_move = self.find_dangerous_threat_move(board, AI)

        # CHẶNG CÁC THREAT NGUY HIỂM NHẤT (open 4 / closed 4 / broken 4)
        block_move = self.find_immediate_threat_block(board)
        if block_move is not None:
            return block_move, WIN_SCORE * 50 - 1

        if len(board.move_history) == 1 and board.grid[board.move_history[0][0]][board.move_history[0][1]] == HUMAN:
            return moves[0], 0

        if attack_move is not None:
            row, col = attack_move

            board.make_move_simulate(row, col, AI)

            attack_score = self.evaluate(board)

            board.undo_move(row, col)

            if attack_score > 300000:
                return attack_move, attack_score

        # TÌM NƯỚC TẤN CÔNG CHIẾM ƯU THẾ NHANH (open 3, broken 3)
        best_tactical, tactical_score = self.find_best_tactical_move(board, AI)
        if tactical_score >= 200_000:
            return best_tactical, int(tactical_score)

        # MINIMAX

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

            board.undo_move(row, col)

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
            depth
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

                board.undo_move(row, col)

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

                board.undo_move(row, col)

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
    # TẠO THREAT MẠNH CHO AI trước, nhưng vẫn chặn nếu player có threat tức thời.
    def is_dangerous_threat(self, board: Board, player):

        open3_count = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                if board.grid[row][col] != player:
                    continue

                for dr, dc in DIRECTIONS:

                    if self.is_previous_same(board, row, col, dr, dc, player):
                        continue

                    length, open_ends = self.count_sequence(
                        board,
                        row,
                        col,
                        dr,
                        dc,
                        player
                    )

                    if length >= 4 and open_ends >= 1:
                        return True

                    broken_score = self.check_broken_pattern(
                        board,
                        row,
                        col,
                        dr,
                        dc,
                        player
                    )
                    if broken_score >= BROKEN_THREE_SCORE:
                        return True

                    if length == 3 and open_ends == 2:
                        open3_count +=1
        if open3_count >= 1:
            return True
        return False
    # TÌM NƯỚC TẤN CÔNG CHIẾM ƯU THẾ NHANH (open 3, broken 3)
    def find_immediate_threat_block(self, board: Board):

        best_move = None
        best_score = -math.inf

        for row, col in self.get_candidate_moves(board):

            board.make_move_simulate(row, col, AI)

            if not self.is_dangerous_threat(board, HUMAN):

                score = self.evaluate(board)

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

            board.undo_move(row, col)

        return best_move
    
    def find_best_tactical_move(self, board: Board, player: int):

        best_move = None
        best_score = -math.inf

        for row, col in self.get_candidate_moves(board):

            score = self.quick_tactical_score(board, row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move, best_score

    def find_dangerous_threat_move(self, board: Board, player: int):

        best_move = None
        best_score = -1

        for row, col in self.get_candidate_moves(board):

            board.make_move_simulate(row, col, player)

            score = self.count_threat_at(board, row, col, player)

            if self.is_dangerous_threat(board, player):
                score += 500_000

            if score > best_score:
                best_score = score
                best_move = (row, col)

            board.undo_move(row, col)

        return best_move

    def is_time_up(self):

        if self.time_up:
            return True

        if (
            time.perf_counter() - self.start_time
        ) >= self.time_limit_sec:

            self.time_up = True
            return True

        return False