import numpy as np
import pdb
import utils
import random

STUPID_GLOBAL = -1

def get_computer_move(board: np.ndarray, which_player: int):
    global STUPID_GLOBAL
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
    STUPID_GLOBAL = which_player
    best_move, _ = minimax(
        board, which_player + 1, depth=4, alpha=float("-inf"), beta=float("inf")
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
    row_value = 0
    for row in range(board.shape[0]):
        for col in range(board.shape[1] - 3):
            row_value += evaluate_window(board[row][col : col + 4], player)
    col_value = 0
    for col in range(board.shape[1]):
        for row in range(board.shape[0] - 3):
            col_value += evaluate_window(board[:, col][row : row + 4], player)

    # Some stackoverflow witch craft comment code
    # https://stackoverflow.com/a/6313414
    diags = [board[::-1,:].diagonal(i) for i in range(-board.shape[0]+1,board.shape[1])]
    diags.extend(board.diagonal(i) for i in range(board.shape[1]-1,-board.shape[0],-1))
    diags = [n.tolist() for n in diags]

    diag_value = 0
    for val in diags:
        if len(val) == 4:
            diag_value += evaluate_window(val, player)
        elif len(val) > 4:
            for i in range(len(val)-3):
                diag_value += evaluate_window(val[i:i+4], player)
    return row_value + col_value + diag_value


def evaluate_window(window, player):
    window = np.array(window)
    opponent = 3 - player

    if STUPID_GLOBAL == 0:
        our_count = np.count_nonzero(window == player)
        their_count = np.count_nonzero(window == opponent)
    else:
        our_count = np.count_nonzero(window == opponent)
        their_count = np.count_nonzero(window == player)
    if our_count == 4:
        return 1e10
    if their_count == 4:
        return -1e10
    if our_count == 3:
        return 10
    if their_count == 3:
        return -15
    if our_count == 2:
        return 5
    return 0


# Works as intended
def simulate_move(board, move, player):
    new_board = board.copy()
    new_board[np.argmin(board[:, move])][move] = player
    return new_board
