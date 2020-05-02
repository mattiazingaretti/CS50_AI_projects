"""
Tic Tac Toe Player
"""

import math
import copy
import utils as u


#Players
X = "X" #He is the MAX player
O = "O" #He is the MIN player

#Board = State
#Action = (i, j) <-> Means put current player on positin i, j on the board

EMPTY = None

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
        return X
    #Count total number of non empty players on the grid 
    total = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != EMPTY:
                total += 1
    #if the total is odd then is O turn
    if total%2 != 0:
        return O
    #otherwise it's X turn
    return X
    

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
                actions.add((i,j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #Check if action is valid raise an Exception otherwise
    if not action in actions(board):
        raise NameError("Invalid Action Attempted!")
        
    #Functional Implementation needed by the MiniMax algorithm
    resultboard = copy.deepcopy(board)
    
    #Apply the action to the current state
    i,j = action
    resultboard[i][j] = player(board)

    #Then return the new State
    return resultboard

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Check for a tris in horizontally vertically and diagonally
    check1 = u.horizontalcheck(board)
    check2 = u.verticalCheck(board)
    check3 = u.diagonalCheck(board)
    #Evaluate thoose checks and return the winner if it exists
    if  check1 != None:
        return check1
    elif check2 != None:
        return check2
    elif check3 != None:
        return check3         
    #Otherwise There is no winner 
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    #Check for a draw
    else:
        for i in range(len(board)):
            for j in range(len(board[i])):
                #Stil there are actions available so game is not ended
                if board[i][j] == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0

def Max(board):
    if terminal(board):
        return utility(board)
    v = -1
    for a in actions(board):
        v = max(v,Min(result(board,a)))
    return v

def Min(board):
    if terminal(board):
        return utility(board)
    v = 1
    for a in actions(board):
        v = min(v, Max(result(board, a)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #Retrieve the current player
    p = player(board)
    
    #If game is over return None
    if terminal(board):
        return None

    # if current player is X pick the action in actions(board) such as
    # it has the bigger value of Min(result(board, a))
    if p == X:
        values = {}
        for a in actions(board):
            values[a] = Min(result(board, a))
        v = max(list(values.values()))
        keys = list(values)
        if len(keys)>0:
            for k in list(values):
                if values.get(k) == v:
                    return k
    # if current player is O pick the action in actions(board) such as
    # it has the smallest value of Max(result(board, a))
    elif p == O:
        values = {}
        for a in actions(board):
            values[a] = Max(result(board, a))
        v = min(list(values.values()))
        keys = list(values)
        if len(keys)>0:
            for k in keys:
                if values.get(k) == v:
                    return k        
    
    
