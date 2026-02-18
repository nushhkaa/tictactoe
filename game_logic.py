"""Core game logic for tic-tac-toe."""

from itertools import cycle
from typing import NamedTuple


class Player(NamedTuple):
    label: str
    color: str


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)
AI_LABEL = "X"
HUMAN_LABEL = "O"


class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.ai_label = AI_LABEL
        self.human_label = HUMAN_LABEL
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def get_board_labels(self):
        """Return the board as labels only: '', 'X', or 'O'."""
        return [
            [move.label for move in row]
            for row in self._current_moves
        ]

    def get_available_positions(self):
        """Return available positions as a list of (row, col)."""
        return [
            (move.row, move.col)
            for row in self._current_moves
            for move in row
            if move.label == ""
        ]

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def minimax(self, board_labels, is_maximizing):
        """Placeholder for your minimax implementation.

        Args:
            board_labels: 2D list board state from get_board_labels().
            is_maximizing: True for AI turn, False for human turn.

        Returns:
            Expected to return one of:
            - (score, (row, col))
            - (row, col)
        """
        _ = board_labels
        _ = is_maximizing
        return self.get_available_positions()[0]

    def get_ai_move(self):
        """Get AI move using minimax placeholder and normalize output."""
        result = self.minimax(self.get_board_labels(), True)
        if (
            isinstance(result, tuple)
            and len(result) == 2
            and isinstance(result[1], tuple)
        ):
            row, col = result[1]
            return Move(row, col, self.ai_label)

        row, col = result
        return Move(row, col, self.ai_label)

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []
