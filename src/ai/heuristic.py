from .types import Score



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

