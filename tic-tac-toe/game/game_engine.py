from game.rules import check_winner, is_board_full
from game.renderer import (
    board_pos_to_cell,
    START_X_RECT,
    START_O_RECT,
    RESTART_RECT,
    RESET_MATCH_RECT
)
from game.ai import choose_move


HUMAN_SYMBOL = 'X'
COMPUTER_SYMBOL = 'O'


class GameEngine:

    def __init__(self):

        # -------------------------
        # MATCH SCOREBOARD
        # -------------------------

        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        # -------------------------
        # STARTER SELECTION
        # -------------------------

        self.first_player = 'X'

        # -------------------------
        # CURRENT ROUND
        # -------------------------

        self.board = [[None] * 3 for _ in range(3)]

        self.current_player = self.first_player

        self.round_over = False
        self.winner = None

    # ==========================================================
    # MOUSE CLICK HANDLING
    # ==========================================================

    def handle_click(self, pos):

        # -----------------------------------
        # Starter selection
        # -----------------------------------

        if START_X_RECT.collidepoint(pos):
            self.first_player = 'X'
            return

        if START_O_RECT.collidepoint(pos):
            self.first_player = 'O'
            return

        # -----------------------------------
        # Restart Round button
        # -----------------------------------

        if RESTART_RECT.collidepoint(pos):
            self.restart_round()
            return

        # -----------------------------------
        # Reset Match button
        # -----------------------------------

        if RESET_MATCH_RECT.collidepoint(pos):
            self.reset_match()
            return

        # -----------------------------------
        # Ignore board clicks after round ends
        # -----------------------------------

        if self.round_over:
            return

        # -----------------------------------
        # Only human can click the board
        # -----------------------------------

        if self.current_player != HUMAN_SYMBOL:
            return

        # -----------------------------------
        # Convert mouse position to cell
        # -----------------------------------

        cell = board_pos_to_cell(pos)

        if cell is None:
            return

        row, col = cell

        # -----------------------------------
        # Reject occupied cells
        # -----------------------------------

        if self.board[row][col] is not None:
            return

        # -----------------------------------
        # Place X
        # -----------------------------------

        self.board[row][col] = HUMAN_SYMBOL

        # Check result
        self.check_round_end()

        # If round ended, stop
        if self.round_over:
            return

        # -----------------------------------
        # Computer's turn
        # -----------------------------------

        self.current_player = COMPUTER_SYMBOL

        self._maybe_take_computer_turn()

    # ==========================================================
    # COMPUTER MOVE
    # ==========================================================

    def _maybe_take_computer_turn(self):

        if self.round_over:
            return

        if self.current_player != COMPUTER_SYMBOL:
            return

        # Ask AI for an empty cell
        move = choose_move(self.board)

        if move is None:
            return

        row, col = move

        # Place O
        self.board[row][col] = COMPUTER_SYMBOL

        # Check result
        self.check_round_end()

        # If round ended, stop
        if self.round_over:
            return

        # Give turn back to human
        self.current_player = HUMAN_SYMBOL

    # ==========================================================
    # KEYBOARD
    # ==========================================================

    def handle_keydown(self, key):

        import pygame

        # R = Restart Round
        if key == pygame.K_r:
            self.restart_round()

        # M = Reset Match
        elif key == pygame.K_m:
            self.reset_match()

    # ==========================================================
    # RESTART ROUND
    # ==========================================================

    def restart_round(self):

        # Clear only the current round
        self.board = [[None] * 3 for _ in range(3)]

        # Apply selected starter
        self.current_player = self.first_player

        self.round_over = False
        self.winner = None

        # If O was selected as starter,
        # computer automatically moves first.
        if self.current_player == COMPUTER_SYMBOL:
            self._maybe_take_computer_turn()

    # ==========================================================
    # RESET MATCH
    # ==========================================================

    def reset_match(self):

        # Reset scoreboard
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        # Reset the round
        self.board = [[None] * 3 for _ in range(3)]

        # Use currently selected starter
        self.current_player = self.first_player

        self.round_over = False
        self.winner = None

        # If O starts, computer moves first
        if self.current_player == COMPUTER_SYMBOL:
            self._maybe_take_computer_turn()

    # ==========================================================
    # CHECK ROUND RESULT
    # ==========================================================

    def check_round_end(self):

        # -----------------------------------
        # CHECK WINNER FIRST
        # -----------------------------------

        winner = check_winner(self.board)

        if winner:

            self.round_over = True
            self.winner = winner

            # Update scoreboard
            if winner == 'X':
                self.x_wins += 1
            else:
                self.o_wins += 1

            return

        # -----------------------------------
        # CHECK DRAW SECOND
        # -----------------------------------

        if is_board_full(self.board):

            self.round_over = True
            self.winner = None

            self.draws += 1

    # ==========================================================
    # DRAW EVERYTHING
    # ==========================================================

    def draw(self, surface, font):

        from game import renderer

        # Board
        renderer.draw_board(
            surface,
            self.board
        )

        # Scoreboard
        renderer.draw_scoreboard(
            surface,
            font,
            self.x_wins,
            self.o_wins,
            self.draws
        )

        # Starter controls
        renderer.draw_controls(
            surface,
            font,
            self.first_player
        )

        # Current turn
        if not self.round_over:

            if self.current_player == HUMAN_SYMBOL:
                turn_text = "Your turn (X)"
            else:
                turn_text = "Computer's turn (O)"

            renderer.draw_text(
                surface,
                font,
                turn_text,
                (10, 490)
            )

        # Result banner
        if self.round_over:

            if self.winner:
                result_text = f"{self.winner} wins!"
            else:
                result_text = "Draw!"

            renderer.draw_banner(
                surface,
                font,
                result_text
            )

        # Action buttons
        renderer.draw_action_buttons(
            surface,
            font
        )