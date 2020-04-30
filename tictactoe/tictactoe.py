"""
Tic Tac Toe Player
"""

import math
import copy

#Players
X = "X"
O = "O"

#Board = State
#Action = (i, j) <-> Means put current player on positin i, j on the board

EMPTY = None
turnCounter = 0

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    #Check if game is already over
    if(terminal(board)): return None #Any value acceptable in this case
    
    #X moves first
    if(board == initial_state()):
        turnCounter += 1
        return X

    #Keep track of the sequence of turns
    if(turnCounter%2 == 0):
        player = O
    else:
        player = X

    #Update total number of turns
    turnCounter += 1
    return player 
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #Check if game is already over
    if(terminal(board)): return None #Any value acceptable in this case

    #Initialize returning set
    actions = set()

    #Look for available actions on the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            # "Box" must be EMPTY to be available
            if(board[i][j] == EMPTY):
                set.add((i,j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Check if action is valid raise an Exception otherwise
    if not action in actions(board):
        #TODO Resolve import errors and raise InvalidActionError()
        pass
    
    #Functional Implementation needed by the MiniMax algorithm
    resultboard = copy.deepcopy(board)

    #Retrieve current/active player
    player = player(board)

    #Apply the action to the current state
    i,j = action
    resultboard[i][j] = player

    #Then return the new State
    return resultboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check for a tris in horizontally vertically and diagonally
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j])
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
