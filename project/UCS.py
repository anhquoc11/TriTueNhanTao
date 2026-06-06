import random
import copy 

def find_goal(a):
    GOAL = copy.deepcopy(a)
    for t in range(4):
        for z in range(4):
            if GOAL[t][z] != 2: GOAL[t][z] = 0
    return GOAL
        
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

def add_(queue, x):
    for i in range(len(queue)):
        if x.COST <= queue[i].COST: 
            queue.insert(i,x)
            return queue
    queue.append(x)
    return queue

def UCS(grid, start_i, start_j):
    GOAL = find_goal(grid)
    queue_priority = []
    reached = {}
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if start_state == GOAL:
        print("SÀN NHÀ ĐÃ ĐƯỢC DỌN SẠCH")
        print_board(GOAL)
        return [start_state], []
    queue_priority.append(Node(start_i,start_j,start_state,None,None,0))
    reached[(start_i, start_j, tuple(tuple(row) for row in start_state))] = 0

    find = False
    while queue_priority:
        cur = queue_priority.pop(0)
        if cur.STATE == GOAL: 
            find = True
            end = cur
            break
        move_list = remove_block(cur.i,cur.j,get_actions(cur.i,cur.j),cur.STATE)
        for action in move_list:
            state_child = copy.deepcopy(cur.STATE)
            i_child , j_child = next_pos(cur.i,cur.j,action)
            if state_child[i_child][j_child] == 1: cost = 2
            else : cost = 1
            state_child[i_child][j_child] = 0
            child = Node(i_child,j_child,state_child,action,cur,cur.COST + cost)
            state_tuple = tuple(tuple(row) for row in state_child)
            if (i_child,j_child,state_tuple) not in reached.keys() or child.COST < reached[i_child,j_child,state_tuple]:
                queue_priority = add_(queue_priority,child)
                reached[i_child,j_child,state_tuple] = child.COST
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

solve = UCS
