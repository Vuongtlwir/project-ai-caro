from typing import List, Set

from src.game.board import Board

from .types import Move
from src.game.constants import *
from .heuristic import CENTER_BONUS, NEIGHBOR_RADIUS, OPPONENT_WEIGHT

NEAREST_STONE_BONUS = 12

class MoveOrdering:

    #Sắp xếp các nước đi tiềm năng dựa trên một số tiêu chí(các ô trống trong bán kính lân cận) để cải thiện hiệu quả của cắt Alpha-Beta.
    def get_candidate_moves(self, board: Board):

        if not board.move_history:
            center = BOARD_SIZE //2
            return [(center, center)]
        
        search_radius = 2 if len(board.move_history) == 1 else NEIGHBOR_RADIUS
        candidate: Set[Move] = set()

        for row, col in board.move_history:

            for dr in range(-search_radius, search_radius +1):
                for dc in range(-search_radius, search_radius +1):
                    if dr == 0 and dc ==0:
                        continue
                    nr = row +dr
                    nc = col +dc

                    if board.in_chess_bound(nr, nc) and board.is_empty(nr, nc):
                        candidate.add((nr,nc))
        
        return list(candidate)
    #Sắp xếp các nước đi để tối ưu hiệu quả cắt tỉa alpha-beta.
    #Ưu tiên: Các nước đi tốt nhất trước đó, Các nước đi mang tính quyết định, Giá trị chiến thuật
    def order_moves(self, board: Board, depth: int, is_maximizing: bool):

        moves = self.get_candidate_moves(board)
        if not moves:
            return moves
        
        center = BOARD_SIZE //2
        killer = self.killer_moves.get(depth, [])
        def score_move(move):
            row, col = move
            score = 0.0
            if move in self.move_scores:
                score += self.move_scores[move] * 0.01
            
            if move in killer:
                score += 100000

            tactical = self.quick_tactical_score(board, row, col)
            score += tactical
            # TĂNG ĐIỂM CHO NƯỚC ĐI TẠO THREAT MẠNH
            board.make_move_simulate(row, col, AI)
            threat_score = self.count_threat_at(
                board,
                row,
                col,
                AI
            )

            score += threat_score * 5

            if self.is_dangerous_threat(board, AI):
                score += 300_000
            board.undo_move(row, col)

            # CHỐNG THREAT CỦA player
            if self.is_dangerous_threat(board, HUMAN):

                board.make_move_simulate(row, col, AI)

                if not self.is_dangerous_threat(board, HUMAN):
                    score += 500_000

                board.undo_move(row, col)

            
            
            distance = abs(row - center) + abs(col -center)
            score += CENTER_BONUS * (BOARD_SIZE *2 - distance)

            nearest_distance = min(
                abs(row - r) + abs(col - c)
                for r, c in board.move_history
            )

            if len(board.move_history) == 1 and board.grid[board.move_history[0][0]][board.move_history[0][1]] == HUMAN:
                score += 1600 - nearest_distance * 240
            else:
                score += NEAREST_STONE_BONUS * (
                    BOARD_SIZE * 2 - nearest_distance
                )

            return score
        moves.sort( key = score_move, reverse = True)

        max_moves = 40 if depth >= 3 else 24
        if len(moves) > max_moves:
            moves = moves[:max_moves]
            
        return moves