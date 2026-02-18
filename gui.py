"""Tkinter GUI for tic-tac-toe."""

import tkinter as tk
from tkinter import font

from game_logic import Move


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._coords_to_button = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()
        self.after(100, self._handle_ai_turn)

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                self._coords_to_button[(row, col)] = button
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        if self._game.current_player.label != self._game.human_label:
            return

        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            game_over = self._apply_and_refresh(move, clicked_btn)
            if not game_over and self._game.current_player.label == self._game.ai_label:
                self.after(100, self._handle_ai_turn)

    def _handle_ai_turn(self):
        if self._game.current_player.label != self._game.ai_label:
            return
        if self._game.has_winner() or self._game.is_tied():
            return

        ai_move = self._game.get_ai_move()
        if not self._game.is_valid_move(ai_move):
            self._update_display(msg="AI move invalid", color="red")
            return

        clicked_btn = self._coords_to_button[(ai_move.row, ai_move.col)]
        self._apply_and_refresh(ai_move, clicked_btn)

    def _apply_and_refresh(self, move, clicked_btn):
        self._update_button(clicked_btn)
        self._game.process_move(move)
        if self._game.is_tied():
            self._update_display(msg="Tied game!", color="red")
            return True
        if self._game.has_winner():
            self._highlight_cells()
            msg = f'Player "{self._game.current_player.label}" won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
            return True

        self._game.toggle_player()
        msg = f"{self._game.current_player.label}'s turn"
        self._update_display(msg)
        return False

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        while self._game.current_player.label != self._game.ai_label:
            self._game.toggle_player()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
        self.after(100, self._handle_ai_turn)
