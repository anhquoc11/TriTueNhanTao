from algorithms import Utility
import copy 
 
class Node():
    def __init__(self,i, j, state, action, parent, g):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.G = g
def UCS(grid, start_i, start_j):
    queue_priority = []
    reached = {}
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0: 
        return [start_state],[]
    queue_priority.append(Node(start_i,start_j,start_state,None,None,0))
    reached[(start_i, start_j, tuple(tuple(row) for row in start_state))] = 0

    while queue_priority:
        parent = queue_priority.pop(0)
        if Utility.count_dirty_cells(parent.STATE) == 0:
                return Utility.trace_path(parent)
        move_list = Utility.get_actions(parent.i,parent.j,parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child , j_child = Utility.next_pos(parent.i,parent.j,action)
            if state_child[i_child][j_child] == 1: g_child = 2
            else : g_child = 1
            state_child[i_child][j_child] = 0
            child = Node(i_child,j_child,state_child,action,parent,parent.G + g_child)
            key = (i_child,j_child,tuple(tuple(row) for row in state_child))
            if key not in reached or child.G < reached[key]:
                queue_priority = Utility.queue_priority_add_UCS(queue_priority,child)
                reached[key] = child.G
    return [],[]