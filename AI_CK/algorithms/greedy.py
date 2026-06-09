from heapq import heappush, heappop
from .base import BaseAlg

class Greedy(BaseAlg):
    def solve(self, start_state):
        def get_current_cost(state):
            count = 0
            current_board = state[2]
            for i in range(len(current_board)):
                for j in range(len(current_board[0])):
                    if current_board[i][j] == 4:
                        count += 1
            return count

        pq = []
        steps = 0
        start_cost = get_current_cost(start_state)
        heappush(pq, (start_cost, steps, start_state, []))
        visited = set()
        visited.add(start_state)
        logs = []
        while pq:
            accumulated_cost, _, state, path = heappop(pq)
            steps += 1
            logs.append(f"Greedy Duyệt Node #{steps} | Vị trí: ({state[0]},{state[1]}) | Cost: {accumulated_cost}")
            if self.is_goal(state[2]):
                return path, logs
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                if new_state not in visited:
                    visited.add(new_state)
                    next_cost = accumulated_cost + get_current_cost(new_state)
                    heappush(pq, (next_cost, steps, new_state, path + [action]))

        return None, logs