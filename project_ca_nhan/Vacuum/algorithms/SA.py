import random
import copy 
import math
from algorithms import Utility


class Node():
    def __init__(self,i, j, state, action, parent, h):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent
        self.H = h

def SA(grid, start_i, start_j):
    T = 100
    T_min = 20
    anpha = 0.9
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    h_parent = Utility.count_dirty_cells(start_state)
    if h_parent == 0:
        return [start_state], []
    parent = Node(start_i,start_j,start_state,None,None,h_parent)
    while T > T_min:
        children = []
        move_list = Utility.get_actions(parent.i,parent.j,parent.STATE)
        for action in move_list:
            state_child = copy.deepcopy(parent.STATE)
            i_child, j_child = Utility.next_pos(parent.i,parent.j,action)
            state_child[i_child][j_child] = 0
            h_child = Utility.count_dirty_cells(state_child)
            child = Node(i_child,j_child,state_child,action,parent,h_child)
            if h_child == 0: return Utility.trace_path(child)
            children.append(child)
        if not children: 
            T *= anpha
            continue
        choice_child = random.choice(children)
        delta = choice_child.H - parent.H
        if delta < 0:
            parent = choice_child
        else:
            p = math.exp(-delta / T)
            if random.random() < p: parent = choice_child
        T *= anpha
    return [],[]


