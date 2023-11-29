# Connect Four

Play the classic two-player board game Connect Four in Python! In the game, players take turns dropping colored discs into a vertically suspended grid. The goal is to connect four of one's own discs in a row, either horizontally, vertically, or diagonally, before the opponent does. Players strategically place their discs to block their opponent's moves and create opportunities for their own winning combinations. The game is known for its simplicity yet offers engaging gameplay, requiring both tactical planning and adaptability. It is an excellent framework for AI players that leverage conventional adversarial search algorithms.

***NOTE: This repository was created for learning purposes in CSC 3510 (Introduction to Artificial Intelligence) at Florida Southern College.***

## Requirements

The code provided here was developed in Python 3.10.6 on Windows 10 using a basic text editor and a Git Bash terminal. Setup and usage may vary slightly for other operating systems or software tools. At a minimum, you will need the following Python library installed:

- numpy

In addition, the instructions that follow assume you have properly installed git on your machine. Click [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you need help doing that.

## Setup

1. The best way to use this code is to [clone the repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) to your local machine. To do so in VS Code, open a terminal and navigate to the parent directory of your choice using the `cd` command, e.g.:

        $ cd ~/Documents/csc3510

    Then, use `git clone` to create a new subdirectory called wordle with the code from this repository:

        $ git clone https://github.com/meicholtz/connect4

    Go into the directory and make sure the appropriate files are there by using the `ls` command:

        $ cd connect4
        $ ls

2. Before running the code, you need to make sure any required libraries are installed. The recommended way to do this is to [create a virtual environment](https://docs.python.org/3/library/venv.html) so that you can have separate environments for different projects. To create a virtual environment, use the `venv` command:

        $ python -m venv /path/to/new/virtual/environment

    If you do not have a preferred location for your environments, try putting them in a hidden folder in your home directory, such as:

        $ python -m venv ~/.venv/connect4

    Next, you need to activate the virtual environment using the `source` command:

        $ source ~/.venv/connect4/Scripts/activate

    You will know that you have done it correctly if you see the environment name in parentheses in your terminal, e.g. (connect4). After you are in your virtual environment, use `pip install` to install the libraries you need. It is easiest to do this with the requirements.txt file provided in the repository.

        $ pip install -r requirements.txt
        $ pip list

    Note that the second command above will list all installed libraries, which is useful for verification purposes.

## Usage

Use the following commands to play the game:

- To play Connect Four on a standard board with two human players,

        $ python connect4.py

- To play Connect Four against an AI player,

        $ python connect4.py --player1 path/to/ai/player.py
        $ python connect4.py --player2 path/to/ai/player.py

    where player.py is the generic name of any file that contains the function `get_computer_move(board, which_player)`. Several sample "dummy" AI players are provided in the players directory of this repo. For example, watch two random AI players compete using

        $ python connect4.py --player1 players/randy.py --player2 players/randy.py

There are several additional optional parameters that can be passed to connect4.py.

- If you want to change the size of the board, use

        $ python connect4.py -r 10 c -20

    This example creates a board with 10 rows and 20 columns. Note that human players can only access up to 9 columns because key presses are used to make moves. AI players, on the other hand, have complete access to the entire board, regardless of size.

- If you want to display additional game information at the command line, use

        $ python connect4.py --verbose

- If you want to speed up gameplay when using AI players, use

        $ python connect4.py --player1 ai1.py --player2 ai2.py --fast

    where `ai1.py` and `ai2.py` are placeholders for AI players of your choosing.

## Creating Custom AI Players

In order to create a custom AI player, simply make a new Python script containing the function `get_computer_move(board, which_player)` that returns a column index in which to drop a disc given the current state of the game (`board`) and which player you are competing as (`which_player`). Check out the sample players for general templates to use.

### NOTES:

1. A decent approach for creating/testing/debugging custom AI players is to put the player file in the players directory and then run games against other human or AI players.

2. You may assume that you have access to `utils.py`, so make sure to `import utils` at the top of your player file if you want to leverage those helpful functions.

3. Your choice of column should use 1-indexing, so the leftmost column is 1, not 0! If that is confusing or frustrating, simply add a "+1" to whatever 0-indexing approach you were planning to use.

4. If any player (human or AI) makes an invalid choice (e.g. a column number that does not exist or a column that is full), they forfeit the game, so be careful in your computations!