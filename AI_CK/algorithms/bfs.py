from collections import deque
from .base import BaseAlg

class BFS(BaseAlg):
    def solve(self, start_state):
        queue = deque()
        queue.append((start_state, []))
        visited = set()
        visited.add(start_state)
        steps = 0
        logs = []
        while queue:
            state, path = queue.popleft()
            steps += 1
            logs.append(f"BFS Duyệt Node #{steps} | Vị trí: ({state[0]},{state[1]}) | Q-Size: {len(queue)}")
            if (self.is_goal(state[2])):
                return path, logs
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                if (new_state not in visited):
                    visited.add(new_state)
                    queue.append((new_state, path + [action]))

        return None, logs
