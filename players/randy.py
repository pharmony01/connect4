# randy.py
# Connect Four AI player that chooses everything randomly.

import pdb
import random
import utils

def get_computer_move(board, which_player):
    """Randomly select a move from the set of valid moves.

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
    return random.choice(valid_moves) + 1