from .types import Score
from src.game.constants import *
from src.game.board import Board
from typing import Set, Tuple, List


WIN_SCORE: Score = 10_000_000

# Score table by (sequence_length, open_ends)

PATTERN_SCORES = {
    # Winning patterns
    (5, 0): WIN_SCORE,
    (5, 1): WIN_SCORE,
    (5, 2): WIN_SCORE,
    
    # Open 4 (2 ĐẦU ĐỀU MỞ : KHÔNG THỂ CHẶN)
    (4, 2): 500_000,
    # Blocked 4 (CHẶN 1 ĐẦU)
    (4, 1): 50_000,
    
    # Open 3 (2 ĐẦU ĐỀU MỞ)
    (3, 2): 18_000,
    # Blocked 3 ( CHẶN 1 ĐẦU )
    (3, 1): 1_500,
    
    # Open 2
    (2, 2): 100,
    # Blocked 2
    (2, 1): 10,
    
    # ĐƠN
    (1, 2): 5,
    (1, 1): 1,
}

# Double threat bonus: ĐIỂM THƯỞNG CHO NHIỀU OPEN 3 OPEN 4
DOUBLE_THREAT_BONUS = 100_000


# NGĂN CHẶN CÁC ĐIỂM QUAN TRỌNG (e.g., XX_XX, X_XXX) - KHOẢNG TRỐNG TRONG CHUỖI
BROKEN_FOUR_SCORE = 100_000  # X_XXX or XX_XX pattern
BROKEN_THREE_SCORE = 5_000   # X_XX or XX_X pattern

# MỨC ĐỘ ƯU TIÊN CHO CÁC MỐI ĐE DỌA TỪ ĐỐI THỦ
OPPONENT_WEIGHT =  1.15

# THƯỞNG THÊM NẾU KIỂM SOÁT ĐIỂM TRUNG TÂM
CENTER_BONUS = 15

# BÁN KÍNH TÌM KIẾM LÂN CẬN CHO CÁC NƯỚC ĐI TIỀM NĂNG
NEIGHBOR_RADIUS = 3



