from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent,cost):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.COST = cost
def depth_limited_search(grid, start_i, start_j, depth_limit):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0:
        return [start_state], []
    stack = []
    reached =  set()
    stack.append(Node(start_i, start_j, start_state, None, None,0))
    reached.add((start_i, start_j, tuple(tuple(row) for row in start_state)))
    end = None
    while stack:
        parent = stack.pop()
        if parent.COST >= depth_limit:
            continue

        move_list = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            state_child[i_child][j_child] = 0
            child = Node(i_child, j_child, state_child, action, parent, parent.COST + 1)
            if Utility.count_dirty_cells(state_child) == 0:
                end = child 
                break
            key = (i_child, j_child,tuple(tuple(row) for row in state_child))
            if key not in reached:
                stack.append(child)
                reached.add(key)
        if end is not None: break 
    return Utility.trace_path(end)


def IDF(grid, start_i, start_j):
    max_depth = 30
    for depth in range(max_depth + 1):
        path_states, actions = depth_limited_search(grid, start_i, start_j, depth)
        if len(path_states) != 0:
            return path_states, actions
    return [],[]

    


