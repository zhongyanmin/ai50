"""
Tic Tac Toe Player
"""
import math
import copy

X = "X"
O = "O"
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
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != EMPTY:
                count += 1
     
    if board == initial_state():
        return X
    elif count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action!")
     
    board_state = copy.deepcopy(board)
    board_state[action[0]][action[1]] = player(board)

    return board_state


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            
    for j in range(len(board)):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
            
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O

    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_result = winner(board)
    if win_result == X:
        return 1
    elif win_result == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, move = max_score(board)
        return move
    else:
        _, move = min_score(board)
        return move
      
            
def max_score(board):
    base = float("-inf")
    move = None
    
    if terminal(board):
        return utility(board), None
    
    for action in actions(board):
        score, mv = min_score(result(board, action))
        
        if score > base:
            base = score
            move = action
            if base == 1:
                return base, move
            
    return base, move


def min_score(board):
    base = float("inf")
    move = None
    
    if terminal(board):
        return utility(board), None
    
    for action in actions(board):
        score, mv = max_score(result(board, action))
        if score < base:
            base = score
            move = action
            if base == -1:
                return base, move
            
    return base, move