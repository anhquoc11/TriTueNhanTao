from .base import BaseAlg

class SimpleHillClimbing(BaseAlg):
    def solve(self, start_state):
        def count_dirt(state):
            dirt_count = 0
            grid = state[2]
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col] == 4:
                        dirt_count = dirt_count + 1
            return dirt_count

        current_state = start_state
        path = []
        algorithm_logs = []
        step_counter = 0

        while True:
            step_counter = step_counter + 1
            current_h = count_dirt(current_state)
            log_message = f"SimpleHC Duyệt Node #{step_counter} | Vị trí: ({current_state[0]},{current_state[1]}) | H: {current_h}"
            algorithm_logs.append(log_message)
            if self.is_goal(current_state[2]):
                return path, algorithm_logs
            all_actions = self.actions(current_state[0], current_state[1], current_state[2])
            neighbor_moved = False

            for action in all_actions:
                next_state = self.apply_action(current_state, action)
                next_h = count_dirt(next_state)
                if next_h < current_h: 
                    current_state = next_state
                    path.append(action)
                    neighbor_moved = True
                    break 
            if not neighbor_moved:
                break

        return None, algorithm_logs