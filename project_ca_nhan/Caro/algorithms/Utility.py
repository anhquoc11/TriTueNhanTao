
EMPTY = ' '
X = 'X'
O = 'O'


def is_winner(board, player):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def is_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    if is_winner(board, X):
        return 1
    if is_winner(board, O):
        return -1
    return 0


def available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.append((i, j))
    return moves


def copy_board(board):
    return [row[:] for row in board]
