# connect4.py 
# Play Connect Four in Python!
#
# Connect Four is a two-player game in which players alternate dropping 
# colored discs in one of several columns on the board. Each disc drops
# to the lowest row possible. The first player to connect four discs
# (horizontally, vertically, or diagonally) wins!
#
# Author: Matthew Eicholtz

import argparse
from copy import deepcopy
import numpy as np
import pdb
import time
import utils

DELAY = 0.1  # default time to wait between things, in seconds
TIMEOUT = 5  # maximum time per move, in seconds

parser = argparse.ArgumentParser(description="Play Connect Four in Python!")
parser.add_argument('--player1', metavar='p1', type=str, help="either 'human' (default) or the name of an AI file", default='human')
parser.add_argument('--player2', metavar='p2', type=str, help="either 'human' (default) or the name of an AI file", default='human')
parser.add_argument('-r', '--rows', type=int, help="number of rows on the board (default=6)", default=6)
parser.add_argument('-c', '--cols', type=int, help="number of columns on the board (default=7)", default=7)
parser.add_argument('-b', '--board', type=str, help="filename containing starting board state")
parser.add_argument('--fast', action='store_true', help='flag to speed up the game by not using graphics (AI only)')
parser.add_argument('--verbose', action='store_true', help="display game details")
parser.add_argument('--version', action='version', version=utils.get_version())

def main(args):
    if args.verbose:
        print("\nLet's play Connect Four!")
        print("=" * 50)

    # Load AI player(s) if necessary
    players = utils.load_players(args.player1, args.player2, verbose=args.verbose)
    
    # Play the game
    play(players, **vars(args))

def play(players, rows=6, cols=7, board=None, fast=False, verbose=False, **kwargs):
    """Play a game of Connect Four.

    Parameters
    ----------
    players : dict of lists
        Dictionary of information for each player. Keys include 'name', 'id', and 'ai'.
        For AI players, the 'ai' module must contain a get_computer_move function.
    rows : int
        Number of rows on the board (default=6).
    cols : int
        Number of columns on the board (default=7).
    board : str
        Filename containing a starting board state (if desired). This is primarily used for
        testing and debugging purposes.
    fast : bool
        Flag that determines whether to show graphics (False) or not (True) (default=False).
        Only matters if both players are non-human.
    verbose : bool
        Print status updates to the terminal (default=False).

    Returns
    -------
    winner : int
        Who won the game? (1=player1, 2=player2, 0=tie, -1=undetermined)
    """
    if verbose: print("Starting the game..")

    # Non-graphics play only valid when no humans are playing
    if 'human' in players['name']:
        fast = False

    # Load board from file (if provided)
    if board:
        data = np.loadtxt(board, dtype=str)
        board = np.array([[int(char) for char in string] for string in data]) # convert data to 2D arrays of ints
        if rows != board.shape[0]:
            print(f'WARNING: The specified number of rows does not match the board file provided. Setting rows = {board.shape[0]}.')
            rows = board.shape[0]
        if cols != board.shape[1]:
            print(f'WARNING: The specified number of columns does not match the board file provided. Setting columns = {board.shape[1]}.')
            cols = board.shape[1]
        board = np.flipud(board) # flip to accommodate utility functions and position of (0,0) place on board
    else: # use an empty board
        board = np.zeros((rows, cols), dtype=int)
    
    # Initialize the graphical user interface
    gui = utils.setup(board)
    params = gui.items[-1]  # extract the global parameters used to create the GUI

    # Determine whose turn it is (toggle between 0 and 1)
    current_player = 1 if np.count_nonzero(board == 1) > np.count_nonzero(board == 2) else 0

    # Play the game
    gameover = False
    while not gameover:
        # Store player ID for easier verbose mode
        player_id = players['id'][current_player]

        # Ask current player to make a move
        if players['name'][current_player] == 'human':
            utils.status(gui, f"{player_id}, pick a column (1-{cols})...")

            key = gui.checkKey()
            if key == "Escape" or key == "Ctrl+e": # exit game
                break
            elif key == 'd': # debug
                pdb.set_trace()
            elif key == 'b': # show board state
                temp = np.flipud(board)
                for row in temp:
                    for element in row:
                        print(element, end="")
                    print()
                print()
            elif key == "Ctrl+n": # start new game
                utils.reset(gui)
                board = np.zeros((rows, cols))
                current_player = 0
            elif key in [str(i + 1) for i in range(cols)]:
                col = int(key) # index of desired column
                if verbose: print(f'\t{player_id} selects column {col}')
                
                # Validate the move
                col = col - 1 # convert to 0-indexing
                if utils.is_valid(board, col):
                    utils.drop(gui, board, current_player, col)
                    current_player = 1 - current_player # switch turns
                else: # the player must forfeit for illegal moves
                    pass # currently allows human to make illegal moves
                    # utils.status(gui, f"{player_id} made an illegal move. You forfeit!")
                    # break
        else: # AI player
            utils.status(gui, f"{player_id} is thinking...")
            if not fast: time.sleep(DELAY)
            try:
                col = players['ai'][current_player].get_computer_move(deepcopy(board), current_player)
                if verbose: print(f'\t{player_id} selects column {col}')
                
                # Validate the move
                col = col - 1 # convert to 0-indexing
                if utils.is_valid(board, col):
                    utils.drop(gui, board, current_player, col)
                    current_player = 1 - current_player # switch turns
                else: # the player must forfeit for illegal moves
                    utils.status(gui, f"{player_id} made an illegal move. You forfeit!")
                    break
            except:
                # pdb.set_trace()
                utils.status(gui, f"{player_id} loses their turn due to code error")
                current_player = 1 - current_player # you lost your turn!

        # Check if game is over yet
        gameover, winner = utils.is_gameover(board)

    # Show result
    if winner == 0:
        msg = "TIE!"
        utils.status(gui, msg)
        if verbose: print(msg)
    elif winner in [1, 2]:
        msg = f"{players['id'][winner - 1].upper()} WINS!"
        utils.status(gui, msg)
        if verbose: print(msg)

    # Wait for user to quit
    while True:
        key = gui.checkKey()
        if key == "Escape" or key == "Ctrl+e": # exit game
            break
        elif key == 'd': # debug
            pdb.set_trace()

if __name__ == "__main__":
    args = parser.parse_args()
    utils.check_args(args)
    main(args)