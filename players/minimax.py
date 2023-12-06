import numpy as np
import pdb
import utils
import random

def get_computer_move(board: np.ndarray, which_player: int):
    """Search for the best move based on the current game state.
    Parameters
    ----------
    board : np.array of ints
    2D array for the current state of the board
    (0=empty, 1=player1, 2=player2).
    which_player : int
    The AI player may want to know which player [1, 2] they are!
    Returns
    -------
    choice : int
    The column (using 1-indexing!) that the player wants to drop a disc into.
    """
    best_move, _ = minimax(board, which_player + 1, depth=3, alpha=float('-inf'), beta=float('inf'))
    print(best_move)
    return best_move + 1

def minimax(board, player, depth, alpha, beta):
    # If the depth is 0 or the game is over, return
    if depth == 0 or utils.is_gameover(board)[0]:
        return None, cost(board, player)

    # Find the possible valid moves
    valid_moves = utils.get_valid_moves(board)

    if player == 1:  # Maximizing player (should be the AI)
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = simulate_move(board, move, player)
            _, eval = minimax(new_board, 3 - player, depth - 1, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:  # Minimizing player (should be the opponent)
        min_eval = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = simulate_move(board, move, player)
            _, eval = minimax(new_board, 3 - player, depth - 1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval


def cost(board, player):
    opponent = 3 - player

    if utils.is_winner(board, player):
        return 1e10  # AI wins
    elif utils.is_winner(board, opponent):
        return -1e10  # Opponent wins

    value = 0

    # Check for proximity to AI player's pieces
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == player:
                # Add value for each neighboring position
                for x in range(i - 1, i + 2):
                    for y in range(j - 1, j + 2):
                        # Sorry about this line
                        if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and (x != i or y != j):
                            if board[x, y] == player:
                                value += 1

    return value

# Works as intended
def simulate_move(board, move, player):
    new_board = board.copy()
    new_board[np.argmin(board[:, move])][move] = player
    return new_board