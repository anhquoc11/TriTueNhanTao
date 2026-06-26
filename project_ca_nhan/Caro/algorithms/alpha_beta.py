
from algorithms.Utility import EMPTY, X, O, is_winner, is_full, utility, available_moves, copy_board


def alphabeta(board, maximizing, alpha, beta):
    u = utility(board)
    if u != 0 or is_full(board):
        return u, None

    if maximizing:
        best_score = -float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = X
            score, _ = alphabeta(nb, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = (i, j)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = O
            score, _ = alphabeta(nb, True, alpha, beta)
            if score < best_score:
                best_score = score
                best_move = (i, j)
            beta = min(beta, score)
            if alpha >= beta:
                break
        return best_score, best_move


def get_best_move(board, player):
    if player == X:
        _, move = alphabeta(board, True, -float('inf'), float('inf'))
        return move
    else:
        _, move = alphabeta(board, False, -float('inf'), float('inf'))
        return move
