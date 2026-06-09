import pygame
import sys
import time
import random
import re
from algorithms import ALG_MAP

# Configuration
GRID_SIZE = 20
PADDING = 15
FPS = 60

ASSET_PATH = "Assets/"


def load_assets(cell_size):
    def load(name):
        try:
            img = pygame.image.load(ASSET_PATH + name)
            return pygame.transform.scale(img, (cell_size, cell_size))
        except Exception:
            return None

    return {
        'building': load('Building.jpg'),
        'drone': load('Drone.jpg'),
        'house': load('house.jpg'),
        'nofly': load('Nofly.jpg'),
        'tree': load('Tree.png'),
        'warehouse': load('Warehouse.jpg'),
    }


def random_map(size, obstacle_prob=0.12, seed=None):
    """
    Terrain codes:
      0: Tree (free)
      1: No-Fly (impassable)
      2: Building (high cost)
      3: Drone (start) - placed exactly once
      4: Warehouse (goal) - placed exactly once
      5: House (customer) - can be multiple
    """
    if seed is not None:
        random.seed(seed)
    grid = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            r = random.random()
            if r < obstacle_prob * 0.5:
                grid[i][j] = 2  # building
            elif r < obstacle_prob * 0.8:
                grid[i][j] = 1  # no-fly (impassable)
            else:
                grid[i][j] = 0  # tree / free

    # Collect free cells (0)
    free_cells = [(i, j) for i in range(size) for j in range(size) if grid[i][j] == 0]
    
    if len(free_cells) < 6:
        # Not enough free cells, retry with lower obstacle prob
        return random_map(size, obstacle_prob=max(0.05, obstacle_prob * 0.8), seed=seed)
    
    # Shuffle and place: drone, warehouse, houses
    random.shuffle(free_cells)
    
    # place exactly one drone (3)
    dx, dy = free_cells[0]
    grid[dx][dy] = 3
    drone_pos = (dx, dy)

    # place exactly one warehouse (goal) (4)
    wx, wy = free_cells[1]
    grid[wx][wy] = 4
    warehouse_pos = (wx, wy)

    # place at least 2-3 houses (5)
    hcount = min(3, len(free_cells) - 2)
    for idx in range(2, 2 + hcount):
        hx, hy = free_cells[idx]
        grid[hx][hy] = 5

    return grid


def choose_algorithm(name):
    n = name.strip().lower()
    mapping = {
        "bfs": "BFS",
        "dfs": "DFS",
        "ucs": "UCS",
        "greedy": "Greedy",
        "astar": "A*",
        "a*": "A*",
        "ida": "IDA*",
    }
    key = mapping.get(n, None)
    if key is None:
        for k in ALG_MAP.keys():
            if k.lower() == name.lower():
                key = k
                break
    if key is None:
        raise ValueError(f"Unknown algorithm: {name}")
    return ALG_MAP[key]


def logs_to_visited(logs):
    coords = set()
    for line in logs:
        for match in re.findall(r"\((\d+),(\d+)\)", line):
            x, y = int(match[0]), int(match[1])
            coords.add((x, y))
    return coords


def compute_path_to_target(start, target, grid, algo):
    temp_grid = [list(row) for row in grid]
    # Ensure only the current target is marked as the goal
    for i in range(len(temp_grid)):
        for j in range(len(temp_grid[i])):
            if temp_grid[i][j] == 4:
                temp_grid[i][j] = 0
    tx, ty = target
    temp_grid[tx][ty] = 4

    start_state = (start[0], start[1], tuple(tuple(row) for row in temp_grid))
    t0 = time.time()
    result_path, logs = algo.solve(start_state)
    t1 = time.time()
    runtime_ms = int((t1 - t0) * 1000)
    visited = logs_to_visited(logs)
    if result_path is None:
        return [], 0, visited, runtime_ms

    positions = [(start[0], start[1])]
    s = start_state
    cost = 0
    for a in result_path:
        ns = algo.apply_action(s, a)
        cost += algo.get_cost(s, a, ns)
        positions.append((ns[0], ns[1]))
        s = ns
    return positions, cost, visited, runtime_ms


