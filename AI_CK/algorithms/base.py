from abc import ABC, abstractmethod


class BaseAlg(ABC):
    def __init__(self):
        self.logs = []

        # Terrain cost mapping (cell_value -> move cost)
        # 0: Tree (free), 1: No-Fly (impassable), 2: Building (high cost),
        # 3: Drone (start), 4: Warehouse, 5: House (goal)
        self.TERRAIN_COSTS = {
            0: 1,  # Tree / free
            2: 5,  # Building
            3: 1,  # Drone (start) treated as free
            4: 1,  # Warehouse
            5: 1,  # House / goal
        }
        self.IMPASSABLE = {1}

    def is_goal(self, dirt):
        return all(cell != 4 for row in dirt for cell in row)

    def actions(self, x, y, ground):
        action = []
        m, n = len(ground), len(ground[0])

        if (x > 0):
            if ground[x - 1][y] not in self.IMPASSABLE:
                action.append("UP")
        if (x < m - 1):
            if ground[x + 1][y] not in self.IMPASSABLE:
                action.append("DOWN")
        if (y > 0):
            if ground[x][y - 1] not in self.IMPASSABLE:
                action.append("LEFT")
        if (y < n - 1):
            if ground[x][y + 1] not in self.IMPASSABLE:
                action.append("RIGHT")
        if 0 <= x < m and 0 <= y < n:
            if (ground[x][y] == 4):
                action.append("CLEAN")
        return action

    def apply_action(self, state, action):
        x, y, dirt = state
        dirt = [list(row) for row in dirt]

        if (action == "UP"):
            x -= 1
        elif (action == "DOWN"):
            x += 1
        elif (action == "LEFT"):
            y -= 1
        elif (action == "RIGHT"):
            y += 1
        elif (action == "CLEAN"):
            dirt[x][y] = 0

        return (x, y, tuple(tuple(row) for row in dirt))

    def get_cost(self, state, action, new_state):
        """
        Return movement cost for applying `action` from `state` to `new_state`.
        Default: cost determined by destination cell value using TERRAIN_COSTS.
        """
        nx, ny = new_state[0], new_state[1]
        grid = new_state[2]
        try:
            cell = grid[nx][ny]
        except Exception:
            return 1
        return self.TERRAIN_COSTS.get(cell, 1)

    def min_move_cost(self):
        return min(self.TERRAIN_COSTS.values())

    @abstractmethod
    def solve(self, start_state):
        pass