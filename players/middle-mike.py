# middle-mike.py
# Connect Four AI player that always tries to pick one of the middle columns.

import numpy as np
import pdb
import random
import utils

def get_computer_move(board, which_player):
    """Pick the middlemost available move.

    Parameters
    ----------
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    which_player : int
        The AI player may want to know which player [1, 2] they are!

    Returns
    -------
    choice : int
        The column (using 1-indexing!) that the player wants to drop a disc into.
    """

    # Get all valid moves
    valid_moves = utils.get_valid_moves(board)
    
    # Determine which moves is closest to the middle
    cols = board.shape[1]
    if cols % 2 == 1: # odd number of columns
        ideal = cols // 2
    else: # even number of columns
        ideal = cols // 2 - 0.5
    distance = abs(valid_moves - ideal)
    options = [valid_moves[i] for i, j in enumerate(distance) if j == np.min(distance)]
    
    # Choose randomly from the options that are equidistant from the middle
    choice = random.choice(options)

    return choice + 1