import heapq
from .base import BaseAlg

class UCS(BaseAlg):
    def solve(self, start_state):
        step = 0
        logs = []
        priority_queue = []
        start_node_key = (start_state[0], start_state[1], start_state[2])
        heapq.heappush(priority_queue, (0, step, start_state, [], frozenset([start_node_key])))
        while priority_queue:
            cost, _, state, path, path_states = heapq.heappop(priority_queue)
            step += 1
            if step % 100 == 0 or step <= 10:
                logs.append(f"UCS Duyệt Node #{step} | Vị trí: ({state[0]},{state[1]}) | Chi phí tích lũy: {cost}")
            if self.is_goal(state[2]):
                logs.append(f"-> UCS THÀNH CÔNG TÌM THẤY ĐƯỜNG TỐI ƯU tại Node #{step}! Tổng chi phí: {cost}")
                return path, logs

            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                new_node_key = (new_state[0], new_state[1], new_state[2])
                if new_node_key not in path_states:
                    step_cost = self.get_cost(state, action, new_state) if hasattr(self, 'get_cost') else 1
                    new_cost = cost + step_cost
                    new_path_states = path_states | frozenset([new_node_key])
                    heapq.heappush(priority_queue, (new_cost, step, new_state, path + [action], new_path_states))
                    
        logs.append("Kết luận: Đã duyệt hết không gian trạng thái | KHÔNG CÓ ĐƯỜNG ĐI!")
        return None, logs