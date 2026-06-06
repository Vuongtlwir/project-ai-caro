import pygame
import math

from src.ai.minimax import Minimax
from src.ai.easy_ai import EasyAI
from src.game.board import Board
from src.game.constants import *
from src.game.rules import get_game_result


SIDE_PANEL = 300

WIDTH = BOARD_SIZE * CELL_SIZE + SIDE_PANEL
HEIGHT = BOARD_SIZE * CELL_SIZE + 80


class CaroGameUI:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro Neon")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 22)

        self.big_font = pygame.font.SysFont(
            "consolas",
            36,
            bold=True
        )

        self.win_font = pygame.font.SysFont(
            "consolas",
            54,
            bold=True
        )

        self.board = Board()

        self.board_pixel_size = BOARD_SIZE * CELL_SIZE + 1
        self.ai = Minimax(max_depth=4, time_limit_sec=2.0)

        self.offset_x = 40
        self.offset_y = 40

        self.running = True
        self.in_menu = True
        self.game_over = False
        self.winner = None

        self.ai_enabled = False

        self.ai_thinking = False
        self.ai_think_start = 0
        self.ai_think_delay = 350

        self.winning_cells = []

        self.move_count = 0

        # MENU
        self.pvp_button = pygame.Rect(
            WIDTH // 2 - 160,
            240,
            320,
            55
        )

        self.pvai_easy_button = pygame.Rect(
            WIDTH // 2 - 160,
            310,
            320,
            55
        )

        self.pvai_hard_button = pygame.Rect(
            WIDTH // 2 - 160,
            380,
            320,
            55
        )

        # SIDE PANEL BUTTONS
        self.restart_button = pygame.Rect(0, 0, 0, 0)
        self.menu_button = pygame.Rect(0, 0, 0, 0)

        # CONFIRM DIALOG
        self.confirm_action = None  # None | "restart" | "menu"
        self.confirm_yes_button = pygame.Rect(0, 0, 0, 0)
        self.confirm_no_button = pygame.Rect(0, 0, 0, 0)

        # WIN POPUP (thông báo khi kết thúc ván)
        self.show_win_popup = False

    #  BACKGROUND 

    def draw_background(self):

        for i in range(HEIGHT):

            color = (
                12 + i // 25,
                12 + i // 30,
                22 + i // 20
            )

            pygame.draw.line(
                self.screen,
                color,
                (0, i),
                (WIDTH, i)
            )

    #  BUTTON 

    def draw_button(self, rect, text, color):

        pygame.draw.rect(
            self.screen,
            (18, 18, 28),
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            color,
            rect,
            2,
            border_radius=10
        )

        txt = self.font.render(text, True, color)

        self.screen.blit(
            txt,
            (
                rect.centerx - txt.get_width() // 2,
                rect.centery - txt.get_height() // 2
            )
        )

    #  MENU 

    def draw_menu(self):

        self.draw_background()

        title = self.big_font.render(
            "CARO NEON",
            True,
            (0, 255, 200)
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                120
            )
        )

        self.draw_button(
            self.pvp_button,
            "PVP MODE",
            (0, 200, 255)
        )

        self.draw_button(
            self.pvai_easy_button,
            "PLAY AI - EASY",
            (0, 255, 140)
        )

        self.draw_button(
            self.pvai_hard_button,
            "PLAY AI - HARD",
            (255, 80, 120)
        )

    def handle_menu_click(self, pos):

        if self.pvp_button.collidepoint(pos):

            self.ai_enabled = False
            self.in_menu = False

        elif self.pvai_easy_button.collidepoint(pos):

            self.ai_enabled = True
            self.ai = EasyAI(mistake_chance=0.25)
            self.in_menu = False

        elif self.pvai_hard_button.collidepoint(pos):

            self.ai_enabled = True
            self.ai = Minimax(max_depth=4, time_limit_sec=2.0)
            self.in_menu = False

    #  GRID 

    def draw_grid(self):

        x0 = self.offset_x
        y0 = self.offset_y
        size = self.board_pixel_size

        pygame.draw.rect(
            self.screen,
            (20, 20, 30),
            (
                x0 - 10,
                y0 - 10,
                size + 20,
                size + 20
            ),
            border_radius=15
        )

        for i in range(BOARD_SIZE + 1):

            x = x0 + i * CELL_SIZE

            pygame.draw.line(
                self.screen,
                (70, 70, 90),
                (x, y0),
                (x, y0 + size),
                1
            )

        for i in range(BOARD_SIZE + 1):

            y = y0 + i * CELL_SIZE

            pygame.draw.line(
                self.screen,
                (70, 70, 90),
                (x0, y),
                (x0 + size, y),
                1
            )

        pygame.draw.rect(
            self.screen,
            (0, 255, 200),
            (x0, y0, size, size),
            2
        )

    # ================= LAST MOVE GLOW =================

    def draw_last_move_glow(self):

        if self.board.last_move is None:
            return

        r, c = self.board.last_move

        x = self.offset_x + c * CELL_SIZE
        y = self.offset_y + r * CELL_SIZE

        piece = self.board.grid[r][c]

        if piece == HUMAN:

            color = (255, 80, 120)

        else:

            color = (0, 255, 200)

        # pulse animation
        pulse = (
            math.sin(pygame.time.get_ticks() * 0.008) + 1
        ) / 2

        alpha = 35 + int(pulse * 25)

        # glow mềm
        glow_surface = pygame.Surface(
            (CELL_SIZE, CELL_SIZE),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (*color, alpha),
            (
                2,
                2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            ),
            border_radius=10
        )

        self.screen.blit(glow_surface, (x, y))

        # viền ngoài mờ
        pygame.draw.rect(
            self.screen,
            (*color, 120),
            (
                x + 1,
                y + 1,
                CELL_SIZE - 2,
                CELL_SIZE - 2
            ),
            width=2,
            border_radius=10
        )

        # viền sáng trong
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                x + 4,
                y + 4,
                CELL_SIZE - 8,
                CELL_SIZE - 8
            ),
            width=1,
            border_radius=8
        )


    # ================= WINNING =================

    def find_winning_cells(self, player):

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):

                if self.board.grid[r][c] != player:
                    continue

                for dr, dc in DIRECTIONS:

                    cells = []

                    for k in range(WIN_LENGTH):

                        nr = r + dr * k
                        nc = c + dc * k

                        if not (
                            0 <= nr < BOARD_SIZE and
                            0 <= nc < BOARD_SIZE
                        ):
                            break

                        if self.board.grid[nr][nc] != player:
                            break

                        cells.append((nr, nc))

                    if len(cells) == WIN_LENGTH:
                        return cells

        return []

    def draw_winning_line(self):

        if len(self.winning_cells) < 2:
            return

        start_r, start_c = self.winning_cells[0]
        end_r, end_c = self.winning_cells[-1]

        start_x = (
            self.offset_x +
            start_c * CELL_SIZE +
            CELL_SIZE // 2
        )

        start_y = (
            self.offset_y +
            start_r * CELL_SIZE +
            CELL_SIZE // 2
        )

        end_x = (
            self.offset_x +
            end_c * CELL_SIZE +
            CELL_SIZE // 2
        )

        end_y = (
            self.offset_y +
            end_r * CELL_SIZE +
            CELL_SIZE // 2
        )

        dx = end_x - start_x
        dy = end_y - start_y

        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return

        ux = dx / length
        uy = dy / length

        extend = CELL_SIZE * 0.22

        start_x -= ux * extend
        start_y -= uy * extend

        end_x += ux * extend
        end_y += uy * extend

        glow_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pygame.draw.line(
            glow_surface,
            (255, 215, 0, 55),
            (start_x, start_y),
            (end_x, end_y),
            18
        )

        self.screen.blit(glow_surface, (0, 0))

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (start_x, start_y),
            (end_x, end_y),
            8
        )

        pygame.draw.line(
            self.screen,
            (255, 215, 0),
            (start_x, start_y),
            (end_x, end_y),
            4
        )

    #  PIECES 

    def draw_pieces(self):

        pad = 10

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):

                v = self.board.grid[r][c]

                x = self.offset_x + c * CELL_SIZE
                y = self.offset_y + r * CELL_SIZE

                cx = x + CELL_SIZE // 2
                cy = y + CELL_SIZE // 2

                if v == HUMAN:

                    pygame.draw.line(
                        self.screen,
                        (255, 80, 120),
                        (x + pad, y + pad),
                        (
                            x + CELL_SIZE - pad,
                            y + CELL_SIZE - pad
                        ),
                        4
                    )

                    pygame.draw.line(
                        self.screen,
                        (255, 80, 120),
                        (
                            x + CELL_SIZE - pad,
                            y + pad
                        ),
                        (
                            x + pad,
                            y + CELL_SIZE - pad
                        ),
                        4
                    )

                elif v == AI:

                    pygame.draw.circle(
                        self.screen,
                        (0, 255, 200),
                        (cx, cy),
                        CELL_SIZE // 2 - pad,
                        4
                    )

    #  HOVER 

    def draw_hover_piece(self):

        if self.game_over:
            return

        if self.ai_enabled and self.board.current_player == AI:
            return

        mx, my = pygame.mouse.get_pos()

        if not (
            self.offset_x <= mx < self.offset_x + self.board_pixel_size and
            self.offset_y <= my < self.offset_y + self.board_pixel_size
        ):
            return

        c = (mx - self.offset_x) // CELL_SIZE
        r = (my - self.offset_y) // CELL_SIZE

        if not (
            self.board.in_chess_bound(r, c)
            and self.board.is_empty(r, c)
        ):
            return

        x = self.offset_x + c * CELL_SIZE
        y = self.offset_y + r * CELL_SIZE

        preview = pygame.Surface(
            (CELL_SIZE, CELL_SIZE),
            pygame.SRCALPHA
        )

        pad = 10

        if self.board.current_player == HUMAN:

            pygame.draw.line(
                preview,
                (255, 80, 120, 120),
                (pad, pad),
                (
                    CELL_SIZE - pad,
                    CELL_SIZE - pad
                ),
                4
            )

            pygame.draw.line(
                preview,
                (255, 80, 120, 120),
                (
                    CELL_SIZE - pad,
                    pad
                ),
                (
                    pad,
                    CELL_SIZE - pad
                ),
                4
            )

        else:

            pygame.draw.circle(
                preview,
                (0, 255, 200, 120),
                (
                    CELL_SIZE // 2,
                    CELL_SIZE // 2
                ),
                CELL_SIZE // 2 - pad,
                4
            )

        self.screen.blit(preview, (x, y))

    #  SIDE PANEL 

    def draw_side_panel(self):

        panel_x = self.offset_x + self.board_pixel_size + 30

        panel = pygame.Rect(
            panel_x,
            self.offset_y,
            220,
            self.board_pixel_size
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 30),
            panel,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            (0, 255, 200),
            panel,
            2,
            border_radius=15
        )

        title = self.font.render(
            "STATUS",
            True,
            (0, 255, 200)
        )

        self.screen.blit(
            title,
            (
                panel.centerx - title.get_width() // 2,
                self.offset_y + 20
            )
        )

        pygame.draw.line(
            self.screen,
            (60, 60, 80),
            (panel_x + 20, self.offset_y + 55),
            (panel_x + 200, self.offset_y + 55),
            1
        )

        if self.game_over:

            if self.ai_enabled:

                text = (
                    "YOU WIN"
                    if self.winner == HUMAN
                    else "AI WIN"
                )

            else:

                text = (
                    "X WIN"
                    if self.winner == HUMAN
                    else "O WIN"
                )

            color = (
                (255, 80, 120)
                if self.winner == HUMAN
                else (0, 255, 200)
            )

            win_text = self.win_font.render(
                text,
                True,
                color
            )

            self.screen.blit(
                win_text,
                (
                    panel.centerx - win_text.get_width() // 2,
                    self.offset_y + 170
                )
            )

        else:

            if self.ai_enabled:

                if self.ai_thinking:

                    text = "AI TURN"
                    color = (255, 200, 0)

                else:

                    text = (
                        "YOUR TURN"
                        if self.board.current_player == HUMAN
                        else "AI TURN"
                    )

                    color = (255, 255, 255)

            else:

                text = (
                    "X TURN"
                    if self.board.current_player == HUMAN
                    else "O TURN"
                )

                color = (255, 255, 255)

            status = self.big_font.render(
                text,
                True,
                color
            )

            self.screen.blit(
                status,
                (
                    panel.centerx - status.get_width() // 2,
                    self.offset_y + 170
                )
            )

        pygame.draw.line(
            self.screen,
            (60, 60, 80),
            (panel_x + 20, self.offset_y + 320),
            (panel_x + 200, self.offset_y + 320),
            1
        )

        mode_text = (
            "MODE : AI"
            if self.ai_enabled
            else "MODE : PVP"
        )

        moves_text = f"MOVES : {self.move_count}"

        mode_render = self.font.render(
            mode_text,
            True,
            (180, 180, 180)
        )

        moves_render = self.font.render(
            moves_text,
            True,
            (180, 180, 180)
        )

        self.screen.blit(
            mode_render,
            (panel_x + 20, self.offset_y + 340)
        )

        self.screen.blit(
            moves_render,
            (panel_x + 20, self.offset_y + 375)
        )

        # RESTART / MENU luôn hiển thị
        self.restart_button = pygame.Rect(
            panel.centerx - 70,
            self.offset_y + 430,
            140,
            45
        )

        self.menu_button = pygame.Rect(
            panel.centerx - 70,
            self.offset_y + 490,
            140,
            45
        )

        self.draw_button(
            self.restart_button,
            "RESTART",
            (0, 255, 200)
        )

        self.draw_button(
            self.menu_button,
            "MENU",
            (255, 80, 120)
        )

    #  CONFIRM DIALOG 

    def draw_confirm_dialog(self):

        if self.confirm_action is None:
            return

        # lớp phủ mờ
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # hộp thoại
        box_w, box_h = 420, 200
        box = pygame.Rect(
            WIDTH // 2 - box_w // 2,
            HEIGHT // 2 - box_h // 2,
            box_w,
            box_h
        )

        pygame.draw.rect(
            self.screen,
            (18, 18, 28),
            box,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            (0, 255, 200),
            box,
            2,
            border_radius=15
        )

        if self.confirm_action == "restart":
            msg = "RESTART GAME?"
        else:
            msg = "BACK TO MENU?"

        msg_render = self.big_font.render(msg, True, (255, 255, 255))
        self.screen.blit(
            msg_render,
            (
                box.centerx - msg_render.get_width() // 2,
                box.y + 35
            )
        )

        self.confirm_yes_button = pygame.Rect(
            box.centerx - 150,
            box.y + 120,
            130,
            45
        )

        self.confirm_no_button = pygame.Rect(
            box.centerx + 20,
            box.y + 120,
            130,
            45
        )

        self.draw_button(
            self.confirm_yes_button,
            "YES",
            (0, 255, 140)
        )

        self.draw_button(
            self.confirm_no_button,
            "NO",
            (255, 80, 120)
        )

    #  WIN POPUP

    def draw_win_popup(self):

        if not self.show_win_popup:
            return

        # lớp phủ mờ toàn màn hình
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))

        # nội dung & màu theo kết quả
        if self.winner == DRAW:
            msg = "DRAW!"
            color = (255, 215, 0)
        elif self.ai_enabled:
            if self.winner == HUMAN:
                msg = "YOU WIN!"
                color = (255, 80, 120)
            else:
                msg = "AI WINS!"
                color = (0, 255, 200)
        else:
            if self.winner == HUMAN:
                msg = "X WINS!"
                color = (255, 80, 120)
            else:
                msg = "O WINS!"
                color = (0, 255, 200)

        # hộp thông báo
        box_w, box_h = 460, 200
        box = pygame.Rect(
            WIDTH // 2 - box_w // 2,
            HEIGHT // 2 - box_h // 2,
            box_w,
            box_h
        )

        pygame.draw.rect(
            self.screen,
            (18, 18, 28),
            box,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            color,
            box,
            3,
            border_radius=15
        )

        msg_render = self.win_font.render(msg, True, color)
        self.screen.blit(
            msg_render,
            (
                box.centerx - msg_render.get_width() // 2,
                box.y + 50
            )
        )

        hint = self.font.render(
            "Click to continue",
            True,
            (180, 180, 180)
        )
        self.screen.blit(
            hint,
            (
                box.centerx - hint.get_width() // 2,
                box.bottom - 55
            )
        )

    #  AI

    def ai_move(self):

        move = self.ai.choose_move(self.board)

        if move is None:
            return

        r, c = move

        self.board.make_move(r, c)

        self.move_count += 1

        result = get_game_result(
            self.board.grid,
            r,
            c
        )

        if result is not None:

            self.game_over = True
            self.winner = result
            self.show_win_popup = True

            if result != DRAW:
                self.winning_cells = self.find_winning_cells(result)

        else:

            self.board.switch_player()
    #  AI UPDATE

    def update_ai(self):

        if not self.ai_enabled:
            return

        if not self.ai_thinking:
            return

        if (
            pygame.time.get_ticks() - self.ai_think_start
            >= self.ai_think_delay
        ):

            self.ai_thinking = False
            self.ai_move()

    #  ACTIONS 

    def do_restart(self):

        self.board.reset()

        self.game_over = False
        self.winner = None
        self.winning_cells = []
        self.move_count = 0
        self.ai_thinking = False
        self.show_win_popup = False

    def do_menu(self):

        self.do_restart()
        self.in_menu = True

    #  INPUT 

    def handle_click(self, pos):

        # Đang mở hộp xác nhận -> chỉ xử lý YES / NO
        if self.confirm_action is not None:

            if self.confirm_yes_button.collidepoint(pos):

                if self.confirm_action == "restart":
                    self.do_restart()
                elif self.confirm_action == "menu":
                    self.do_menu()

                self.confirm_action = None

            elif self.confirm_no_button.collidepoint(pos):

                self.confirm_action = None

            return

        # RESTART / MENU luôn bấm được -> hỏi xác nhận
        if self.restart_button.collidepoint(pos):
            self.confirm_action = "restart"
            return

        if self.menu_button.collidepoint(pos):
            self.confirm_action = "menu"
            return

        # Đang hiện thông báo thắng -> bấm bất kỳ đâu để đóng
        if self.show_win_popup:
            self.show_win_popup = False
            return

        if self.game_over:
            return

        if (
            self.ai_enabled and
            self.board.current_player == AI
        ):
            return

        x, y = pos

        if not (
            self.offset_x <= x < self.offset_x + self.board_pixel_size and
            self.offset_y <= y < self.offset_y + self.board_pixel_size
        ):
            return

        c = (x - self.offset_x) // CELL_SIZE
        r = (y - self.offset_y) // CELL_SIZE

        if not (
            self.board.in_chess_bound(r, c)
            and self.board.is_empty(r, c)
        ):
            return

        self.board.make_move(r, c)

        self.move_count += 1

        result = get_game_result(
            self.board.grid,
            r,
            c
        )

        if result is not None:

            self.game_over = True
            self.winner = result
            self.show_win_popup = True

            if result != DRAW:
                self.winning_cells = self.find_winning_cells(result)

            return

        self.board.switch_player()

        if self.ai_enabled:

            self.ai_thinking = True
            self.ai_think_start = pygame.time.get_ticks()

    #  MAIN LOOP 

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                if self.in_menu:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_menu_click(event.pos)

                else:

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(event.pos)

            if not self.in_menu and self.confirm_action is None:
                self.update_ai()

            if self.in_menu:

                self.draw_menu()

            else:

                self.draw_background()

                self.draw_grid()

                self.draw_winning_line()

                self.draw_pieces()

                self.draw_hover_piece()

                self.draw_side_panel()

                # Thông báo thắng / hộp thoại xác nhận vẽ trên cùng
                self.draw_win_popup()
                self.draw_confirm_dialog()

            pygame.display.update()

        pygame.quit()