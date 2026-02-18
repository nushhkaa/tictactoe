"""Application entrypoint for tic-tac-toe."""

from game_logic import TicTacToeGame
from gui import TicTacToeBoard


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()