class HeuristicsMixin:
    #Đánh giá nhanh chiến thuật của một nước đi mà không cần xem xét toàn bộ bàn cờ.
    #Kiểm tra các mối đe dọa tức thời được tạo ra và bị chặn.
    def quick_tactical_score(self, board: Board, row, col):
        board.make_move_simulate(row, col, HUMAN)

        if board.get_winner() == HUMAN:
            board.undo_move_simulate(row, col)
            return WIN_SCORE

        board.undo_move_simulate(row, col)
        score = 0

        board.make_move_simulate(row, col, AI)
        ai_threat = self.count_threat_at(board, row, col, AI)
        board.undo_move_simulate(row, col)
        
        board.make_move_simulate(row, col, HUMAN)
        human_threat = self.count_threat_at(board, row, col, HUMAN)
        board.undo_move_simulate(row, col)

        score = ai_threat + int(human_threat * OPPONENT_WEIGHT)

        return score
        

    # Tính giá trị mối đe dọa nếu đặt lại row, col
    def count_threat_at(self, board: Board, row, col, player):
        total =0
        for dr,dc in DIRECTIONS :
            length, open_ends = self.count_sequence_both_dir(board, row, col, dr, dc, player)
            total += self.score_pattern(length, open_ends)
        return total

    # Đếm độ dài chuỗi theo cả 2 hướng từ 1 vị trí
    def count_sequence_both_dir(
        self,
        board: Board,
        row,
        col,
        dr,
        dc,
        player
    ):
        size = BOARD_SIZE
        length =1
        r = row +dr
        c = col + dc
        # Kiếm tra hướng trước
        while 0<= r < size and 0 <= c < size and board.grid[r][c] == player:
            length +=1
            r += dr
            c += dc
        open_ends = 0
        if 0 <= r < size and 0 <= c < size and board.grid[r][c] == EMPTY:
            open_ends +=1
        # Kiểm tra hướng ngược lại
        prev_r = row -dr
        prev_c = col - dc
        while 0<= prev_r < size and  0 <= prev_c < size and board.grid[prev_r][prev_c] == player :
            length +=1
            prev_r -= dr
            prev_c -=dc
        if 0 <= prev_r < size and 0 <= prev_c < size and board.grid[prev_r][prev_c] == EMPTY:
            open_ends +=1

        return length, open_ends
        
    # Đánh giá trạng thái bàn cờ tổng thể
    def evaluate(self, board: Board):

        ai_score = self.evaluate_player(board, AI)
        human_score = self.evaluate_player(board, HUMAN)
        # Kiểm tra đe dọa kép (2 open 3 , 2 open 4 tạo đe dọa)
        ai_score += self.count_double_threats(board, AI)
        human_score += self.count_double_threats(board, HUMAN)

        return int(ai_score - OPPONENT_WEIGHT * human_score)

    # Đấnh giá trạng thái bàn cờ của 1 người cụ thể
    def evaluate_player( self, board: Board, player):
        total =0
        size = BOARD_SIZE
        evaluate_sequences: Set[Tuple[int, int, int, int, int]] = set()

        for row in range(size):
            for col in range(size):
                if board.grid[row][col] != player:
                    continue
                
                for dr, dc in DIRECTIONS:
                    if self.is_previous_same(board, row, col, dr, dc, player):
                        continue
                    sequence_key = (row, col, dr, dc)
                    if sequence_key in evaluate_sequences:
                        continue
                    evaluate_sequences.add(sequence_key)

                    length, open_ends = self.count_sequence(board, row, col, dr, dc, player)
                    total += self.score_pattern(length, open_ends)

                    broken_score = self.check_broken_pattern(board, row, col, dr, dc, player)
                    total += broken_score
        
        return total
    

    # Kiểm tra các mẫu nguy hiểm (các mẫu bị phá vỡ như X_XXX, ...) tạo thành chuỗi 4 với 1 nước đi
    def check_broken_pattern(
        self,
        board: Board,
        row,
        col,
        dr,
        dc,
        player
    ):

        size = BOARD_SIZE

        line = []

        for i in range(-4, 5):

            r = row + i * dr
            c = col + i * dc

            if 0 <= r < size and 0 <= c < size:
                if board.grid[r][c] == player:
                    line.append("X")
                elif board.grid[r][c] == EMPTY:
                    line.append("_")
                else:
                    line.append("O")
            else:
                line.append("O")

        s = "".join(line)

        score = 0

        if "XXXX_" in s or "_XXXX" in s:
            score += BROKEN_FOUR_SCORE

        if "XXX_X" in s or "X_XXX" in s or "XX_XX" in s:
            score += BROKEN_FOUR_SCORE

        if "XX_X_" in s or "_X_XX" in s:
            score += BROKEN_THREE_SCORE

        return score
    # Đếm số vị trí player có nhiều open 3 , open 4 có sự đe dọa kép mạnh
    def count_double_threats(self, board: Board, player):
        threats: List[Tuple[int, int]] = []
        size = BOARD_SIZE
        for row in range(size):
            for col in range(size):
                if board.grid[row][col] != player:
                    continue
                for dr, dc in DIRECTIONS:
                    if self.is_previous_same(board, row, col, dr, dc, player):
                        continue
                    length, open_ends = self.count_sequence(board, row, col, dr, dc, player)
                    
                    if( length == 3 and open_ends == 2) or( length == 4 and open_ends == 2):
                        threats.append((length, open_ends))
        strong_threats = len([t for t in threats if t[0] >= 3])
        if strong_threats >=2:
            return DOUBLE_THREAT_BONUS * (strong_threats -1)
        return 0
        
    
    # Đếm các đoạn liên tiếp và các đầu hở theo 1 hướng
    def count_sequence(
            self,
            board: Board,
            row,
            col,
            dr,
            dc,
            player
    ):
        size = BOARD_SIZE
        length = 0
        r = row
        c = col
        while 0 <= r < size and 0 <= c < size and board.grid[r][c] == player:
            length +=1
            r += dr
            c += dc

        open_ends = 0
        # Kiểm tra đầu đằng trước (xxx ?)
        if 0 <= r < size and 0 <= c < size and board.grid[r][c] == EMPTY:
            open_ends +=1 

        # Kiểm tra đầu đằng sau ( ?xxx)
        prev_r = row - dr
        prev_c = col -dc
        if 0 <= prev_r < size and 0 <= prev_c < size and board.grid[prev_r][prev_c] == EMPTY:
            open_ends +=1 
        return length, open_ends


    # Kiểm tra ô theo hướng trước có có cùng người chơi không
    def is_previous_same(
            self,
            board: Board,
            row,
            col,
            dr,
            dc,
            player
    ):
        prev_r = row -dr 
        prev_c = col - dc
        return board.in_chess_bound(prev_r,prev_c) and board.grid[prev_r][prev_c] == player
    # Tính điểm cho 1 mẫu dựa trên số quân liên tiếp (xxxo) và các đầu hở
    def score_pattern( self, length, open_ends):
        if( length >= 5):
            return WIN_SCORE
        return PATTERN_SCORES.get((length, open_ends), 0)
