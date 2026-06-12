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

def get_grid_MTPT():
    """Return the fixed grid for BFS_MTPT"""
    A = [[2, 0, 1, 2],
         [1, 2, 0, 0],
         [0, 1, 2, 1],
         [2, 1, 0, 2]]
    A[0][1] = 0  # Mark starting position
    return A

def BFS_MTPT():
    A = [[2, 0, 1, 2],
         [1, 2, 0, 0],
         [0, 1, 2, 1],
         [2, 1, 0, 2]]
    B = [[1, 1, 0, 2],
         [2, 0, 2, 0],
         [0, 0, 1, 2],
         [1, 0, 2, 0]]
    i_A , j_A = 0, 1
    i_B, j_B = 0, 1
    A[i_A][j_A] = 0
    B[i_B][j_B] = 0
    goal = [[0, 0, 0, 2],
            [2, 0, 2, 0],
            [0, 0, 0, 2],
            [0, 0, 2, 0]]
    queue = []
    queue.append(Node(i_A,j_A,A,None,None,0))
    queue.append(Node(i_B,j_B,B,None,None,0))
    reached = []
    for x in queue: reached.append((tuple(tuple(row) for row in x.STATE),0,1))
    path_states = []
    actions = []
    end = None
    find = False
    while queue:
        children = []
        for x in queue:
            if x.STATE == goal: 
                return [goal],[]
        for parent in queue:
            moves = get_actions(parent.i,parent.j)
            moves = remove_block(parent.i,parent.j,moves,parent.STATE)
            for action in moves:
                state_child =  copy.deepcopy(parent.STATE)
                i_child,j_child = next_pos(parent.i,parent.j,action)
                state_child[i_child][j_child] = 0
                key = tuple(tuple(row) for row in state_child)
                if key not in reached:
                    children.append(Node(i_child,j_child,state_child,action,parent,parent.COST + 1))
                    reached.append((key,i_child,j_child))
        for x in children:
            if x.STATE == goal:
                find = True
                end = x
                break
        if find: break
        queue = children
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