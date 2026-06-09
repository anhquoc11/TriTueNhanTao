from collections import deque
from .base import BaseAlg

class IDS(BaseAlg):
    def solve(self, start_state):
        limit = 0
        step = 0
        logs = []
        MAX_DEPTH = 30 
        while limit <= MAX_DEPTH:
            logs.append(f"--- Bắt đầu tìm kiếm với Độ sâu Giới hạn: {limit} ---")
            status, path, step, logs = self.depth_limited_search(start_state, limit, step, logs)
            if status == "FOUND":
                return path, logs
            elif status == "NOT_FOUND":
                logs.append("Kết luận: Đã vét cạn mọi trạng thái có thể sinh ra | KHÔNG CÓ ĐƯỜNG ĐI!")
                return None, logs
            limit += 1
            
        logs.append(f"Dừng thuật toán vì đã vượt quá giới hạn an toàn {MAX_DEPTH} tầng.")
        return None, logs

    def depth_limited_search(self, start_state, limit, step, logs):
        stack = deque()
        start_node_key = (start_state[0], start_state[1], start_state[2])
        stack.append((start_state, [], 0, frozenset([start_node_key])))
        
        any_node_remaining = False
        
        while stack:
            state, path, current_depth, path_states = stack.pop()
            step += 1
            if step % 100 == 0 or current_depth == limit:
                logs.append(f"IDS Duyệt Node #{step} | Vị trí: ({state[0]},{state[1]}) | Tầng: {current_depth}/{limit}")
            if self.is_goal(state[2]):
                logs.append(f"-> THÀNH CÔNG TÌM THẤY ĐÍCH tại Node #{step}!")
                return "FOUND", path, step, logs
            if current_depth == limit:
                has_valid_child = False
                for action in self.actions(state[0], state[1], state[2]):
                    sub_state = self.apply_action(state, action)
                    sub_node_key = (sub_state[0], sub_state[1], sub_state[2])
                    if sub_node_key not in path_states:
                        has_valid_child = True
                        break
                if has_valid_child:
                    any_node_remaining = True
                continue
                
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                new_node_key = (new_state[0], new_state[1], new_state[2])
                if new_node_key not in path_states:
                    new_path_states = path_states | frozenset([new_node_key])
                    stack.append((new_state, path + [action], current_depth + 1, new_path_states))

        if any_node_remaining:
            return "REACHED_LIMIT", None, step, logs
        else:
            return "NOT_FOUND", None, step, logs