import math, time
from src.game.board import Board

from .heuristic import WIN_SCORE


#Sử dụng phương pháp iterative deepening (Lặp đi lặp lại) để tìm nước đi tốt nhất trong thời gian giới hạn.
#Mỗi lần lặp sử dụng thuật toán Minimax với cắt Alpha-Beta.


class IterativeDeepening:
    def choose_move(self, board: Board):
        self.start_time = time.perf_counter()
        self.time_up = False
        self.killer_moves.clear()
        self.move_scores.clear()
        self.nodes_evaluated = 0

        legal_moves = self.get_candidate_moves(board)

        if not legal_moves:
            return None
        
        if len(legal_moves) == 1:
            return legal_moves[0]
        best_move = legal_moves[0]
        best_score = -math.inf

        for depth in range(1, self.max_depth +1):
            if self.is_time_up():
                break
            
            move, score = self.search_root(board, depth)
            
            if move is not None and not self.is_time_up():
                best_move = move
                best_score = score

                if score >= WIN_SCORE - 1000:
                    break

        return best_move 