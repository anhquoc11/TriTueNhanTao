import copy
import random
from algorithms import Utility

def Random_Restart_Hill_Climbing(grid, start_i, start_j):
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0:
        return [start_state], []
    i = 0 
    while i < 20:
        state_parent = start_state
        i_parent, j_parent = start_i, start_j
        path_states = [state_parent]
        actions = []
        h_parent = Utility.count_dirty_cells(start_state)
        while True:
            children = []
            move_list = Utility.get_actions(i_parent,j_parent,state_parent)
            for action in move_list:
                i_child, j_child = Utility.next_pos(i_parent, j_parent, action)
                state_child = copy.deepcopy(state_parent)
                state_child[i_child][j_child] = 0 
                h_child = Utility.count_dirty_cells(state_child)
                if h_child < h_parent:
                    children.append([i_child,j_child,state_child,h_child,action])
            if not children: break
            choice_child = random.choice(children)
            h_parent = choice_child[3]
            state_parent = choice_child[2]
            i_parent,j_parent = choice_child[0],choice_child[1]
            path_states.append(state_parent)
            actions.append(choice_child[4])
            if h_parent == 0: return path_states, actions
        i+=1
    return [], []
