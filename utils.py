# utils.py
# Utility functions for Connect 4.
#
# Author: Matthew Eicholtz

from graphics import *
import importlib
import numpy as np
import os
import pdb
import subprocess
import sys

ROOT = os.path.dirname(os.path.realpath(__file__))
COLORS = { # dictionary of colors relevant to the game user interface
	'background': '#f0f0f0',
	'board': '#007be7',
	'outline': '#005399',
	'player1': '#f6d22f',
	'player2': '#e74235',
	'text': '#000000'
	}
DISC = 25 # radius of each disc, in pixels
FONT = 12 # font size for instructions
HEADER = 30 # space for instructions at the top of the board, in pixels
MARGIN = 15 # margin on side of the board, in pixels

def check_args(args):
    """Helper function to run error checks on the argparse arguments.
    
    Parameters
    ----------
    args : argparse.Namespace
        Output from parse_args() method of the ArgumentParser object
    """
    if 'rows' not in args or args.rows < 4:
        raise Exception('The number of rows must be at least 4. Check inputs.')
    if 'cols' not in args or args.cols < 4:
        raise Exception('The number of columns must be at least 4. Check inputs.')
    
def drop(gui, board, player, col):
    """Update the game when a player drops a discs in a specific column on the board.

    Parameters
    ----------
    gui : GraphWin object
        The main graphics window for the game.
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    player : int
        The player index (0-indexing) specifying who is taking the action.
    col : int
        The column index (0-indexing) in which to drop the disc.
    """
    
    # Determine which row the disc will drop to
    rows = get_next_available_rows(board)
    row = rows[col]

    # Update graphics
    holes = gui.items[1:-1]
    disc = holes[sub2ind(board.shape[1], row, col)]
    disc.setFill(COLORS['player1' if player == 0 else 'player2'])
    
    # Update the board
    board[row][col] = player + 1

def get_next_available_rows(board, invalid=-1):
    """Find the row index for the next disc in any column.
    
    Parameters
    ----------
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    invalid : int (default=-1)
        Value to provide when no rows are available in a given column.

    Returns
    -------
    rows : np.array of ints
        List of next available row for each column.
    """
    mask = board == 0
    rows = np.where(mask.any(axis=0), mask.argmax(axis=0), invalid)
    return rows

def get_valid_moves(board):
    """Determine which columns are still available.
    
    Parameters
    ----------
    board: np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).

    Returns
    -------
    cols : np.array of ints
        List of columns that are not full yet.
    """
    rows = get_next_available_rows(board)
    cols = np.flatnonzero(rows >= 0)
    return cols

def get_version():
    """Retrieve the current git hash to use as a 'version' number."""
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

def is_gameover(board):
    """Check to see if the game is over yet.
    
    Parameters
    ----------
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).

    Returns
    -------
    gameover : bool
        Is the game over (True) or not (False).
    winner : int
        Who won the game? (1=player1, 2=player2, 0=tie, -1=undetermined)
    """
    if get_valid_moves(board).size == 0: # tie
        gameover = True
        winner = 0
    elif is_winner(board, 1): # player 1 wins
        gameover = True
        winner = 1
    elif is_winner(board, 2): # player 2 wins
        gameover = True
        winner = 2
    else: # game is not over yet
        gameover = False
        winner = -1

    return gameover, winner

def is_valid(board, col):
    """Determine whether a potential move (defined by a desired column)
    is valid based on the current board state. In other words, is there
    at least one open row in that column?

    Parameters
    ----------
    board : np.array
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    col : int
        The column index (0-indexing) to validate.
    
    Returns
    -------
    isvalid : bool
        True if there is at least one open row available in that column;
        false otherwise.
    """
    rows = get_next_available_rows(board)
    return rows[col] >= 0

def is_winner(board, player):
    """Check to see if a specific player has connected four discs.
    
    Parameters
    ----------
    board : np.array of ints
        2D array for the current state of the board (0=empty, 1=player1, 2=player2).
    player : int
        Which player are we checking? (using 1-indexing here!)

    Returns
    -------
    winner : bool
        Did the player win (True) or not (False)?
    """
    rows, cols = board.shape
    # Check vertically
    for row in range(rows):
        for col in range(cols - 3):
            if (board[row][col] == player and
                    board[row][col + 1] == player and
                    board[row][col + 2] == player and
                    board[row][col + 3] == player):
                return True

    # Check horizontally
    for row in range(rows - 3):
        for col in range(cols):
            if (board[row][col] == player and
                    board[row + 1][col] == player and
                    board[row + 2][col] == player and
                    board[row + 3][col] == player):
                return True

    # Check diagonally
    for row in range(rows - 3):
        for col in range(cols - 3):
            if (board[row][col] == player and
                    board[row + 1][col + 1] == player and
                    board[row + 2][col + 2] == player and
                    board[row + 3][col + 3] == player):
                return True

    # Check anti-diagonally
    for row in range(3, rows):
        for col in range(cols - 3):
            if (board[row][col] == player and
                    board[row - 1][col + 1] == player and
                    board[row - 2][col + 2] == player and
                    board[row - 3][col + 3] == player):
                return True

