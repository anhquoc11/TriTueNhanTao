
from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent, g, f):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.G = g
        self.F = f

def A_sao(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0

    if Utility.count_dirty_cells(start_state) == 0:
        return [start_state], []

    reached = {}
    start_node = Node(start_i, start_j, start_state, None, None, 0, Utility.count_dirty_cells(start_state))
    queue_priority = [start_node]
    reached[(start_i, start_j, tuple(tuple(row) for row in start_state))] = 0

    end = None
    while queue_priority:
        parent = queue_priority.pop(0)
        if Utility.count_dirty_cells(parent.STATE) == 0:
            end = parent
            break
        move_list = Utility.get_actions(parent.i, parent.j, parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i, parent.j, action)
            energy = 2 if state_child[i_child][j_child] == 1 else 1
            g_child = parent.G + energy
            state_child[i_child][j_child] = 0
            child = Node(i_child, j_child, state_child, action, parent, g_child, Utility.count_dirty_cells(state_child) + g_child)
            key = (i_child, j_child,tuple(tuple(row) for row in state_child))
            if key not in reached or g_child < reached[key]:
                queue_priority = Utility.queue_priority_add(queue_priority, child)
                reached[key] = g_child
    return Utility.trace_path(end)




