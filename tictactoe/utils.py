#Players
X = "X"
O = "O"


def horizontalcheck(board):
    """
        Tries to find the player who has done an horizontal tris None otherwise
    """
    for i in range(len(board)):
        x = 0
        o = 0
        for j in range(len(board[i])):
            #Horizontal increment check
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
            #Check first for a winner
        if x== 3:
            return X
        if o == 3 :
            return O
    return None

def verticalCheck(board):
    """
        Tries to find the player who has done a vertical tris None otherwise
    """
    for i in range(len(board)):
        o = 0
        x = 0
        for j in range(len(board[i])):
            #Vertical increment check
            if board[j][i] == X:
                x += 1
            elif board[j][i] == O:
                o += 1
            #Check first for a winner
            if o == 3:
                return O
            if x == 3:
                return X 
    return None

def diagonalCheck(board):
    """
        Tries to find the player who has done a diagonal tris None otherwise
    """
    for i in range(len(board)):
        o = 0
        x = 0
        for j in range(len(board[i])):
            #Diagonal increment check
            if board[j][j] == X:
                x += 1
            elif board[j][j] == O:
                o += 1
            #Check first for a winner
            if o == 3:
                return O
            if x == 3:
                return X 
    return None
