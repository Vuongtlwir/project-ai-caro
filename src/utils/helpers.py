from src.game.constants import BOARD_SIZE, CELL_SIZE


# ----------------------------------------
# Bàn cờ
# ----------------------------------------

def in_bounds(row: int, col: int, size: int = BOARD_SIZE) -> bool:
    """Kiểm tra (row, col) có nằm trong bàn cờ không."""
    return 0 <= row < size and 0 <= col < size


def board_center() -> int:
    """Trả về chỉ số hàng/cột trung tâm của bàn cờ."""
    return BOARD_SIZE // 2


def opponent_of(player: int) -> int:
    """Trả về người chơi đối lập: HUMAN ↔ AI."""
    return player * -1


# ----------------------------------------
# Tọa độ UI (pixel  ô lưới)
# ----------------------------------------

def pixel_to_cell(
    x: int,
    y: int,
    offset_x: int,
    offset_y: int,
    cell_size: int = CELL_SIZE,
) -> tuple[int, int]:
    """Chuyển tọa độ pixel → (row, col) trên lưới."""
    col = (x - offset_x) // cell_size
    row = (y - offset_y) // cell_size
    return row, col


def cell_to_pixel_center(
    row: int,
    col: int,
    offset_x: int,
    offset_y: int,
    cell_size: int = CELL_SIZE,
) -> tuple[int, int]:
    """Trả về tọa độ pixel tâm của ô (row, col)."""
    x = offset_x + col * cell_size + cell_size // 2
    y = offset_y + row * cell_size + cell_size // 2
    return x, y


# ----------------------------------------
# Khoảng cách
# ----------------------------------------

def manhattan_distance(r1: int, c1: int, r2: int, c2: int) -> int:
    """Khoảng cách Manhattan giữa hai ô trên bàn cờ."""
    return abs(r1 - r2) + abs(c1 - c2)
