import copy
from algorithms import Utility
class Node:
    def __init__(self, i, j, state, action, parent, g):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.G = g
def depth_limited_search(grid, start_i, start_j,limit):
    start_state = copy.deepcopy(grid)
    stack = []
    stack.append(Node(start_i,start_j,start_state,None,None,0))
    reached = {}
    reached[(start_i,start_j,tuple(tuple(row) for row in start_state))] = 0
    list_f = []
    while stack:
        parent = stack.pop()
        f = parent.G + Utility.count_dirty_cells(parent.STATE)
        if f > limit:
            continue
        move_list = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            energy = 2 if state_child[i_child][j_child] == 1 else 1
            g_child = parent.G + energy
            state_child[i_child][j_child] = 0
            h_child = Utility.count_dirty_cells(state_child)
            f_child = g_child + h_child
            if f_child > limit: list_f.append(f_child)
            child = Node(i_child, j_child, state_child, action, parent,g_child)
            if h_child == 0:
                return None,Utility.trace_path(child)
            key = (i_child, j_child,tuple(tuple(row) for row in state_child))
            if key not in reached or reached[key] > g_child:
                stack.append(child)
                reached[key] = g_child
    if len(list_f) == 0: return None,([],[])
    return min(list_f),([],[])
def IDA_sao(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0:
        return None,[start_state],[]
    limit = Utility.count_dirty_cells(start_state)
    while True:
        limit,temp = depth_limited_search(start_state,start_i,start_j,limit)
        path_states,actions = temp
        if limit == None:
            return path_states,actions



