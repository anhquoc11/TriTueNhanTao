from .base import BaseAlg

class IDAStar(BaseAlg):
    def solve(self, start_state):
        def count_dirt(state):
            dirt_count = 0
            grid = state[2]
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col] == 4:
                        dirt_count = dirt_count + 1
            return dirt_count

        algorithm_logs = []
        step_counter = 0

        def search(state, g_cost, path, current_path_states, threshold):
            nonlocal step_counter
            h_cost = count_dirt(state)
            f_cost = g_cost + h_cost
            if f_cost > threshold:
                return f_cost, None
            step_counter = step_counter + 1
            log_message = f"IDA* Duyệt Node #{step_counter} | Vị trí: ({state[0]},{state[1]}) | Cost G: {g_cost} | Ngưỡng: {threshold}"
            algorithm_logs.append(log_message)
            if self.is_goal(state[2]):
                return "FOUND", path
            min_threshold = float('inf')
            all_actions = self.actions(state[0], state[1], state[2])
            for action in all_actions:
                next_state = self.apply_action(state, action)
                if next_state in current_path_states:
                    continue
                next_g_cost = g_cost + 1
                next_path = path + [action]
                current_path_states.add(next_state)
                status, result = search(next_state, next_g_cost, next_path, current_path_states, threshold)
                if status == "FOUND":
                    return "FOUND", result
                current_path_states.remove(next_state)
                if status < min_threshold:
                    min_threshold = status
            return min_threshold, None
        threshold = count_dirt(start_state)
        while threshold != float('inf'):
            start_states_set = {start_state}
            status, result = search(start_state, 0, [], start_states_set, threshold)
            if status == "FOUND":
                return result, algorithm_logs
            if status == float('inf'):
                break
            threshold = status
            
        return None, algorithm_logs