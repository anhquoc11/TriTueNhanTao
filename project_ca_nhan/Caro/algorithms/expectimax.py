
from algorithms.Utility import EMPTY, X, O, is_winner, is_full, utility, available_moves, copy_board


def expectimax(board, player):
    u = utility(board)
    if u != 0 or is_full(board):
        return u, None

    if player == X:
        best_score = -float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = X
            score, _ = expectimax(nb, O)
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_score, best_move
    else:
        moves = available_moves(board)
        if not moves:
            return utility(board), None
        total_score = 0
        for (i, j) in moves:
            nb = copy_board(board)
            nb[i][j] = O
            score, _ = expectimax(nb, X)
            total_score += score
        expected_score = total_score / len(moves)
        return expected_score, None


def get_best_move(board, player):
    if player == X:
        _, move = expectimax(board, X)
        return move
    else:
        best_score = -float('inf')
        best_move = None
        for (i, j) in available_moves(board):
            nb = copy_board(board)
            nb[i][j] = O
            score, _ = expectimax(nb, X)
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move
