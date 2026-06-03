import random

from src.game.board import Board
from src.game.constants import *


class EasyAI:
    """
    AI dễ: thuật toán tham lam (greedy) đơn giản, KHÔNG dùng minimax.

    """

    def __init__(self, mistake_chance=0.25):
        # Xác suất AI bỏ qua nước tốt nhất để chọn nước kém hơn
        self.mistake_chance = mistake_chance



    def choose_move(self, board: Board):

        moves = self.get_candidate_moves(board)

        if not moves:
            return None

        # Nước đầu tiên: đánh giữa bàn
        if len(board.move_history) == 0:
            center = BOARD_SIZE // 2
            return (center, center)

        # 1) Thắng ngay
        win = self.find_winning_move(board, AI)
        if win is not None:
            return win

        # 2) Chặn đối thủ thắng ngay
        block = self.find_winning_move(board, HUMAN)
        if block is not None:
            return block

        # 3) Chấm điểm tham lam
        scored = []
        for (r, c) in moves:
            score = (
                self.score_cell(board, r, c, AI)
                + self.score_cell(board, r, c, HUMAN)  # cũng thích phá thế đối thủ
            )
            scored.append((score, (r, c)))

        scored.sort(reverse=True, key=lambda x: x[0])

        # Thỉnh thoảng đi "ngu" cho dễ
        if random.random() < self.mistake_chance and len(scored) > 1:
            # chọn ngẫu nhiên trong nửa trên (trừ nước tốt nhất)
            upper = scored[1:max(2, len(scored) // 2)]
            return random.choice(upper)[1]

        # Chọn ngẫu nhiên giữa các nước có điểm cao nhất
        best_score = scored[0][0]
        best_moves = [m for s, m in scored if s == best_score]
        return random.choice(best_moves)



    def find_winning_move(self, board: Board, player):
        """Tìm ô mà nếu player đánh vào sẽ thắng ngay."""
        for (r, c) in self.get_candidate_moves(board):
            board.make_move_simulate(r, c, player)
            won = board.get_winner() == player
            board.undo_move(r, c)
            if won:
                return (r, c)
        return None



    def score_cell(self, board: Board, row, col, player):
        """
        Điểm của 1 ô = tổng độ dài chuỗi liên tiếp tạo được theo 4 hướng.
        Đơn giản, không phân biệt open/closed kỹ như heuristic xịn.
        """
        total = 0

        for dr, dc in DIRECTIONS:
            count = 1  # tính cả ô đang xét

            # về phía trước
            count += self.count_dir(board, row, col, dr, dc, player)
            # về phía sau
            count += self.count_dir(board, row, col, -dr, -dc, player)

            # thưởng theo cấp số nhân nhẹ cho chuỗi dài
            total += count * count

        return total

    def count_dir(self, board: Board, row, col, dr, dc, player):
        cnt = 0
        r = row + dr
        c = col + dc
        while (
            board.in_chess_bound(r, c)
            and board.grid[r][c] == player
        ):
            cnt += 1
            r += dr
            c += dc
        return cnt



    def get_candidate_moves(self, board: Board, radius=1):
        """Các ô trống nằm cạnh quân đã đánh (giảm không gian tìm kiếm)."""
        if not board.move_history:
            center = BOARD_SIZE // 2
            return [(center, center)]

        candidates = set()
        for (r, c) in board.move_history:
            for dr in range(-radius, radius + 1):
                for dc in range(-radius, radius + 1):
                    nr, nc = r + dr, c + dc
                    if (
                        board.in_chess_bound(nr, nc)
                        and board.is_empty(nr, nc)
                    ):
                        candidates.add((nr, nc))

        return list(candidates)
