from itertools import cycle
from math import inf
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
        return [[move.label for move in row] for row in self._current_moves]

    def get_available_positions(self):
        return [
            (move.row, move.col)
            for row in self._current_moves
            for move in row
            if move.label == ""
        ]

    def toggle_player(self):
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def _get_winner_from_labels(self, board_labels):
        for combo in self._winning_combos:
            labels_in_combo = {board_labels[row][col] for row, col in combo}
            if len(labels_in_combo) == 1 and "" not in labels_in_combo:
                return next(iter(labels_in_combo))
        return None

    def _get_available_positions_from_labels(self, board_labels):
        return [
            (row, col)
            for row in range(self.board_size)
            for col in range(self.board_size)
            if board_labels[row][col] == ""
        ]

    def minimax(self, board_labels, is_maximizing):
        """Compute best move score and coordinates for a simulated turn.

        Args:
            board_labels: 2D list of board labels for current simulation node.
            is_maximizing: `True` when AI turn is being evaluated, else `False`.

        Returns:
            - Tuple `(score, (row, col))` for best available move in this node.
            - Score values: `1` for AI-winning branch, `0` for draw, `-1` for human-winning branch.

        Used by:
            - `get_ai_move()` for real AI choice.
            - Recursively calls itself to explore the full game tree.
        """
        winner = self._get_winner_from_labels(board_labels)
        if winner == self.ai_label:
            return 1, (-1, -1)
        if winner == self.human_label:
            return -1, (-1, -1)

        available_positions = self._get_available_positions_from_labels(board_labels)
        if not available_positions:
            return 0, (-1, -1)

        if is_maximizing:
            best_score = -inf
            best_move = (-1, -1)
            for row, col in available_positions:
                board_labels[row][col] = self.ai_label
                score, _ = self.minimax(board_labels, False)
                board_labels[row][col] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            return best_score, best_move

        best_score = inf
        best_move = (-1, -1)
        for row, col in available_positions:
            board_labels[row][col] = self.human_label
            score, _ = self.minimax(board_labels, True)
            board_labels[row][col] = ""
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move

    def get_ai_move(self):
        _score, (row, col) = self.minimax(self.get_board_labels(), True)
        return Move(row, col, self.ai_label)

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        no_winner = not self._has_winner
        played_moves = (move.label for row in self._current_moves for move in row)
        return no_winner and all(played_moves)

    def reset_game(self):
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []
