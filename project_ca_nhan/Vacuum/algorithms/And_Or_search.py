
from algorithms import Utility
import copy
import random

MAX_AND_OR_EXPANSIONS = 50000
MAX_AND_OR_DEPTH = 40
_and_or_expansions = 0

class Node:
    def __init__(self, i, j, state):
        self.i = i
        self.j = j
        self.STATE = state
def Or_Search(cur, path, depth=0):
    global _and_or_expansions
    if _and_or_expansions >= MAX_AND_OR_EXPANSIONS:
        return None
    _and_or_expansions += 1
    if depth > MAX_AND_OR_DEPTH:
        return None
    if Utility.count_dirty_cells(cur.STATE) == 0:
        return [cur.STATE], []
    key = (cur.i, cur.j, tuple(tuple(row) for row in cur.STATE))
    if key in path:
        return None
    move_list = Utility.get_actions(cur.i, cur.j, cur.STATE)
    for action in move_list:
        result = And_Search(cur, action, path | {key}, depth + 1)
        if result is not None:
            states, actions = result
            return [cur.STATE] + states, [action] + actions
    return None
def get_possible_outcomes(action, move_list): 
    result = [action]
    for a in move_list:
        if a != action and random.random() < 0.3:
            result.append(a)
    return result

def And_Search(cur, ACTION, path, depth=0):
    global _and_or_expansions
    if _and_or_expansions >= MAX_AND_OR_EXPANSIONS:
        return None
    _and_or_expansions += 1
    if depth > MAX_AND_OR_DEPTH:
        return None
    move_list = Utility.get_actions(cur.i, cur.j, cur.STATE)
    outcomes = get_possible_outcomes(ACTION, move_list)
    states = None
    actions = None
    for action in outcomes:
        i_child, j_child = Utility.next_pos(cur.i, cur.j, action)
        state_child = copy.deepcopy(cur.STATE)
        state_child[i_child][j_child] = 0
        child = Node(i_child, j_child, state_child)
        result = Or_Search(child, path, depth + 1)
        if result is None:
            return None
        states, actions = result
    return states, actions
def And_Or_Search(grid, start_i, start_j):
    global _and_or_expansions
    _and_or_expansions = 0
    start_state = copy.deepcopy(grid)
    start_state[start_i][start_j] = 0
    if Utility.count_dirty_cells(start_state) == 0:
        return [start_state], []
    parent = Node(start_i, start_j, start_state)
    result = Or_Search(parent, set())
    if result is None:
        return [], []
    return result 