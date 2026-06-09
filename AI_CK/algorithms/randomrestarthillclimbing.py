from .base import BaseAlg
import random

class RandomRestartHillClimbing(BaseAlg):
    def solve(self, start_state):
        def count_dirt(state):
            return sum(row.count(4) for row in state[2])
        MAX_RESTART = 30
        algorithm_logs = []
        step_counter = 0
        grid_m = len(start_state[2])
        grid_n = len(start_state[2][0])
        for i in range(1, MAX_RESTART + 1):
            algorithm_logs.append(f"--- RESTART {i} ---")
            if i == 1:
                current_state = start_state
            else:
                while True:
                    rx = random.randint(0, grid_m - 1)
                    ry = random.randint(0, grid_n - 1)
                    if start_state[2][rx][ry] != 2:
                        current_state = (rx, ry, current_state[2])
                        break
            path = []
            visited = set()
            while True:
                step_counter += 1
                current_h = count_dirt(current_state)
                algorithm_logs.append(f"Step {step_counter} | Pos: ({current_state[0]},{current_state[1]}) | H: {current_h}")
                if self.is_goal(current_state[2]):
                    return path, algorithm_logs
                visited.add((current_state[0], current_state[1]))
                all_actions = self.actions(current_state[0], current_state[1], current_state[2])
                if "CLEAN" in all_actions:
                    current_state = self.apply_action(current_state, "CLEAN")
                    path.append("CLEAN")
                    continue
                better_neighbors = []
                for action in all_actions:
                    next_state = self.apply_action(current_state, action)
                    next_h = count_dirt(next_state)
                    if next_h <= current_h and (next_state[0], next_state[1]) not in visited:
                        better_neighbors.append((next_state, action, next_h))
                if not better_neighbors:
                    break
                else:
                    min_h = min(better_neighbors, key=lambda x: x[2])[2]
                    best_candidates = [n for n in better_neighbors if n[2] == min_h]
                    chosen_neighbor = random.choice(best_candidates)
                    current_state = chosen_neighbor[0]
                    path.append(chosen_neighbor[1])

        return None, algorithm_logs