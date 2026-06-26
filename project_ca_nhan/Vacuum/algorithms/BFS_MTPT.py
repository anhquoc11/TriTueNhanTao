
from algorithms import Utility
import copy 

class Node():
    def __init__(self,i, j, state, action, parent):
        self.i = i
        self.j = j
        self.STATE = state
        self.ACTION = action
        self.PARENT = parent

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
    if Utility.count_dirty_cells(A) == 0: return [A],[]
    if Utility.count_dirty_cells(B) == 0: return [B],[]
    queue = []
    queue.append(Node(i_A,j_A,A,None,None))
    queue.append(Node(i_B,j_B,B,None,None))
    reached = set()
    for x in queue: reached.add((x.i,x.j,tuple(tuple(row) for row in x.STATE)))
    end = None
    while queue:
        parent = queue.pop(0)
        moves = Utility.get_actions(parent.i,parent.j,parent.STATE)
        for action in moves:
            state_child =  copy.deepcopy(parent.STATE)
            i_child,j_child = Utility.next_pos(parent.i,parent.j,action)
            state_child[i_child][j_child] = 0
            key = (i_child,j_child,tuple(tuple(row) for row in state_child))
            child = Node(i_child,j_child,state_child,action,parent)
            if Utility.count_dirty_cells(state_child) == 0:
                end = child
                break
            if key not in reached:
                queue.append(child)
                reached.add(key)
        if end is not None: break
    return Utility.trace_path(end)