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
    (3, 2): 10_000,
    # Blocked 3 ( CHẶN 1 ĐẦU )
    (3, 1): 1_000,
    
    # Open 2
    (2, 2): 100,
    # Blocked 2
    (2, 1): 10,
    
    # ĐƠN
    (1, 2): 5,
    (1, 1): 1,
}

# Double threat bonus: ĐIỂM THƯỞNG CHO NHIỀU OPEN 3 OPEN 4
DOUBLE_THREAT_BONUS = 200_000


# NGĂN CHẶN CÁC ĐIỂM QUAN TRỌNG (e.g., XX_XX, X_XXX) - KHOẢNG TRỐNG TRONG CHUỖI
BROKEN_FOUR_SCORE = 40_000  # X_XXX or XX_XX pattern
BROKEN_THREE_SCORE = 5_000   # X_XX or XX_X pattern

# MỨC ĐỘ ƯU TIÊN CHO CÁC MỐI ĐE DỌA TỪ ĐỐI THỦ
OPPONENT_WEIGHT = 1.15

# THƯỞNG THÊM NẾU KIỂM SOÁT ĐIỂM TRUNG TÂM
CENTER_BONUS = 15

# BÁN KÍNH TÌM KIẾM LÂN CẬN CHO CÁC NƯỚC ĐI TIỀM NĂNG
NEIGHBOR_RADIUS = 2



class HeuristicsMixin:
    #Đánh giá nhanh chiến thuật của một nước đi mà không cần xem xét toàn bộ bàn cờ.
    #Kiểm tra các mối đe dọa tức thời được tạo ra và bị chặn.
    def quick_tactical_score(self, board: Board, row, col):
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
        r = row -dr
        c = col - dc
        while 0<= r < size and  0 <= c < size and board.grid[r][c] == player :
            length +=1
            r -= dr
            c -=dc
        if 0 <= r < size and 0 <= c < size and board.grid[r][c] == EMPTY:
            open_ends +=1

        return length, open_ends
        
    # Đánh giá trạng thái bàn cờ tổng thể
    def evuluate(self, board: Board):
        ai_score = self.evuluate_player(board, AI)
        human_score = self.evuluate_player(board, HUMAN)

        # Kiểm tra đe dọa kép (2 open 3 , 2 open 4 tạo đe dọa)
        ai_score += self.count_double_threats(board, AI)
        human_score += self.count_double_threats(board, HUMAN)

        return int(ai_score - OPPONENT_WEIGHT * human_score)

    # Đấnh giá trạng thái bàn cờ của 1 người cụ thể
    def evuluate_player( self, board: Board, player):
        total =0
        size = BOARD_SIZE
        evuluate_sequences: Set[Tuple[int, int, int, int, int]] = set()

        for row in range(size):
            for col in range(size):
                if board.grid[row][col] != player:
                    continue
                
                for dr, dc in DIRECTIONS:
                    if self.is_previous_same(board, row, col, dr, dc, player):
                        continue
                    sequence_key = (row, col, dr, dc)
                    if sequence_key in evuluate_sequences:
                        continue
                    evuluate_sequences.add(sequence_key)

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
        first_count = 0
        r = row
        c = col
        while 0 <= r< size and 0 <=c < size and board.grid[r][c] == player:
            first_count  +=1
            r += dr
            c += dc
        if not (0 <= r< size and 0 <=c < size and board.grid[r][c] == EMPTY):
            return  0
        r += dr
        c += dc
        second_count = 0
        while (0 <= r< size and 0 <=c < size and board.grid[r][c] == player):
            second_count +=1
            r += dr
            c += dc
        if second_count == 0:
            return 0
        total_pieces = first_count + second_count

        open_ends =0
        if 0 <= r< size and 0 <=c < size and board.grid[r][c] == EMPTY:
            open_ends +=1

        prev_r = row - dr
        prev_c = col -dc
        if 0 <= r< size and 0 <=c < size and board.grid[r][c] == EMPTY:
            open_ends +=1
        
        if( total_pieces >=4 and open_ends >=1):
            return BROKEN_FOUR_SCORE
        elif total_pieces ==3 and opens_end >=1:
            return BROKEN_THREE_SCORE
        return 0
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
        pre_c = row -dc
        if 0 <= r < size and 0 <= c < size and board.grid[r][c] == EMPTY:
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
