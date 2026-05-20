import pygame
import random

from src.game.board import Board
from src.game.constants import *
from src.game.rules import get_game_result


class CaroGameUI:

    def __init__(self):

        pygame.init()

        # ================= FIX HEIGHT (QUAN TRỌNG) =================
        # thêm 100px để chứa TURN TEXT
        global HEIGHT
        HEIGHT = BOARD_SIZE * CELL_SIZE + 100

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Caro Game")

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 26)
        self.big_font = pygame.font.SysFont("arial", 40)
        self.popup_font = pygame.font.SysFont("arial", 34)

        self.board = Board()

        # ================= FIX LAYOUT =================
        self.board_pixel_size = BOARD_SIZE * CELL_SIZE + 1

        self.offset_x = (WIDTH - self.board_pixel_size) // 2
        self.offset_y = (HEIGHT - self.board_pixel_size) // 2

        # STATE
        self.running = True
        self.in_menu = True
        self.game_over = False
        self.winner = None

        # MODE
        self.ai_enabled = False

        # AI STATE
        self.ai_thinking = False
        self.ai_think_start = 0
        self.ai_think_delay = 400

        # MENU BUTTONS
        self.pvp_button = pygame.Rect(WIDTH // 2 - 180, 250, 360, 70)
        self.pvai_button = pygame.Rect(WIDTH // 2 - 180, 350, 360, 70)

        # END BUTTONS
        self.restart_button = pygame.Rect(WIDTH // 2 - 170, HEIGHT // 2 + 40, 150, 55)
        self.menu_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 40, 150, 55)

    # ================= MENU =================

    def draw_menu(self):

        self.screen.fill((240, 240, 240))

        title = self.big_font.render("CARO GAME", True, (0, 0, 0))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 120))

        pygame.draw.rect(self.screen, (70, 130, 180), self.pvp_button, border_radius=12)
        pygame.draw.rect(self.screen, (220, 20, 60), self.pvai_button, border_radius=12)

        self.draw_center_text("Player vs Player", self.pvp_button, (255, 255, 255))
        self.draw_center_text("Player vs AI", self.pvai_button, (255, 255, 255))

    def draw_center_text(self, text, rect, color):

        img = self.font.render(text, True, color)
        self.screen.blit(
            img,
            (rect.centerx - img.get_width() // 2,
             rect.centery - img.get_height() // 2)
        )

    def handle_menu_click(self, pos):

        if self.pvp_button.collidepoint(pos):
            self.ai_enabled = False
            self.in_menu = False

        elif self.pvai_button.collidepoint(pos):
            self.ai_enabled = True
            self.in_menu = False

    # ================= GRID =================

    def draw_grid(self):

        x0 = self.offset_x
        y0 = self.offset_y
        size = self.board_pixel_size

        for i in range(BOARD_SIZE + 1):
            x = x0 + i * CELL_SIZE
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x, y0), (x, y0 + size), 1)

        for i in range(BOARD_SIZE + 1):
            y = y0 + i * CELL_SIZE
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x0, y), (x0 + size, y), 1)

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (x0, y0, size, size),
            2
        )

    # ================= PIECES =================

    def draw_pieces(self):

        pad = 8

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):

                v = self.board.grid[r][c]

                x = self.offset_x + c * CELL_SIZE
                y = self.offset_y + r * CELL_SIZE

                cx = x + CELL_SIZE // 2
                cy = y + CELL_SIZE // 2

                if v == HUMAN:

                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (x + pad, y + pad),
                                     (x + CELL_SIZE - pad, y + CELL_SIZE - pad), 3)

                    pygame.draw.line(self.screen, (255, 0, 0),
                                     (x + CELL_SIZE - pad, y + pad),
                                     (x + pad, y + CELL_SIZE - pad), 3)

                elif v == AI:

                    pygame.draw.circle(self.screen, (0, 0, 255),
                                       (cx, cy), CELL_SIZE // 2 - pad, 3)

    # ================= STATUS (SAFE NOW) =================

    def draw_status(self):

        if self.game_over:
            return

        if self.ai_thinking:
            text = "Turn: AI"
        else:
            if self.ai_enabled:
                text = "Turn: YOU" if self.board.current_player == HUMAN else "Turn: AI"
            else:
                text = "Turn: X" if self.board.current_player == HUMAN else "Turn: O"

        img = self.font.render(text, True, (0, 0, 0))

        # luôn nằm dưới bàn cờ (trong vùng HEIGHT mới)
        self.screen.blit(
            img,
            (self.offset_x, self.offset_y + self.board_pixel_size + 10)
        )

    # ================= GAME OVER =================

    def draw_game_over(self):

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 120, 400, 220)
        pygame.draw.rect(self.screen, (255, 255, 255), box, border_radius=12)

        msg = "Draw!"
        if self.winner == HUMAN:
            msg = "X Wins!"
        elif self.winner == AI:
            msg = "O Wins!"

        txt = self.popup_font.render(msg, True, (0, 0, 0))
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - 50))

        pygame.draw.rect(self.screen, (70, 130, 180), self.restart_button, border_radius=10)
        pygame.draw.rect(self.screen, (220, 20, 60), self.menu_button, border_radius=10)

        self.draw_center_text("Restart", self.restart_button, (255, 255, 255))
        self.draw_center_text("Menu", self.menu_button, (255, 255, 255))

    # ================= AI =================

    def ai_move(self):

        moves = self.board.available_neighbors()

        if not moves:
            return

        r, c = random.choice(moves)

        self.board.make_move(r, c)

        result = get_game_result(self.board.grid, r, c)

        if result is not None:
            self.game_over = True
            self.winner = result
        else:
            self.board.switch_player()

    def update_ai(self):

        if not self.ai_enabled or not self.ai_thinking:
            return

        if pygame.time.get_ticks() - self.ai_think_start >= self.ai_think_delay:
            self.ai_thinking = False
            self.ai_move()

    # ================= INPUT =================

    def handle_click(self, pos):

        if self.game_over:

            if self.restart_button.collidepoint(pos):
                self.board.reset()
                self.game_over = False
                self.winner = None

            elif self.menu_button.collidepoint(pos):
                self.board.reset()
                self.game_over = False
                self.in_menu = True

            return

        if self.ai_enabled and self.board.current_player == AI:
            return

        x, y = pos

        if not (
            self.offset_x <= x < self.offset_x + self.board_pixel_size and
            self.offset_y <= y < self.offset_y + self.board_pixel_size
        ):
            return

        c = (x - self.offset_x) // CELL_SIZE
        r = (y - self.offset_y) // CELL_SIZE

        if not self.board.is_valid_move(r, c):
            return

        self.board.make_move(r, c)

        result = get_game_result(self.board.grid, r, c)

        if result is not None:
            self.game_over = True
            self.winner = result
            return

        self.board.switch_player()

        if self.ai_enabled:
            self.ai_thinking = True
            self.ai_think_start = pygame.time.get_ticks()

    # ================= MAIN LOOP =================

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

            if not self.in_menu:
                self.update_ai()

            if self.in_menu:
                self.draw_menu()
            else:
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                self.draw_pieces()
                self.draw_status()

                if self.game_over:
                    self.draw_game_over()

            pygame.display.update()
#hhu
        pygame.quit()