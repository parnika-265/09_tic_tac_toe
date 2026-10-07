"""
renderer: all pygame drawing lives here.
"""

import pygame


# Window
WIDTH, HEIGHT = 520, 700
WINDOW_SIZE = (WIDTH, HEIGHT)

# Board
BOARD_SIZE = 360
CELL_SIZE = BOARD_SIZE // 3
BOARD_LEFT = 80
BOARD_TOP = 120


# Colors
COLOR_BG = (245, 245, 245)
COLOR_LINE = (60, 60, 60)
COLOR_X = (200, 60, 60)
COLOR_O = (60, 100, 200)
COLOR_TEXT = (30, 30, 30)
COLOR_BUTTON = (220, 220, 220)
COLOR_SELECTED = (170, 210, 170)


# Buttons
START_X_RECT = pygame.Rect(80, 75, 100, 35)
START_O_RECT = pygame.Rect(195, 75, 100, 35)

RESTART_RECT = pygame.Rect(80, 590, 170, 45)
RESET_MATCH_RECT = pygame.Rect(270, 590, 170, 45)


def board_pos_to_cell(pos):
    x, y = pos

    x -= BOARD_LEFT
    y -= BOARD_TOP

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    return int(row), int(col)


def draw_board(surface, board):
    # Background
    surface.fill(COLOR_BG)

    # Board lines
    for i in range(1, 3):
        pygame.draw.line(
            surface,
            COLOR_LINE,
            (
                BOARD_LEFT + i * CELL_SIZE,
                BOARD_TOP
            ),
            (
                BOARD_LEFT + i * CELL_SIZE,
                BOARD_TOP + BOARD_SIZE
            ),
            3
        )

        pygame.draw.line(
            surface,
            COLOR_LINE,
            (
                BOARD_LEFT,
                BOARD_TOP + i * CELL_SIZE
            ),
            (
                BOARD_LEFT + BOARD_SIZE,
                BOARD_TOP + i * CELL_SIZE
            ),
            3
        )

    # Draw X and O
    for r in range(3):
        for c in range(3):

            symbol = board[r][c]

            if symbol is None:
                continue

            center = (
                BOARD_LEFT + c * CELL_SIZE + CELL_SIZE // 2,
                BOARD_TOP + r * CELL_SIZE + CELL_SIZE // 2
            )

            if symbol == 'X':
                offset = CELL_SIZE // 3

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] - offset,
                        center[1] - offset
                    ),
                    (
                        center[0] + offset,
                        center[1] + offset
                    ),
                    6
                )

                pygame.draw.line(
                    surface,
                    COLOR_X,
                    (
                        center[0] + offset,
                        center[1] - offset
                    ),
                    (
                        center[0] - offset,
                        center[1] + offset
                    ),
                    6
                )

            else:
                pygame.draw.circle(
                    surface,
                    COLOR_O,
                    center,
                    CELL_SIZE // 3,
                    6
                )


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(
        font.render(text, True, color),
        pos
    )


def draw_button(surface, font, rect, text, selected=False):
    if selected:
        color = COLOR_SELECTED
    else:
        color = COLOR_BUTTON

    pygame.draw.rect(
        surface,
        color,
        rect,
        border_radius=6
    )

    pygame.draw.rect(
        surface,
        COLOR_LINE,
        rect,
        width=2,
        border_radius=6
    )

    text_surface = font.render(
        text,
        True,
        COLOR_TEXT
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    surface.blit(
        text_surface,
        text_rect
    )


def draw_scoreboard(surface, font, x_wins, o_wins, draws):
    text = (
        f"X Wins: {x_wins}    "
        f"O Wins: {o_wins}    "
        f"Draws: {draws}"
    )

    text_surface = font.render(
        text,
        True,
        COLOR_TEXT
    )

    text_rect = text_surface.get_rect(
        center=(WIDTH // 2, 25)
    )

    surface.blit(
        text_surface,
        text_rect
    )


def draw_controls(surface, font, first_player):
    # Starter selection label
    draw_text(
        surface,
        font,
        "Who starts?",
        (10, 80)
    )

    # X and O starter buttons
    draw_button(
        surface,
        font,
        START_X_RECT,
        "X starts",
        selected=(first_player == 'X')
    )

    draw_button(
        surface,
        font,
        START_O_RECT,
        "O starts",
        selected=(first_player == 'O')
    )


def draw_action_buttons(surface, font):
    draw_button(
        surface,
        font,
        RESTART_RECT,
        "Restart Round"
    )

    draw_button(
        surface,
        font,
        RESET_MATCH_RECT,
        "Reset Match"
    )


def draw_banner(surface, font, text):
    surf = font.render(
        text,
        True,
        (180, 40, 40)
    )

    rect = surf.get_rect(
        center=(
            WIDTH // 2,
            BOARD_TOP + BOARD_SIZE + 40
        )
    )

    surface.blit(
        surf,
        rect
    )