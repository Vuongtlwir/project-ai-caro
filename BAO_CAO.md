# ĐẠI HỌC BÁCH KHOA HÀ NỘI
## TRƯỜNG CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG

---

# BÁO CÁO BÀI TẬP LỚN
# NHẬP MÔN TRÍ TUỆ NHÂN TẠO

## Đề tài: Bot chơi cờ Caro

**Học kỳ:** 2024.2  
**Giảng viên:** Lê Thanh Hương

---

*Hà Nội, tháng 5 năm 2025*

---

## Mục lục

1. [Giới thiệu và mô tả bài toán](#1-giới-thiệu-và-mô-tả-bài-toán)
2. [Phân công nhiệm vụ](#2-phân-công-nhiệm-vụ)
3. [Cấu trúc dự án](#3-cấu-trúc-dự-án)
4. [Phương pháp giải quyết bài toán](#4-phương-pháp-giải-quyết-bài-toán)
   - 4.1 [Biểu diễn bàn cờ và luật chơi](#41-biểu-diễn-bàn-cờ-và-luật-chơi)
   - 4.2 [Thuật toán Minimax với Alpha-Beta Pruning](#42-thuật-toán-minimax-với-alpha-beta-pruning)
   - 4.3 [Iterative Deepening](#43-iterative-deepening)
   - 4.4 [Hàm đánh giá Heuristic](#44-hàm-đánh-giá-heuristic)
   - 4.5 [Tối ưu tìm kiếm](#45-tối-ưu-tìm-kiếm)
5. [Các chức năng chính](#5-các-chức-năng-chính)
6. [Các vấn đề và giải pháp trong quá trình thực hiện](#6-các-vấn-đề-và-giải-pháp-trong-quá-trình-thực-hiện)
7. [Định hướng trong tương lai](#7-định-hướng-trong-tương-lai)

---

## 1. Giới thiệu và mô tả bài toán

### Nguồn gốc và cách chơi

Cờ caro, hay còn gọi là sọc caro, là một trò chơi dân gian phổ biến. Trong tiếng Triều Tiên, trò chơi này được gọi là *omok*, trong tiếng Nhật là *gomoku narabe*, và trong tiếng Anh gọi là *gomoku*.

Ở Việt Nam, cờ caro thường được chơi trên giấy tập học sinh, sử dụng ký hiệu hình tròn (O) và chữ X để đại diện cho hai loại quân cờ. Người thắng là người tạo được chuỗi liên tục gồm **5 quân cờ** theo hàng ngang, dọc hoặc chéo mà không bị chặn hoặc bị quân đối phương ngắt quãng.

### Mô tả dự án

Dự án tập trung vào việc phát triển một **bot chơi cờ caro thông minh** bằng Python, sử dụng thư viện Pygame cho giao diện đồ họa. Bot được xây dựng với thuật toán **Minimax kết hợp Alpha-Beta Pruning** và nhiều kỹ thuật tối ưu nâng cao.

**Thông số kỹ thuật cơ bản:**

| Thông số | Giá trị |
|---|---|
| Kích thước bàn cờ | 15 × 15 |
| Điều kiện thắng | 5 quân liên tiếp |
| Độ sâu tìm kiếm tối đa (`MAX_DEPTH`) | 4 |
| Giới hạn thời gian mỗi lượt AI (`TIME_LIMIT`) | 2.0 giây |
| Ngôn ngữ lập trình | Python 3.13 |
| Thư viện đồ họa | Pygame |

---

## 2. Phân công nhiệm vụ

### Thành viên 1 — Game + UI

**Phụ trách file:**

| File | Mô tả |
|---|---|
| `src/game/board.py` | Quản lý trạng thái bàn cờ, lịch sử nước đi, undo |
| `src/game/rules.py` | Kiểm tra kết quả trận đấu (thắng / hòa) |
| `src/game/win_checker.py` | Kiểm tra điều kiện 5 quân liên tiếp theo 4 hướng |
| `src/ui/pygame_ui.py` | Toàn bộ giao diện Pygame: menu, bàn cờ, side panel, hiệu ứng |
| `main.py` | Điểm khởi chạy chương trình |

**Nhiệm vụ:**
- Xây dựng logic game: đặt quân, undo, chuyển lượt, phát hiện thắng/hòa
- Vẽ bàn cờ lưới 15×15, quân X/O với hiệu ứng neon
- Xử lý sự kiện chuột (click, hover preview)
- Duy trì game loop 60 FPS và điều phối luồng PvP / PvAI

---

### Thành viên 2 — AI Core

**Phụ trách file:**

| File | Mô tả |
|---|---|
| `src/ai/minimax.py` | Minimax + Alpha-Beta Pruning, xử lý threat tức thời |
| `src/ai/heuristic.py` | Hàm đánh giá bàn cờ theo pattern, broken pattern, double threat |
| `src/ai/move_ordering.py` | Sắp xếp nước đi để Alpha-Beta cắt tỉa hiệu quả |
| `src/ai/iterative_deepening.py` | Tìm kiếm lặp sâu dần (IDDFS) với giới hạn thời gian |

**Nhiệm vụ:**
- Cài đặt thuật toán Minimax với Alpha-Beta Pruning
- Xây dựng hàm heuristic đánh giá pattern (open 4, open 3, broken 4, ...)
- Cài đặt Move Ordering để tối ưu thứ tự duyệt nước đi
- Cài đặt Iterative Deepening để tận dụng giới hạn thời gian `TIME_LIMIT`
- Tích hợp phát hiện threat tức thời (win, block, attack)

---

### Thành viên 3 — Optimization + Docs

**Phụ trách file:**

| File | Mô tả |
|---|---|
| `src/ai/killer_heuristic.py` | Kỹ thuật Killer Move — ghi nhớ nước cắt tỉa hiệu quả |
| `src/utils/timer.py` | Lớp `Timer` quản lý giới hạn thời gian cho AI search |
| `src/utils/helpers.py` | Hàm tiện ích dùng chung: `in_bounds`, `pixel_to_cell`, `opponent_of`, ... |
| `docs/` | Tài liệu nội bộ |
| `README.md` | Hướng dẫn cài đặt và chạy dự án |

**Nhiệm vụ:**
- Cài đặt Killer Heuristic giảm branching factor cho Alpha-Beta
- Xây dựng `Timer` class theo đúng quy ước `main.md` (snake_case, comments)
- Xây dựng `helpers.py` cung cấp các tiện ích dùng chung cho cả game lẫn AI
- Test, debug và benchmark hiệu năng AI
- Viết tài liệu, README và báo cáo

---

### Quy ước chung (Thống nhất khi làm)

| Hạng mục | Quy ước |
|---|---|
| **Cấu trúc thư mục** | `src/ai/`, `src/game/`, `src/ui/`, `src/utils/`, `docs/` |
| **Format bàn cờ** | `board[row][col]` |
| **Format nước đi** | `(row, col)` |
| **Đặt tên hàm** | snake_case — `get_best_move()`, không dùng `GetBestMove()` |
| **Comment** | Ghi chú các phần quan trọng bằng tiếng Việt |
| **API Board** | `make_move()`, `undo_move()`, `is_valid_move()`, `check_win()`, `switch_player()` |
| **API AI** | `get_best_move(board, player)`, `evaluate_board(board, player)`, `minimax(...)` |
| **Luật game** | Thắng 5 quân, không có overline, không có double-three |
| **Search settings** | `MAX_DEPTH = 4`, `TIME_LIMIT = 2.0` (giây) |
| **Move generation** | Chỉ xét ô lân cận (`NEIGHBOR_RADIUS = 3`), có move ordering |
| **Undo move** | Restore đúng board, restore lượt chơi, restore cache/state |
| **Git workflow** | Branch riêng cho từng thành viên, merge rule, commit format rõ ràng |

---

## 3. Cấu trúc dự án

```
project-ai-caro/
├── main.py                      # Điểm khởi chạy chương trình
├── main.md                      # Quy ước chung của nhóm
├── src/
│   ├── game/
│   │   ├── board.py             # Quản lý trạng thái bàn cờ
│   │   ├── constants.py         # Hằng số toàn cục (BOARD_SIZE, MAX_DEPTH, TIME_LIMIT, ...)
│   │   ├── rules.py             # Luật chơi (kiểm tra thắng, hòa)
│   │   └── win_checker.py       # Kiểm tra điều kiện thắng 5 quân
│   ├── ai/
│   │   ├── minimax.py           # Thuật toán Minimax + Alpha-Beta, xử lý threat
│   │   ├── heuristic.py         # Hàm đánh giá bàn cờ theo pattern
│   │   ├── iterative_deepening.py # Tìm kiếm lặp sâu dần (IDDFS)
│   │   ├── killer_heuristic.py  # Kỹ thuật Killer Move
│   │   ├── move_ordering.py     # Sắp xếp nước đi cho Alpha-Beta
│   │   └── types.py             # Định nghĩa kiểu dữ liệu
│   ├── ui/
│   │   └── pygame_ui.py         # Giao diện Pygame (menu, bàn cờ, panel)
│   └── utils/
│       ├── timer.py             # Lớp Timer quản lý giới hạn thời gian AI
│       └── helpers.py           # Hàm tiện ích (in_bounds, pixel_to_cell, ...)
```

---

## 4. Phương pháp giải quyết bài toán

### 4.1 Biểu diễn bàn cờ và luật chơi

**Định dạng bàn cờ:** `board[row][col]`

```python
EMPTY = 0
HUMAN = 1
AI    = -1
```

Bàn cờ là ma trận `15×15` số nguyên. Ô trống có giá trị `0`, quân người chơi là `1`, quân AI là `-1`.

**API Board (`src/game/board.py`):**

```python
make_move(row, col)          # Thực hiện nước đi, chuyển lượt
undo_move()                  # Hoàn tác nước đi gần nhất
is_valid_move(row, col)      # Kiểm tra nước đi hợp lệ
available_neighbors()        # Trả về các ô trống kề quân đã có
get_winner()                 # Trả về người thắng sau nước vừa đi
switch_player()              # Đổi lượt chơi
reset()                      # Xóa bàn cờ, bắt đầu lại
make_move_simulate(row, col, player)  # Giả lập nước đi (cho Minimax)
undo_move_simulate(row, col)          # Hoàn tác nước giả lập
```

**Kiểm tra thắng (`src/game/win_checker.py`):**

Hàm `check_win(board, row, col)` duyệt 4 hướng (ngang, dọc, chéo xuôi, chéo ngược) từ ô vừa đánh, đếm tổng số quân liên tiếp cùng màu. Nếu tổng ≥ `WIN_LENGTH = 5` thì người đó thắng.

```python
DIRECTIONS = [
    (0, 1),   # ngang
    (1, 0),   # dọc
    (1, 1),   # chéo xuôi
    (1, -1),  # chéo ngược
]
```

---

### 4.2 Thuật toán Minimax với Alpha-Beta Pruning

**Input:** Trạng thái bàn cờ `board`, độ sâu `depth`, cửa sổ `[alpha, beta]`, cờ `maximizing`  
**Output:** Điểm đánh giá `int`

Lớp `Minimax` kế thừa nhiều mixin: `HeuristicsMixin`, `KillerHeuristic`, `MoveOrdering`, `IterativeDeepening`.

#### a. Phương thức `search_root` — xử lý ưu tiên tại gốc

```python
def search_root(self, board, depth):
    # 1. AI THẮNG NGAY → trả về ngay không cần Minimax
    for move in moves:
        board.make_move_simulate(row, col, AI)
        if board.get_winner() == AI:
            return move, WIN_SCORE

    # 2. CHẶN HUMAN THẮNG NGAY
    for move in moves:
        board.make_move_simulate(row, col, HUMAN)
        if board.get_winner() == HUMAN:
            return move, WIN_SCORE * 100 - 1

    # 3. TẤN CÔNG: tìm nước tạo threat mạnh cho AI
    attack_move = self.find_dangerous_threat_move(board, AI)

    # 4. PHÒNG THỦ: chặn threat nguy hiểm nhất của Human
    block_move = self.find_immediate_threat_block(board)
    if block_move is not None:
        return block_move, WIN_SCORE * 50 - 1

    # 5. TÌM KIẾM CHIẾN THUẬT NHANH (open 3, broken 3)
    best_tactical, tactical_score = self.find_best_tactical_move(board, AI)
    if tactical_score >= 200_000:
        return best_tactical, tactical_score

    # 6. MINIMAX đầy đủ với Alpha-Beta
    for move in moves:
        score = self.minimax(board, depth-1, alpha, beta, False)
        ...
```

#### b. Phương thức `minimax` — đệ quy Alpha-Beta

```python
def minimax(self, board, depth, alpha, beta, maximizing):
    # Điều kiện dừng
    if self.is_time_up():     return self.evaluate(board)
    if winner == AI:          return WIN_SCORE + depth
    if winner == HUMAN:       return -WIN_SCORE - depth
    if depth == 0:            return self.evaluate(board)

    # Maximizing (AI)
    if maximizing:
        value = -inf
        for row, col in moves:
            board.make_move_simulate(row, col, AI)
            value = max(value, self.minimax(..., False))
            board.undo_move_simulate(row, col)
            alpha = max(alpha, value)
            if beta <= alpha:                   # Alpha-Beta cut
                self.store_killer(depth, move)  # lưu Killer Move
                break
        return value

    # Minimizing (Human)
    else:
        value = +inf
        for row, col in moves:
            board.make_move_simulate(row, col, HUMAN)
            value = min(value, self.minimax(..., True))
            ...
            beta = min(beta, value)
            if beta <= alpha: break
        return value
```

Đặc điểm nổi bật:
- Nước thắng ở độ sâu lớn hơn được ưu tiên hơn (`WIN_SCORE + depth`)
- Tích hợp **Killer Move** tại mỗi điểm cắt tỉa

---

### 4.3 Iterative Deepening

**API AI (`src/ai/iterative_deepening.py`):**

```python
def choose_move(board):   # get_best_move tương đương
def search_root(board, depth)
def minimax(board, depth, alpha, beta, maximizing)
```

Thay vì tìm kiếm thẳng đến `MAX_DEPTH = 4`, thuật toán tăng dần từ depth 1 → 2 → 3 → 4:

```python
def choose_move(self, board):
    self.start_time = time.perf_counter()
    best_move = legal_moves[0]

    for depth in range(1, self.max_depth + 1):
        if self.is_time_up():
            break
        move, score = self.search_root(board, depth)
        if move is not None and not self.is_time_up():
            best_move = move
            if score >= WIN_SCORE - 1000:   # tìm thấy nước thắng → dừng
                break

    return best_move
```

**Ưu điểm của Iterative Deepening:**
- Luôn có kết quả ở depth cạn hơn làm "nước dự phòng" nếu hết giờ
- Sử dụng kết quả của depth trước để sắp xếp nước đi cho depth sau (move ordering)
- Tương thích tự nhiên với giới hạn thời gian `TIME_LIMIT = 2.0` giây

---

### 4.4 Hàm đánh giá Heuristic

**`evaluate_board(board, player)` — tương đương với tên trong báo cáo:**

```python
def evaluate(self, board):
    ai_score    = self.evaluate_player(board, AI)
    human_score = self.evaluate_player(board, HUMAN)
    ai_score    += self.count_double_threats(board, AI)
    human_score += self.count_double_threats(board, HUMAN)
    return int(ai_score - OPPONENT_WEIGHT * human_score)
```

Trong đó `OPPONENT_WEIGHT = 1.15` — đặt trọng số phòng thủ cao hơn một chút để AI ưu tiên chặn đòn nguy hiểm.

#### Bảng điểm theo pattern (`PATTERN_SCORES`)

| Pattern | Mô tả | Điểm |
|---|---|---|
| 5 quân liên tiếp | Thắng ngay | 10,000,000 |
| Open 4 (2 đầu mở) | Không thể chặn | 500,000 |
| Broken 4 (`XX_XX`, `X_XXX`) | Ăn sau 1 nước | 100,000 |
| Blocked 4 (1 đầu mở) | Cần chặn | 50,000 |
| Open 3 (2 đầu mở) | Nguy hiểm | 18,000 |
| Broken 3 (`XX_X_`, `_X_XX`) | Tiềm năng | 5,000 |
| Blocked 3 (1 đầu mở) | Thấp | 1,500 |
| Open 2 | Phát triển | 100 |

#### Phát hiện đe dọa kép (`count_double_threats`)

Nếu một người chơi có từ 2 open-3 hoặc open-4 trở lên cùng lúc (double threat — không thể chặn cả hai), thưởng thêm:

```
Điểm thưởng = DOUBLE_THREAT_BONUS × (số threat mạnh − 1)
            = 100,000 × (n − 1)
```

#### Pattern bị phá vỡ (`check_broken_pattern`)

Hàm trích xuất một "dòng" 9 ký tự xung quanh vị trí (`X` = quân mình, `_` = trống, `O` = đối thủ/biên), sau đó khớp chuỗi:

```python
if "XXX_X" in s or "X_XXX" in s or "XX_XX" in s:
    score += BROKEN_FOUR_SCORE   # 100,000

if "XX_X_" in s or "_X_XX" in s:
    score += BROKEN_THREE_SCORE  # 5,000
```

#### Bonus kiểm soát trung tâm

```python
CENTER_BONUS = 15
# Điểm cộng thêm tỷ lệ nghịch với khoảng cách Manhattan tới trung tâm
score += CENTER_BONUS * (BOARD_SIZE * 2 - distance_to_center)
```

---

### 4.5 Tối ưu tìm kiếm

#### a. Move Generation — chỉ xét ô lân cận

Thay vì duyệt toàn bộ 225 ô, chỉ xét các ô trống trong bán kính `NEIGHBOR_RADIUS = 3` xung quanh các quân đã đi (`get_candidate_moves`). Điều này giảm không gian tìm kiếm đáng kể.

#### b. Move Ordering — sắp xếp nước đi

```python
def score_move(move):
    score = 0
    score += self.move_scores[move] * 0.01   # lịch sử từ depth trước
    if move in killer:
        score += 100_000                      # Killer Move ưu tiên cao
    score += self.quick_tactical_score(...)  # đánh giá chiến thuật nhanh
    score += CENTER_BONUS * (...)            # ưu tiên trung tâm
    return score

moves.sort(key=score_move, reverse=True)
```

Nước đi tốt được thử trước → Alpha-Beta cắt tỉa nhiều hơn → duyệt ít node hơn.

#### c. Killer Heuristic

Khi một nước đi gây ra cắt tỉa Alpha-Beta (beta ≤ alpha), nước đó được lưu lại như **Killer Move** cho độ sâu hiện tại (tối đa 2 killer mỗi depth):

```python
def store_killer(self, depth, move):
    killer = self.killer_moves[depth]
    killer.insert(0, move)          # chèn đầu danh sách
    if len(killer) > self.max_killers_per_depth:
        killer.pop()
```

#### d. Phát hiện Threat tức thời

Trước khi chạy Minimax đầy đủ, `search_root` kiểm tra nhanh:

| Ưu tiên | Điều kiện | Hành động |
|---|---|---|
| 1 | AI thắng ngay | Đánh ngay, trả về `WIN_SCORE` |
| 2 | Human thắng ngay | Chặn ngay |
| 3 | Human có threat nguy hiểm (open 4 / broken 4 / open 3) | Chặn bằng `find_immediate_threat_block` |
| 4 | AI tạo được attack score > 300,000 | Tấn công |
| 5 | Có nước chiến thuật score ≥ 200,000 | Đánh nhanh |
| 6 | Minimax đầy đủ với IDDFS | Tìm kiếm sâu |

#### e. Quản lý thời gian (`src/utils/timer.py`)

```python
class Timer:
    def start(self)          # Bắt đầu đếm giờ
    def is_up(self)          # Đã hết time_limit_sec chưa?
    def elapsed(self)        # Thời gian đã dùng (giây)
    def remaining(self)      # Thời gian còn lại (giây)
```

Hàm `is_time_up()` trong Minimax gọi kiểm tra này tại mỗi node để dừng đúng lúc.

---

## 5. Các chức năng chính

### Giao diện tổng quan

Trò chơi được xây dựng bằng **Pygame**, chạy ở 60 FPS. Cửa sổ gồm:
- **Bàn cờ** (640 × 640 pixel, lưới 15×15)
- **Side panel** bên phải: hiển thị trạng thái, lượt chơi, số nước, nút Restart / Menu

### Chế độ 1: Người với Người (PvP)

Hai người chơi lần lượt click vào ô trống trên bàn cờ. Quân X (hồng) luôn đi trước.

**Luồng xử lý một nước đi:**
```
Click chuột
  → handle_click(pos)
    → pixel_to_cell(x, y, offset_x, offset_y)   # chuyển pixel → (row, col)
    → board.is_valid_move(row, col)              # kiểm tra hợp lệ
    → board.make_move(row, col)                  # ghi xuống bàn cờ
    → get_game_result(board.grid, row, col)      # kiểm tra thắng/hòa
    → board.switch_player()                      # đổi lượt
```

### Chế độ 2: Người với AI (PvAI)

Người chơi dùng quân X, AI dùng quân O (xanh lá). Sau mỗi nước của người, AI sẽ suy nghĩ và đánh lại.

**Luồng xử lý lượt AI (có delay 350ms để tạo cảm giác tự nhiên):**

```
Người đánh xong → board.switch_player() → ai_thinking = True
  → update_ai() (mỗi frame, tick 60 FPS)
    → nếu đã đợi đủ 350ms:
      → ai_move()
        → ai.choose_move(board)     # IDDFS + Minimax
        → board.make_move(row, col)
        → get_game_result(...)
        → board.switch_player()
```

### Hover preview

Khi di chuột qua ô trống (trong lượt của người chơi), hiển thị quân bán trong suốt để xem trước.

### Hiệu ứng khi thắng

Khi game kết thúc, hàm `find_winning_cells(player)` tìm ra 5 ô liên tiếp thắng, sau đó vẽ một đường sáng (glow effect) nối từ ô đầu đến ô cuối qua `draw_winning_line()`.

### Nút điều khiển

| Nút | Chức năng |
|---|---|
| **RESTART** | Reset bàn cờ, giữ nguyên chế độ chơi |
| **MENU** | Quay về màn hình chọn chế độ |

---

## 6. Các vấn đề và giải pháp trong quá trình thực hiện

| Vấn đề | Giải pháp |
|---|---|
| AI duyệt quá nhiều node, chạy chậm | Giới hạn ô xét bằng `NEIGHBOR_RADIUS`, thêm giới hạn `TIME_LIMIT = 2.0s` |
| AI không chặn được đòn đánh phối hợp (open 3 + open 3) | Thêm `count_double_threats()` trong heuristic để phát hiện và xử lý double threat |
| AI bỏ lỡ nước thắng hoặc nước chặn tức thời | Thêm ưu tiên bậc cao tại `search_root`: kiểm tra win/block ngay trước khi gọi Minimax |
| AI phản ứng chậm ở đầu ván (bàn cờ trống) | Trả về ô trung tâm ngay lập tức nếu bàn cờ chưa có quân |
| Heuristic không đánh giá được pattern bị phá vỡ (X_XXX) | Thêm `check_broken_pattern()` phát hiện các mẫu broken-4 và broken-3 nguy hiểm |
| Move ordering không hiệu quả ở depth cao | Kết hợp ba tiêu chí: lịch sử điểm, Killer Move, và `quick_tactical_score()` |
| Code phân tán, thiếu quy ước | Lập `main.md` thống nhất quy ước đặt tên snake_case, format move `(row, col)`, API chuẩn |

---

## 7. Định hướng trong tương lai

- **Thêm mức độ khó:** Bổ sung chế độ Easy (heuristic đơn giản, độ sâu 1–2) và Medium (Minimax depth 3, không có broken pattern detection) để phù hợp với người chơi mới.

- **Chế độ AI vs AI:** Cho phép hai cấu hình AI đấu nhau tự động, dùng để so sánh hiệu suất và kiểm thử.

- **Tối ưu heuristic thêm:** Nghiên cứu thêm các pattern nguy hiểm trong Gomoku chuyên nghiệp (VCF — Victory by Continuous Four, VCT — Victory by Continuous Threat).

- **Transposition Table (Bảng chuyển vị):** Cache kết quả Minimax theo hash của trạng thái bàn cờ, tránh tính lại các trạng thái đã gặp.

- **Ứng dụng học máy:** Huấn luyện mô hình đánh giá thay thế heuristic thủ công bằng dữ liệu từ các ván đấu thực tế.

- **Cải thiện giao diện:** Thêm hiệu ứng âm thanh, animation đặt quân, thống kê trận đấu (số node duyệt, thời gian AI, điểm heuristic).

- **Hỗ trợ undo nhiều lượt:** Hiện tại Board có `undo_move()`, nhưng giao diện chưa có nút Undo cho người chơi sử dụng.

---

*Báo cáo được tạo tự động từ codebase dự án `project-ai-caro`.*
