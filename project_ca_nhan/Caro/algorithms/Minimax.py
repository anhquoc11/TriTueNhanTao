
from algorithms.Utility import EMPTY, X, O, is_winner, is_full, utility, available_moves, copy_board


def minimax(board, maximizing):
    u = utility(board)
    if u != 0 or is_full(board):
        return u, None

    if maximizing:
        best_score = -float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = X
            score, _ = minimax(nb, False)
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = O
            score, _ = minimax(nb, True)
            if score < best_score:
                best_score = score
                best_move = (i, j)
        return best_score, best_move


def get_best_move(board, player):
    if player == X:
        _, move = minimax(board, True)
        return move
    else:
        _, move = minimax(board, False)
        return move
