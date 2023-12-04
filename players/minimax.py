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
    valid_moves = utils.get_valid_moves(board)
    pdb.set_trace()
    best_move = minimax(board, which_player + 1, depth=3, alpha=float('-inf'), beta=float('inf'))
    return np.random.choice(valid_moves) + 1

def minimax(board, player, depth, alpha, beta):
    if depth == 0 or utils.is_gameover(board):
        return
    
    for move in utils.get_valid_moves():
        new_board = simulate_move(board, move, player)
        value = cost(new_board, player)

# It runs, not great heuristic though (fix later)
def cost(board, player):
    if utils.is_winner(board, player):
        return 1e10 # Large number, might have to change this later
    value = -1
    # Check for multiple in sequence in rows
    for row in board:
        value = max(len(sum(np.where(row == player))), value)
    # Check for multiple in sequence in cols
    for col in range(board.shape[1] - 1):
        value = max(len(sum(np.where(board[:,col] == player))), value)
    return value

# Works as intended
def simulate_move(board, move, player):
    new_board = board.copy()
    new_board[np.argmin(board[:, move])][move] = player
    return new_board


    