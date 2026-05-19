#main.py
import pygame
import sys
from src.config import *
from src.game import CaroGame
from src.ai import get_ai_move


def draw_ui(screen, game, font_large, font_medium, font_small, buttons):
    screen.fill(WHITE)
    pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.line(screen, BLACK, (0, HEADER_HEIGHT), (WIDTH, HEADER_HEIGHT), 2)

    mouse_pos = pygame.mouse.get_pos()

    for btn_name, btn_rect in buttons["modes"].items():
        is_hover = btn_rect.collidepoint(mouse_pos)
        is_active = btn_name == game.mode

        btn_color = GRAY if (is_hover or is_active) and btn_name != "Reset" else WHITE
        if btn_name == "Reset" and is_hover:
            btn_color = GRAY

        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, btn_rect, 2, border_radius=5)
        text_surf = font_medium.render(btn_name, True, BLACK)
        screen.blit(text_surf, text_surf.get_rect(center=btn_rect.center))

    for btn_name, btn_rect in buttons["algos"].items():
        is_hover = btn_rect.collidepoint(mouse_pos)
        is_active = btn_name == game.ai_algo

        if game.mode == "PvP":
            btn_color = WHITE
            text_color = DARK_GRAY
        else:
            btn_color = GRAY if (is_hover or is_active) else WHITE
            text_color = BLACK

        pygame.draw.rect(screen, btn_color, btn_rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, btn_rect, 2, border_radius=5)
        text_surf = font_small.render(btn_name, True, text_color)
        screen.blit(text_surf, text_surf.get_rect(center=btn_rect.center))

    if game.game_over:
        status_text = "Hòa!" if game.winner == "Tie" else f"{'X' if game.winner == PLAYER_X else 'O'} Thắng!"
    else:
        if game.mode == "PvE":
            status_text = f"Lượt: {'X (Bạn)' if game.current_player == PLAYER_X else 'O (Máy)'}"
        else:
            status_text = f"Lượt: {'X' if game.current_player == PLAYER_X else 'O'}"

    status_surf = font_large.render(status_text, True, BLACK)
    screen.blit(status_surf, status_surf.get_rect(midright=(WIDTH - 20, HEADER_HEIGHT // 2 + 10)))

    if game.game_over and game.winner != "Tie":
        for r, c in game.win_cells:
            pygame.draw.rect(screen, GREEN, (OFFSET_X + c * CELL_SIZE, OFFSET_Y + r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, DARK_GRAY, (OFFSET_X + i * CELL_SIZE, OFFSET_Y),
                         (OFFSET_X + i * CELL_SIZE, OFFSET_Y + BOARD_SIZE), 1)
        pygame.draw.line(screen, DARK_GRAY, (OFFSET_X, OFFSET_Y + i * CELL_SIZE),
                         (OFFSET_X + BOARD_SIZE, OFFSET_Y + i * CELL_SIZE), 1)

    font_cell = pygame.font.Font(r'C:\Windows\Fonts\arialbd.ttf', int(CELL_SIZE * 0.5))

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cx = OFFSET_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2
            if game.grid[r][c] == PLAYER_X:
                text_surf = font_cell.render("X", True, RED)
                screen.blit(text_surf, text_surf.get_rect(center=(cx, cy)))
            elif game.grid[r][c] == PLAYER_O:
                text_surf = font_cell.render("O", True, BLUE)
                screen.blit(text_surf, text_surf.get_rect(center=(cx, cy)))

    pygame.display.flip()


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cờ Caro")

    font_large = pygame.font.Font(r'C:\Windows\Fonts\arialbd.ttf', 28)
    font_medium = pygame.font.Font(r'C:\Windows\Fonts\arialbd.ttf', 20)
    font_small = pygame.font.Font(r'C:\Windows\Fonts\arialbd.ttf', 14)

    game = CaroGame()

    btn_w, btn_h = 80, 35
    buttons = {
        "modes": {
            "PvP": pygame.Rect(20, 15, btn_w, btn_h),
            "PvE": pygame.Rect(110, 15, btn_w, btn_h),
            "Reset": pygame.Rect(200, 15, btn_w, btn_h),
        },
        "algos": {
            "Minimax": pygame.Rect(20, 65, 120, 35),
            "Alpha-Beta": pygame.Rect(150, 65, 130, 35)
        }
    }

    clock = pygame.time.Clock()
    running = True

    while running:
        draw_ui(screen, game, font_large, font_medium, font_small, buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                for name, rect in buttons["modes"].items():
                    if rect.collidepoint(mouse_pos):
                        if name == "Reset":
                            game.reset()
                        else:
                            game.mode = name
                            game.reset()

                if game.mode == "PvE":
                    for name, rect in buttons["algos"].items():
                        if rect.collidepoint(mouse_pos):
                            game.ai_algo = name

                if not game.game_over:
                    is_human_turn = False
                    if game.mode == "PvP":
                        is_human_turn = True
                    elif game.mode == "PvE" and game.current_player == PLAYER_X:
                        is_human_turn = True

                    if is_human_turn:
                        c = (mouse_pos[0] - OFFSET_X) // CELL_SIZE
                        r = (mouse_pos[1] - OFFSET_Y) // CELL_SIZE
                        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                            game.make_move(r, c)

        if not game.game_over:
            if game.mode == "PvE" and game.current_player == PLAYER_O:
                draw_ui(screen, game, font_large, font_medium, font_small, buttons)
                pygame.display.update()

                move = get_ai_move(game.grid, algorithm=game.ai_algo, ai_player=PLAYER_O, random_first=False)
                if move:
                    game.make_move(move[0], move[1])

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()