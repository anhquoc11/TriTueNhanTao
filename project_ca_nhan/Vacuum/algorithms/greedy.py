from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent, h):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.H = h

def greedy(grid, start_i, start_j):
    queue_priority = []
    reached = {}
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0:
        return [start_state], []
    queue_priority = Utility.queue_priority_add_greedy(queue_priority,Node(start_i,start_j,start_state,None,None,0))
    reached[(start_i,start_j, tuple(tuple(row) for row in start_state))] = Utility.count_dirty_cells(start_state)
    end = None
    while queue_priority:
        parent = queue_priority.pop(0)
        if Utility.count_dirty_cells(parent.STATE) == 0:
            end = parent
            break
        move_list = Utility.get_actions(parent.i,parent.j,parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child , j_child = Utility.next_pos(parent.i,parent.j,action)
            state_child[i_child][j_child] = 0
            h = Utility.count_dirty_cells(state_child)
            child = Node(i_child,j_child,state_child,action,parent,h)
            key = (i_child, j_child,tuple(tuple(row) for row in state_child))
            if key not in reached or reached[key] > h:
                queue_priority = Utility.queue_priority_add_greedy(queue_priority,child)
                reached[key] = h
    return Utility.trace_path(end)