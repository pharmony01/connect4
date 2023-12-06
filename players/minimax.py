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
    best_move, _ = minimax(
        board, which_player + 1, depth=3, alpha=float("-inf"), beta=float("inf")
    )
    print(f"Chosen move: {_}")
    return best_move + 1


def minimax(board, player, depth, alpha, beta):
    # If the depth is 0 or the game is over, return
    if depth == 0 or utils.is_gameover(board)[0]:
        return None, cost(board, player)

    # Find the possible valid moves
    valid_moves = utils.get_valid_moves(board)

    if player == 1:
        value = float("-inf")
        best_move = None
        for move in valid_moves:
            new_board = simulate_move(board, move, player)
            _, eval = minimax(new_board, 3 - player, depth - 1, alpha, beta)
            if eval > value:
                value = eval
                best_move = move
            if value > beta:
                break
            alpha = max(alpha, value)
        return best_move, value
    else:
        value = float("inf")
        best_move = None
        for move in valid_moves:
            new_board = simulate_move(board, move, player)
            _, eval = minimax(new_board, 3 - player, depth - 1, alpha, beta)
            if eval < value:
                value = eval
                best_move = move
            if value < alpha:
                break
            beta = min(beta, value)
        return best_move, value


def cost(board, player):
    value = 0
    for row in range(board.shape[0]):
        for col in range(board.shape[1] - 3):
            value += evaluate_window(board[row][col : col + 4], player)
    for col in range(board.shape[1]):
        for row in range(board.shape[0] - 3):
            value += evaluate_window(board[:, col][row : row + 4], player)

    return value


def evaluate_window(window, player):
    opponent = 3 - player
    if np.count_nonzero(window == opponent) == 4:
        return 1e10
    if np.count_nonzero(window == opponent) == 3:
        return 10
    if np.count_nonzero(window == opponent) == 2:
        return 5
    if np.count_nonzero(window == player) == 4:
        return -1e10
    if np.count_nonzero(window == player) == 3:
        return -15
    else:
        return 0


# Works as intended
def simulate_move(board, move, player):
    new_board = board.copy()
    new_board[np.argmin(board[:, move])][move] = player
    return new_board
