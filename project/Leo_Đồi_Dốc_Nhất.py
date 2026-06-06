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


def value(state):
    """Giá trị càng nhỏ càng tốt: số ô bẩn còn lại."""
    return sum(1 for row in state for cell in row if cell == 1)


def solve(grid, start_i, start_j):
    goal = find_goal(grid)
    current_state = copy.deepcopy(grid)
    current_state[start_i][start_j] = 0

    if current_state == goal:
        return [current_state], []

    current_value = value(current_state)
    path_states = [current_state]
    actions = []
    current_i, current_j = start_i, start_j

    while True:
        moves = get_actions(current_i, current_j, current_state)
        moves = remove_block(current_i, current_j, moves, current_state)

        neighbors = []
        for action in moves:
            next_i, next_j = next_pos(current_i, current_j, action)
            child = copy.deepcopy(current_state)
            if child[next_i][next_j] == 1:
                child[next_i][next_j] = 0
            neighbors.append((value(child), action, next_i, next_j, child))

        if not neighbors:
            break

        better_neighbors = [n for n in neighbors if n[0] < current_value]
        if not better_neighbors:
            break

        best_value = min(n[0] for n in better_neighbors)
        best_candidates = [n for n in better_neighbors if n[0] == best_value]
        best_value, best_action, best_i, best_j, best_state = random.choice(best_candidates)

        current_value = best_value
        current_state = best_state
        current_i, current_j = best_i, best_j
        actions.append(best_action)
        path_states.append(current_state)

        if current_state == goal:
            return path_states, actions

    return [], []


Leo_Đồi_Dốc_Nhất = solve
