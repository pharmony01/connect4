# lefty-lucy.py
# Connect Four AI player that always picks the leftmost column.

import pdb
import utils

def get_computer_move(board, which_player):
    """Pick the leftmost available move.

    Parameters
    ----------
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    which_player : int
        The AI player may want to know which player [1, 2] they are!

    Returns
    -------
    col : int
        The column (using 1-indexing!) that the player wants to drop a disc into.
    """
    valid_moves = utils.get_valid_moves(board)
    return valid_moves[0] + 1