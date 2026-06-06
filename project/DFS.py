import random
import copy 

class Node():
    def __init__(self,i, j, state, action, parent, cost):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.COST = cost

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

def find_goal(a):
    GOAL = copy.deepcopy(a)
    for t in range(4):
        for z in range(4):
            if GOAL[t][z] != 2: GOAL[t][z] = 0
    return GOAL 
def DFS(grid, start_i, start_j):
    GOAL = find_goal(grid)
    stack = []
    reached = []
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if start_state == GOAL:
        print("SÀN NHÀ ĐÃ ĐƯỢC DỌN SẠCH")
        print_board(GOAL)
        return [start_state], []
    stack.append(Node(start_i,start_j,start_state,None,None,0))
    reached.append((start_i,start_j, tuple(tuple(row) for row in start_state)))

    find = False
    while stack:
        cur = stack.pop()
        move_list = remove_block(cur.i,cur.j,get_actions(cur.i,cur.j),cur.STATE)
        for action in move_list:
            state_child = copy.deepcopy(cur.STATE)
            i_child , j_child = next_pos(cur.i,cur.j,action)
            state_child[i_child][j_child] = 0
            child = Node(i_child,j_child,state_child,action,cur,cur.COST + 1)
            if state_child == GOAL: 
                end = child
                find = True
                break
            state_tuple = tuple(tuple(row) for row in state_child)
            if (i_child,j_child,state_tuple) not in reached:
                stack.append(child)
                reached.append((i_child,j_child,state_tuple))
        if find: break

    path_states = []
    actions = []

    if find:
        cur = end
        while cur is not None:
            path_states.append(cur.STATE)
            if cur.ACTION is not None:
                actions.append(cur.ACTION)
            cur = cur.PARENT
        path_states.reverse()
        actions.reverse()
    return path_states, actions



