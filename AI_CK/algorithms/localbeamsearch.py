from .base import BaseAlg

class LocalBeamSearch(BaseAlg):
    def __init__(self, k=3):
        super().__init__()
        self.k = k

    def solve(self, start_state):
        current_beam = [(start_state, [])]
        algorithm_logs = []
        step_counter = 0
        max_steps = 100
        while step_counter < max_steps:
            step_counter += 1
            candidates = []
            for state, path in current_beam:
                if self.is_goal(state[2]):
                    return path, algorithm_logs
                for action in self.actions(state[0], state[1], state[2]):
                    next_state = self.apply_action(state, action)
                    new_path = path + [action]
                    candidates.append((next_state, new_path))
            if not candidates:
                break
            candidates.sort(key=lambda item: self.count_dirt(item[0]))
            current_beam = candidates[:self.k]
            best_h = self.count_dirt(current_beam[0][0])
            algorithm_logs.append(f"Bước {step_counter} | Best H: {best_h}")
            if best_h == 0:
                continue
                
        return None, algorithm_logs

    def count_dirt(self, state):
        return sum(row.count(1) for row in state[2])