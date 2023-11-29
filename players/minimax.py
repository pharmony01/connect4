import numpy as np
import pdb
import utils
import random

def get_computer_move(board, which_player):
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
    def is_terminal():
        ...
    
    def minimax():
        ...

    def cost():
        ...
    
    valid_moves = utils.get_valid_moves(board)
    return np.random.choice(valid_moves) + 1