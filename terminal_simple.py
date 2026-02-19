"""Terminal tic-tac-toe game with minimax AI - Simple procedural version."""

from math import inf


def initialize_board():
    """Create an empty 3x3 board."""
    return [[" " for _ in range(3)] for _ in range(3)]


def display_board(board):
    """Print the board with row and column labels."""
    print("\n    0   1   2")
    print("  +---+---+---+")
    for row_idx in range(3):
        print(f"{row_idx} | {board[row_idx][0]} | {board[row_idx][1]} | {board[row_idx][2]} |")
        print("  +---+---+---+")
    print()


def get_available_moves(board):
    """Return list of (row, col) for empty cells."""
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                moves.append((row, col))
    return moves


def check_winner(board, player):
    """Check if player has won. Return True if won."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    
    return False


def is_board_full(board):
    """Check if board has no empty cells."""
    return all(board[row][col] != " " for row in range(3) for col in range(3))


def minimax(board, is_maximizing, ai_player="X", human_player="O"):
    """Minimax algorithm to find best move.
    
    Args:
        board: Current board state.
        is_maximizing: True for AI turn, False for human turn.
        ai_player: AI label (default "X").
        human_player: Human label (default "O").
    
    Returns:
        (score, (row, col)) where score is 1 (AI win), 0 (draw), -1 (human win).
    """
    # Terminal states
    if check_winner(board, ai_player):
        return 1, (-1, -1)
    if check_winner(board, human_player):
        return -1, (-1, -1)
    if is_board_full(board):
        return 0, (-1, -1)
    
    available_moves = get_available_moves(board)
    
    if is_maximizing:
        best_score = -inf
        best_move = (-1, -1)
        for row, col in available_moves:
            board[row][col] = ai_player
            score, _ = minimax(board, False, ai_player, human_player)
            board[row][col] = " "
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move
    else:
        best_score = inf
        best_move = (-1, -1)
        for row, col in available_moves:
            board[row][col] = human_player
            score, _ = minimax(board, True, ai_player, human_player)
            board[row][col] = " "
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move


def get_human_move(board):
    """Get and validate human (O) move."""
    while True:
        try:
            user_input = input("Your move (row col, e.g., '1 2'): ").strip()
            row, col = map(int, user_input.split())
            
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid: Enter numbers 0-2 for row and column.")
                continue
            
            if board[row][col] != " ":
                print("Invalid: Cell already occupied.")
                continue
            
            return row, col
        except ValueError:
            print("Invalid input. Please enter row and column as two numbers (0-2).")


def play_game():
    """Main game loop."""
    board = initialize_board()
    ai_player = "X"
    human_player = "O"
    current_player = ai_player
    
    print("=" * 40)
    print("  TERMINAL TIC-TAC-TOE with MINIMAX AI")
    print("=" * 40)
    print("\nYou are O (human).  AI is X (computer).")
    print("Rows and columns are numbered 0-2.\n")
    print("AI goes first (X). You go second (O).\n")
    
    display_board(board)
    
    while True:
        # AI turn
        if current_player == ai_player:
            print("AI is thinking...")
            score, (row, col) = minimax(board, True, ai_player, human_player)
            board[row][col] = ai_player
            print(f"X played at row {row}, col {col}.\n")
            
            display_board(board)
            
            if check_winner(board, ai_player):
                print("X wins!")
                break
            if is_board_full(board):
                print("Game is tied!")
                break
            
            current_player = human_player
        
        # Human turn
        else:
            print("Your turn (O).")
            row, col = get_human_move(board)
            board[row][col] = human_player
            print(f"O played at row {row}, col {col}.\n")
            
            display_board(board)
            
            if check_winner(board, human_player):
                print("O win! Congratulations!")
                break
            if is_board_full(board):
                print("Game is tied!")
                break
            
            current_player = ai_player
    
    print("=" * 40)
    play_again = input("Play again? (yes/no): ").strip().lower()
    if play_again in ["yes", "y"]:
        play_game()
    else:
        print("Thanks for playing!")


if __name__ == "__main__":
    play_game()
