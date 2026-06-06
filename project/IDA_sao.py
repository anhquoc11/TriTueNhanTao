import copy

class Node:
    def __init__(self, i, j, state, action, parent, g):
        self.i = i
        self.j = j
        self.state = state
        self.action = action
        self.parent = parent
        self.g = g


def find_goal(grid):
    return [[0 if cell != 2 else 2 for cell in row] for row in grid]


def heuristic(state):
    return sum(1 for row in state for cell in row if cell == 1)


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


def state_key(i, j, state):
    return (i, j, tuple(tuple(row) for row in state))


def reconstruct_path(node):
    path_states = []
    actions = []
    while node is not None:
        path_states.append(node.state)
        if node.action is not None:
            actions.append(node.action)
        node = node.parent
    return list(reversed(path_states)), list(reversed(actions))


def depth_limited_search(node, bound, visited, goal, grid):
    f = node.g + heuristic(node.state)
    if f > bound:
        return f, None
    if node.state == goal:
        return f, node

    min_bound = float('inf')
    for action in get_actions(node.i, node.j, grid):
        i2, j2 = next_pos(node.i, node.j, action)
        if node.state[i2][j2] == 2:
            continue

        next_state = [row[:] for row in node.state]
        move_cost = 2 if next_state[i2][j2] == 1 else 1
        next_state[i2][j2] = 0
        key = state_key(i2, j2, next_state)
        if key in visited:
            continue

        visited.add(key)
        child = Node(i2, j2, next_state, action, node, node.g + move_cost)
        t, result = depth_limited_search(child, bound, visited, goal, grid)
        visited.remove(key)

        if result is not None:
            return t, result
        if t < min_bound:
            min_bound = t

    return min_bound, None


def IDA_sao(grid, start_i, start_j):
    goal = find_goal(grid)
    start_state = [row[:] for row in grid]
    if start_state[start_i][start_j] == 1:
        start_state[start_i][start_j] = 0

    if start_state == goal:
        return [start_state], []

    start_node = Node(start_i, start_j, start_state, None, None, 0)
    bound = heuristic(start_state)
    visited = {state_key(start_i, start_j, start_state)}

    while True:
        t, result = depth_limited_search(start_node, bound, visited, goal, grid)
        if result is not None:
            return reconstruct_path(result)
        if t == float('inf'):
            return [], []
        bound = t