def load_players(player1, player2, verbose=False):
    """Load AI players from file, if needed.
    
    Parameters
    ----------
    player1 : str
        Name of Python file containing AI code for the first player, or 'human'.
    player2 : str
        Name of Python file containing AI code for the second player, or 'human'.

    Returns
    -------
    players : list of str
    	List containing the player names.
    ai : list of imported modules
    	List of imported AI player functions (None if human).
    """
    if verbose: print(f"Loading players...")

    # Initialize outputs
    players = [player1, player2]
    ai = [None, None]

    # Try loading each player
    for i in range(len(players)):
        if players[i] == "human":
            if verbose: print(f"\tPlayer {i + 1} is a human.")
        else: # AI player
            if verbose: print(f"\tPlayer {i + 1} AI ({players[i]})...", end="")
            try:
                pathname, filename = os.path.split(os.path.abspath(players[i]))
                filename = ''.join(filename.split('.')[:-1])  # remove filename extension
                players[i] = filename  # simplify the player name for display
                sys.path.append(pathname)  # add directory containing AI player to system path
                ai[i] = importlib.import_module(filename)
            except ImportError:
                print(f"\n\tERROR: Cannot import AI player from file ({players[i]})")
                return 0

            if not hasattr(ai[i], 'get_computer_move'):
                print(f"\n\tERROR: This AI player ({players[i]}) does not have a 'get_computer_move' function")
                return 0
            if verbose: print("complete")

    return players, ai

def reset(gui, delay=1.0):
    """Reset the user interface elements in order to start a new game.

    Parameters
    ----------
    gui : GraphWin object
        The main graphics window for the game.
    delay : float
        Amount of time to pause after resetting the game (default=1.0).
    """
    status(gui, "Starting new game...")
    holes = gui.items[1:-1]
    for hole in holes:
        hole.setFill(COLORS['background'])
    time.sleep(delay)
    status(gui, "")

def setup(rows=6, cols=7):
    """Create the graphical user interface for the game.
    
    Parameters
    ----------
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.

    Returns
    -------
    gui : GraphWin object
        The graphics object containing all of the necessary UI elements.
    """
    # Input checking
    if rows < 4:
        raise Exception(f'ERROR: The number of rows ({rows}) must be at least 4. Check inputs.')
    if cols < 4:
        raise Exception(f'ERROR: The number of columns ({columns}) must be at least 4. Check inputs.')

    # Make game window
    wid = cols * (2.5 * DISC) + MARGIN * 2
    hei = rows * (2.5 * DISC) + MARGIN * 2 + HEADER
    gui = GraphWin("Connect Four", wid, hei)
    gui.setCoords(0, 0, wid, hei) # put origin in bottom-left corner

    # Add board
    board = Rectangle(Point(MARGIN, MARGIN), Point(wid - MARGIN, hei - MARGIN - HEADER))
    board.setFill(COLORS['board'])
    board.setOutline(COLORS['outline'])
    board.setWidth(4)
    board.draw(gui)

    # Add holes
    for row in range(rows):
        for col in range(cols):
            x = MARGIN + 1.25 * DISC * (2 * col + 1)
            y = MARGIN + 1.25 * DISC * (2 * row + 1)
            hole = Circle(Point(x, y), DISC)
            hole.setFill(COLORS['background'])
            hole.setOutline(COLORS['outline'])
            hole.setWidth(4)
            hole.draw(gui)

    # Add text instructions
    instructions = Text(Point(MARGIN, hei - (MARGIN + HEADER) // 2), "")
    instructions._reconfig("anchor", "w")
    instructions.setSize(FONT)
    instructions.draw(gui)

    return gui

def status(gui, msg):
    """Update the text status in the gui with a new message.

    Parameters
    ----------
    gui : GraphWin object
        The main graphics window for the game.
    msg : str
        The text message to display in the gui.
    """
    txt = gui.items[-1]
    txt.setText(msg)

def sub2ind(ncols, row, col):
    """Convert 2D subscripts (row, col) to a linear index based on the board size.

    Parameters
    ----------
    ncols : int
        Number of columns on the board.
    row : int
        The row index of a space on the board.
    col : int
        The column index of a space on the board.
	
    Returns
    -------
    ind : int
        The corresponding linear index on the board.
    """
    return row * ncols + col

def test():
    """Test utility functions for errors."""
    print('\nCONNECT FOUR')
    print('=' * 30)
    print('Testing utility functions...')
    print(f'    Version: {getversion()}')
    print(f'    Making standard board...', end='')
    gui = setup()
    while True:
        key = gui.checkKey()
        if key:
            status(gui, key)
            if key == "Escape" or key == "Ctrl+e":  # exit game
                break
            elif key == 'd':
                pdb.set_trace()
    print(f'complete')
    print(f'    Checking get_next_available_rows function...')
    # board = np.zeros((6, 7))
    board = np.random.randint(2, size=(6, 7))
    rows = get_next_available_rows(board)
    print(*board, sep='\n')
    print(f'rows = {rows}')

if __name__ == "__main__":
    test()