def main():
    pygame.init()
    
    # Get screen info for fullscreen
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    
    # Calculate layout: left panel + grid
    LEFT_PANEL = max(250, int(screen_width * 0.2))  # 20% for panel, min 250px
    GRID_WIDTH = screen_width - LEFT_PANEL - 3 * PADDING
    GRID_HEIGHT = screen_height - 2 * PADDING
    
    # Cell size based on available grid space
    CELL_SIZE = min(GRID_WIDTH // GRID_SIZE, GRID_HEIGHT // GRID_SIZE)
    
    # Create fullscreen window
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Drone Delivery Pathfinding Simulator")
    clock = pygame.time.Clock()
    assets = load_assets(CELL_SIZE)

    font_size = max(16, CELL_SIZE // 2)
    big_font_size = max(24, CELL_SIZE)
    font = pygame.font.SysFont(None, font_size)
    bigfont = pygame.font.SysFont(None, big_font_size)

    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
    # find drone (3) and warehouse (4)
    start = None
    goal = None
    houses = []  # Initialize houses early
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 3:
                start = (i, j)
            elif grid[i][j] == 4:
                goal = (i, j)
            elif grid[i][j] == 5:
                houses.append((i, j))
    
    if start is None:
        start = (0, 0)
        grid[start[0]][start[1]] = 3
    if goal is None:
        goal = (GRID_SIZE-1, GRID_SIZE-1)
        grid[goal[0]][goal[1]] = 4

    base = start
    selected_algo_name = 'A*'
    algo = choose_algorithm(selected_algo_name)

    path = []
    visited = set()
    total_cost = 0
    runtime_ms = 0

    running = True
    anim_index = 0
    anim_time = 0
    
    # Delivery state machine
    delivery_state = "IDLE"  # IDLE, PICKING, DELIVERING, RETURNING
    current_target = None  # (x, y) of current target
    delivery_log = []
    state_change_time = 0
    delivered_count = 0
    delivered_houses = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r:
                    grid = random_map(GRID_SIZE, obstacle_prob=0.12)
                    # find new start and goal
                    start = None
                    goal = None
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 3:
                                start = (i, j)
                            elif grid[i][j] == 4:
                                goal = (i, j)
                    if start is None:
                        start = (0,0)
                        grid[start[0]][start[1]] = 3
                    if goal is None:
                        goal = (GRID_SIZE-1, GRID_SIZE-1)
                        grid[goal[0]][goal[1]] = 4
                    base = start
                    delivered_houses = []
                    path = []
                    visited = set()
                    delivery_state = "IDLE"
                    delivery_log = []
                    delivered_count = 0
                    # Re-collect houses
                    houses = []
                    for i in range(GRID_SIZE):
                        for j in range(GRID_SIZE):
                            if grid[i][j] == 5:
                                houses.append((i, j))
                elif event.key == pygame.K_SPACE:
                    # Start delivery
                    if delivery_state == "IDLE":
                        start = base
                        delivery_state = "PICKING"
                        delivery_log = [f"[PICKING] Flying to Warehouse at ({goal[0]}, {goal[1]})"]
                        delivered_count = 0
                        current_target = goal  # warehouse position
                    
                    algo = choose_algorithm(selected_algo_name)
                    path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                    anim_index = 0
                    anim_time = pygame.time.get_ticks()
                    state_change_time = pygame.time.get_ticks()
                elif event.key == pygame.K_c:
                    # compare all algorithms
                    summaries = []
                    for name, instance in ALG_MAP.items():
                        start_state = (start[0], start[1], tuple(tuple(row) for row in grid))
                        t0 = time.time()
                        p, logs = instance.solve(start_state)
                        t1 = time.time()
                        visited_set = logs_to_visited(logs)
                        if p is None:
                            summaries.append((name, len(visited_set), 0, 0, int((t1 - t0)*1000)))
                        else:
                            # compute cost
                            s = start_state
                            c = 0
                            positions = [(s[0], s[1])]
                            for a in p:
                                ns = instance.apply_action(s, a)
                                c += instance.get_cost(s, a, ns)
                                positions.append((ns[0], ns[1]))
                                s = ns
                            summaries.append((name, len(visited_set), len(p), c, int((t1 - t0)*1000)))
                    # print summary to console and also show first lines on screen
                    print("COMPARE ALL RESULTS")
                    for row in summaries:
                        print(f"{row[0]:12} Nodes:{row[1]:4} PathLen:{row[2]:4} Cost:{row[3]:4} Time:{row[4]}ms")

                elif event.key == pygame.K_1:
                    selected_algo_name = 'BFS'
                elif event.key == pygame.K_2:
                    selected_algo_name = 'DFS'
                elif event.key == pygame.K_3:
                    selected_algo_name = 'UCS'
                elif event.key == pygame.K_4:
                    selected_algo_name = 'Greedy'
                elif event.key == pygame.K_5:
                    selected_algo_name = 'A*'

        screen.fill((30, 30, 30))
        
        # Handle delivery state transitions
        now = pygame.time.get_ticks()
        if path and delivery_state != "IDLE":
            # Check if animation finished
            step = (now - anim_time) // 150
            if step >= len(path):
                # Drone reached goal
                if delivery_state == "PICKING":
                    delivery_log.append(f"[PICKED UP] At Warehouse. Now delivering...")
                    if houses:
                        delivery_state = "DELIVERING"
                        current_target = houses[0]
                        delivery_log.append(f"[DELIVERING] Flying to House at ({current_target[0]}, {current_target[1]})")
                        state_change_time = now
                    else:
                        delivery_state = "IDLE"
                        delivery_log.append("[DONE] No houses to deliver")

                elif delivery_state == "DELIVERING":
                    delivered_count += 1
                    delivery_log.append(f"[DELIVERED] House #{delivered_count} at ({current_target[0]}, {current_target[1]})")
                    delivered_houses.append(current_target)
                    grid[current_target[0]][current_target[1]] = 0
                    houses.pop(0)
                    delivery_state = "RETURNING"
                    current_target = base
                    delivery_log.append(f"[RETURNING] Back to Drone Base at ({base[0]}, {base[1]})")
                    state_change_time = now

                elif delivery_state == "RETURNING":
                    if houses:
                        delivery_state = "PICKING"
                        current_target = goal
                        delivery_log.append(f"[PICKING] Flying to Warehouse at ({goal[0]}, {goal[1]})")
                        state_change_time = now
                    else:
                        delivery_state = "IDLE"
                        delivery_log.append("[DONE] All houses delivered!")

                # Update current drone position after arriving at the target
                start = path[-1]

                # Immediately plan the next leg when not idle
                if delivery_state != "IDLE":
                    algo = choose_algorithm(selected_algo_name)
                    path, total_cost, visited, runtime_ms = compute_path_to_target(start, current_target, grid, algo)
                    anim_time = now
                    state_change_time = now

        # Draw left panel
        panel_x = PADDING
        panel_y = PADDING
        pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, LEFT_PANEL - PADDING, GRID_SIZE * CELL_SIZE))

        screen.blit(bigfont.render('THUẬT TOÁN', True, (200, 200, 200)), (panel_x + 10, panel_y + 10))
        algs = ['BFS', 'DFS', 'UCS', 'Greedy', 'A*']
        for i, a in enumerate(algs):
            y = panel_y + 50 + i * (font_size + 5)
            color = (255, 255, 0) if a == selected_algo_name else (200, 200, 200)
            screen.blit(font.render(f"{i+1}. {a}", True, color), (panel_x + 16, y))

        # controls
        ctrl_y = panel_y + 220
        screen.blit(font.render('[SPACE] START', True, (200,200,200)), (panel_x + 10, ctrl_y))
        screen.blit(font.render('[R] RANDOM', True, (200,200,200)), (panel_x + 10, ctrl_y + font_size + 5))
        screen.blit(font.render('[C] COMPARE', True, (200,200,200)), (panel_x + 10, ctrl_y + 2*(font_size + 5)))
        screen.blit(font.render('[ESC] EXIT', True, (200,200,200)), (panel_x + 10, ctrl_y + 3*(font_size + 5)))

        # Draw grid
        grid_x0 = LEFT_PANEL + PADDING
        grid_y0 = PADDING
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = grid[i][j]
                rect = pygame.Rect(grid_x0 + j*CELL_SIZE, grid_y0 + i*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
                color = (240, 240, 240)
                if cell == 2:
                    color = (160, 160, 160)  # building
                elif cell == 1:
                    color = (120, 30, 30)    # no-fly
                elif cell == 4:
                    color = (255, 220, 100)  # warehouse (goal)
                elif cell == 5:
                    color = (220, 140, 80)   # house (customer)
                elif cell == 3:
                    color = (240, 240, 240)  # drone base
                elif cell == 0:
                    color = (180, 225, 180)  # tree
                pygame.draw.rect(screen, color, rect)

        # draw visited
        for (x, y) in visited:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (100, 200, 150), rect)

        # draw final path
        for (x, y) in path:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (230, 220, 100), rect)

        # draw delivered houses overlay
        for (x, y) in delivered_houses:
            rect = pygame.Rect(grid_x0 + y*CELL_SIZE, grid_y0 + x*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (120, 180, 255), rect)
            pygame.draw.circle(screen, (0, 80, 200), (grid_x0 + y*CELL_SIZE + CELL_SIZE//2, grid_y0 + x*CELL_SIZE + CELL_SIZE//2), max(2, CELL_SIZE//4))

        # highlight current delivery target
        if current_target is not None and delivery_state in ("DELIVERING", "PICKING", "RETURNING"):
            tx, ty = current_target
            rect = pygame.Rect(grid_x0 + ty*CELL_SIZE, grid_y0 + tx*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1)
            pygame.draw.rect(screen, (255, 140, 0), rect, 3)

# draw warehouse(s), house and buildings/nofly/tree icons where applicable
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                cell = grid[i][j]
                x = grid_x0 + j*CELL_SIZE
                y = grid_y0 + i*CELL_SIZE
                if cell == 4 and assets.get('warehouse'):
                    screen.blit(assets['warehouse'], (x, y))
                elif cell == 5 and assets.get('house'):
                    screen.blit(assets['house'], (x, y))
                elif cell == 2 and assets.get('building'):
                    screen.blit(assets['building'], (x, y))
                elif cell == 1 and assets.get('nofly'):
                    screen.blit(assets['nofly'], (x, y))
                elif cell == 0 and assets.get('tree'):
                    screen.blit(assets['tree'], (x, y))

        # draw drone (animated along path) or at start if no path
        if path:
            now = pygame.time.get_ticks()
            # one step per 150ms
            step = (now - anim_time) // 150
            if step < len(path):
                dx, dy = path[step]
                if assets.get('drone'):
                    screen.blit(assets['drone'], (grid_x0 + dy*CELL_SIZE, grid_y0 + dx*CELL_SIZE))
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + dy*CELL_SIZE + CELL_SIZE//2, grid_y0 + dx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)
        else:
            # draw drone at start if no path yet
            sx, sy = start
            if assets.get('drone'):
                screen.blit(assets['drone'], (grid_x0 + sy*CELL_SIZE, grid_y0 + sx*CELL_SIZE))
            else:
                pygame.draw.circle(screen, (255, 0, 0), (grid_x0 + sy*CELL_SIZE + CELL_SIZE//2, grid_y0 + sx*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//3)

        # Draw legend and statistics on left panel
        stats_y = panel_y + 330
        screen.blit(bigfont.render('THỐNG KÊ', True, (200,200,200)), (panel_x + 10, stats_y))
        screen.blit(font.render(f"Nodes Visited : {len(visited)}", True, (200,200,200)), (panel_x + 12, stats_y + 36))
        screen.blit(font.render(f"Path Length   : {max(0, len(path)-1)}", True, (200,200,200)), (panel_x + 12, stats_y + 56))
        screen.blit(font.render(f"Total Cost    : {total_cost}", True, (200,200,200)), (panel_x + 12, stats_y + 76))
        screen.blit(font.render(f"Delivered     : {len(delivered_houses)}", True, (200,200,200)), (panel_x + 12, stats_y + 96))
        screen.blit(font.render(f"Runtime       : {runtime_ms} ms", True, (200,200,200)), (panel_x + 12, stats_y + 116))
        
        # Draw delivery log
        log_y = stats_y + 160
        screen.blit(bigfont.render('LOG', True, (200,200,200)), (panel_x + 10, log_y))
        for i, log_line in enumerate(delivery_log[-5:]):  # Show last 5 lines
            log_color = (100, 200, 150) if "DELIVERED" in log_line else (200, 150, 100) if "PICKING" in log_line else (200, 200, 200)
            screen.blit(font.render(log_line[:30], True, log_color), (panel_x + 12, log_y + 36 + i*(font_size + 3)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
