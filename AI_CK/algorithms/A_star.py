from heapq import heappush, heappop
from .base import BaseAlg


class AStar(BaseAlg):
    def solve(self, start_state):
        def find_goal(grid):
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] == 4:
                        return (i, j)
            return None

        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        priority_queue = []
        step_counter = 0
        start_g_cost = 0
        grid = start_state[2]
        goal_pos = find_goal(grid)
        start_h_cost = 0 if goal_pos is None else manhattan((start_state[0], start_state[1]), goal_pos) * self.min_move_cost()
        start_f_cost = start_g_cost + start_h_cost
        heappush(priority_queue, (start_f_cost, start_g_cost, step_counter, start_state, []))
        visited_nodes = {}
        visited_nodes[start_state] = start_g_cost
        algorithm_logs = []

        while len(priority_queue) > 0:
            current_node = heappop(priority_queue)
            f_cost = current_node[0]
            g_cost = current_node[1]
            state = current_node[3]
            path = current_node[4]
            step_counter = step_counter + 1
            log_message = f"A* Duyệt Node #{step_counter} | Vị trí: ({state[0]},{state[1]}) | Cost G: {g_cost}"
            algorithm_logs.append(log_message)
            if self.is_goal(state[2]):
                algorithm_logs.append(f"-> A* THÀNH CÔNG tại Node #{step_counter} | Tổng chi phí G: {g_cost}")
                return path, algorithm_logs
            all_actions = self.actions(state[0], state[1], state[2])
            for action in all_actions:
                next_state = self.apply_action(state, action)
                step_cost = self.get_cost(state, action, next_state)
                next_g_cost = g_cost + step_cost
                if next_state not in visited_nodes or next_g_cost < visited_nodes[next_state]:
                    visited_nodes[next_state] = next_g_cost
                    next_h_cost = 0 if goal_pos is None else manhattan((next_state[0], next_state[1]), goal_pos) * self.min_move_cost()
                    next_f_cost = next_g_cost + next_h_cost
                    next_path = path + [action]
                    heappush(priority_queue, (next_f_cost, next_g_cost, step_counter, next_state, next_path))

        return None, algorithm_logs