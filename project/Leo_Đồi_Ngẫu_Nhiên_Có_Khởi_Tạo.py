import random
import copy 

def find_goal(a):
    GOAL = copy.deepcopy(a)
    for t in range(len(a)):
        for z in range(len(a[0])):
            if GOAL[t][z] != 2: GOAL[t][z] = 0
    return GOAL      

class Node():
    def __init__(self,i, j, state, action, parent, cost, path_cost):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
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

def solve(grid, start_i, start_j):
    goal = find_goal(grid)
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0

    if start_state == goal:
        return [start_state], []

    end = None
    path_states = []
    actions = []
    i = 0
    find = False
    while i < 20:
        parent = Node(start_i,start_j,start_state,None,None,h(start_state),0)
        while True:
            moves = get_actions(parent.i,parent.j)
            moves = remove_block(parent.i,parent.j,moves,parent.STATE)
            children = []
            for action in moves:
                state_child = copy.deepcopy(parent.STATE)
                i_child, j_child = next_pos(parent.i,parent.j,action)
                state_child[i_child][j_child] = 0
                cost = h(state_child)
                if cost < parent.COST: children.append(Node(i_child,j_child,state_child,action,parent,cost,parent.PATH_COST + 1))
                if state_child == goal: 
                    end = Node(i_child,j_child,state_child,action,parent,cost,parent.PATH_COST + 1)
                    find = True
                    break
            if find: break
            if len(children) == 0:
                break
            parent = random.choice(children)
        if find: break
        i += 1
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

Leo_Đồi_Ngẫu_Nhiên_Có_Khởi_Tạo = solve



