from collections import deque
from .base import BaseAlg

class DFS_EARLY(BaseAlg):
    def solve(self, start_state):
        stack = [(start_state, [])]
        visited = set()
        steps = 0
        logs = []
        if self.is_goal(start_state[2]):
            logs.append("Early Goal detected tại node gốc!")
            return [], logs
        while stack:
            state, path = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            steps += 1
            logs.append(f"DFS Early Duyệt Node #{steps} | Vị trí: ({state[0]},{state[1]}) | Stack: {len(stack)}")
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                if new_state not in visited:
                    if self.is_goal(new_state[2]):
                        logs.append("Early Goal detected!")
                        return path + [action], logs
                    stack.append((new_state, path + [action]))
        return None, logs