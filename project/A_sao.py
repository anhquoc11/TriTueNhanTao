import random
import copy 

def find_goal(a):
    GOAL = copy.deepcopy(a)
    for t in range(4):
        for z in range(4):
            if GOAL[t][z] != 2: GOAL[t][z] = 0
    return GOAL      

class Node():
    def __init__(self,i, j, state, action, parent, g, cost, path_cost):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.G = g
        self.COST = cost
        self.PATH_COST = path_cost

def get_actions(i,j):
    result = []
    if i > 0: result.append("UP")
    if i < 3: result.append("DOWN")
    if j > 0: result.append("LEFT")
    if j < 3: result.append("RIGHT")
    return result

def remove_block(i, j, move, x):
    result = move.copy()
    if "UP" in result and x[i-1][j] == 2: result.remove("UP")
    if "DOWN" in result and x[i+1][j] == 2: result.remove("DOWN")
    if "LEFT" in result and x[i][j-1] == 2: result.remove("LEFT")
    if "RIGHT" in result and x[i][j+1] == 2: result.remove("RIGHT")
    return result

def next_pos(i,j,x):
    if x == "UP": return i-1,j
    if x == "DOWN": return i+1,j
    if x == "RIGHT": return i,j+1
    if x == "LEFT": return i,j-1

def print_board(board):
    for row in board:
        print(row)
    print()
def h(board):
    cost = 0
    for t in range(len(board)):
        for z in range(len(board[0])):
            if board[t][z] == 1: cost += 1
    return cost

def add_(queue, x):
    for index in range(len(queue)):
        if x.COST <= queue[index].COST: 
            queue.insert(index,x)
            return queue
    queue.append(x)
    return queue
def solve(grid, start_i, start_j):
    goal = find_goal(grid)
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0

    if start_state == goal:
        return [start_state], []

    queue_priority = []
    reached = {}
    start_node = Node(start_i, start_j, start_state, None, None, 0, h(start_state), 0)
    queue_priority = add_(queue_priority, start_node)
    reached[(start_i, start_j, tuple(tuple(row) for row in start_state))] = 0

    end = None
    while queue_priority:
        cur = queue_priority.pop(0)
        if cur.STATE == goal:
            end = cur
            break
        move_list = remove_block(cur.i, cur.j, get_actions(cur.i, cur.j), cur.STATE)
        for action in move_list:
            state_child = copy.deepcopy(cur.STATE)
            i_child, j_child = next_pos(cur.i, cur.j, action)
            energy = 2 if state_child[i_child][j_child] == 1 else 1
            g_child = cur.G + energy
            state_child[i_child][j_child] = 0
            child = Node(i_child, j_child, state_child, action, cur, g_child, h(state_child) + g_child, cur.PATH_COST + 1)
            state_tuple = tuple(tuple(row) for row in state_child)
            key = (i_child, j_child, state_tuple)
            if key not in reached or g_child < reached[key]:
                queue_priority = add_(queue_priority, child)
                reached[key] = g_child

    path_states = []
    actions = []
    if end is not None:
        node = end
        while node is not None:
            path_states.append(node.STATE)
            if node.ACTION is not None:
                actions.append(node.ACTION)
            node = node.PARENT
        path_states.reverse()
        actions.reverse()
    return path_states, actions


A_sao = solve



