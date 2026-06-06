import copy
import random

def get_actions(i, j, grid):
    max_rows = len(grid)
    max_cols = len(grid[0]) if grid else 0
    moves = []
    if i > 0:
        moves.append("UP")
    if i < max_rows - 1:
        moves.append("DOWN")
    if j > 0:
        moves.append("LEFT")
    if j < max_cols - 1:
        moves.append("RIGHT")
    return moves


def remove_block(i, j, moves, grid):
    result = moves.copy()
    if "UP" in result and grid[i-1][j] == 2:
        result.remove("UP")
    if "DOWN" in result and grid[i+1][j] == 2:
        result.remove("DOWN")
    if "LEFT" in result and grid[i][j-1] == 2:
        result.remove("LEFT")
    if "RIGHT" in result and grid[i][j+1] == 2:
        result.remove("RIGHT")
    return result


def next_pos(i, j, action):
    if action == "UP":
        return i - 1, j
    if action == "DOWN":
        return i + 1, j
    if action == "LEFT":
        return i, j - 1
    if action == "RIGHT":
        return i, j + 1
    return i, j


def find_goal(grid):
    return [[0 if cell != 2 else 2 for cell in row] for row in grid]

def score(state):
    return sum(1 for row in state for cell in row if cell == 1)

def solve(grid, start_i, start_j):
    goal = find_goal(grid)
    current_state = copy.deepcopy(grid)
    current_state[start_i][start_j] = 0

    if current_state == goal:
        return [current_state], []

    current_score = score(current_state)
    path_states = [current_state]
    actions = []
    current_i, current_j = start_i, start_j

    while True:
        move_list = get_actions(current_i, current_j, current_state)
        move_list = remove_block(current_i, current_j, move_list, current_state)

        found_better = False
        for action in move_list:
            next_i, next_j = next_pos(current_i, current_j, action)
            child = copy.deepcopy(current_state)
            if child[next_i][next_j] == 1:
                child[next_i][next_j] = 0
            child_score = score(child)
            if child_score < current_score:
                current_score = child_score
                current_state = child
                current_i, current_j = next_i, next_j
                actions.append(action)
                path_states.append(current_state)
                found_better = True
                break

        if not found_better:
            break

        if current_state == goal:
            return path_states, actions

    return [], []

Leo_Đồi_Đơn_Giản = solve
