import os
import pygame
import random
import BFS as bfs
import DFS as dfs
import IDF as idf
import UCS as ucs
import IDA_sao as ida
import SA as sa
import Local_Beam_Search as local_beam
import Leo_Đồi_Đơn_Giản as hill_simple
import Leo_Đồi_Dốc_Nhất as hill_steep
import Leo_Đồi_Ngẫu_Nhiên as hill_random
import Leo_Đồi_Ngẫu_Nhiên_Có_Khởi_Tạo as hill_random_init

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum AI")

clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)
title_font = pygame.font.SysFont("consolas", 26, bold=True)

# ======================
# ASSET IMAGES
# ======================
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(name):
    path = os.path.join(ASSETS_DIR, name)
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception:
            return None
    return None

DIRT_IMG = load_image("dirt.jpg")
WALL_IMG = load_image("wall.jpg")
ROBOT_IMG = load_image("robot.jpg")

# ======================
# LAYOUT
# ======================
GRID_SIZE = 4
CELL = 100
GRID_X, GRID_Y = 50, 120
GRID_WIDTH = GRID_SIZE * CELL
GRID_HEIGHT = GRID_SIZE * CELL
LOG_X, LOG_Y = GRID_X + GRID_WIDTH + 50, GRID_Y
LOG_WIDTH = 500
LOG_HEIGHT = GRID_HEIGHT
BUTTON_Y = GRID_Y + GRID_HEIGHT + 20
BUTTON_HEIGHT = 45
BUTTON_WIDTH = 130
LOG_LINE_HEIGHT = 24
ALGO_BUTTON_Y = BUTTON_Y
ALGO_BUTTON_WIDTH = 100
ALGO_BUTTON_HEIGHT = 34
ALGO_BUTTON_MARGIN = 10
CONTROL_BUTTON_Y = ALGO_BUTTON_Y + ALGO_BUTTON_HEIGHT + 16

# ======================
# STATE
# ======================
path_states = []
actions = []
step = 0
running = False
status_text = "Ready"
log_entries = ["Ready to run algorithm simulation."]
scroll_offset = 0
auto_scroll = True
scroll_dragging = False
scroll_drag_y = 0
scroll_offset_start = 0
speed_delay = 18
speed_counter = 0

# ======================
# BUTTONS
# ======================
start_btn = pygame.Rect(50, CONTROL_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_btn = pygame.Rect(200, CONTROL_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
slower_btn = pygame.Rect(350, CONTROL_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
faster_btn = pygame.Rect(500, CONTROL_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
scroll_up_btn = pygame.Rect(LOG_X + LOG_WIDTH - 30, LOG_Y + 20, 20, 20)
scroll_down_btn = pygame.Rect(LOG_X + LOG_WIDTH - 30, LOG_Y + LOG_HEIGHT - 40, 20, 20)

ALGORITHM_NAMES = ["UCS", "BFS", "DFS", "IDF", "IDA_sao", "LD_ĐG", "LD_DN", "LD_NN", "LD_NN_KT", "SA", "LBS"]
# Combobox (placed under Event Log on the right, aligned with buttons)
COMBO_X = LOG_X + LOG_WIDTH - 182 - 12
COMBO_Y = CONTROL_BUTTON_Y
COMBO_WIDTH = 182  # reduced by about 1cm
COMBO_HEIGHT = ALGO_BUTTON_HEIGHT
selected_algorithm = "UCS"
# Dropdown state for the combobox
dropdown_open = False
dropdown_items = ALGORITHM_NAMES
DROP_ITEM_HEIGHT = 30
# Scrollable dropdown settings
DROP_VISIBLE = 5
dropdown_scroll = 0
def run_idf(grid, start_i, start_j):
    return idf.IDF(grid, start_i, start_j)

algorithms = {
    "UCS": ucs.UCS,
    "BFS": bfs.BFS,
    "DFS": dfs.DFS,
    "IDF": run_idf,
    "IDA_sao": ida.IDA_sao,
    "LD_ĐG": hill_simple.Leo_Đồi_Đơn_Giản,
    "LD_DN": hill_steep.Leo_Đồi_Dốc_Nhất,
    "LD_NN": hill_random.Leo_Đồi_Ngẫu_Nhiên,
    "LD_NN_KT": hill_random_init.Leo_Đồi_Ngẫu_Nhiên_Có_Khởi_Tạo,
    "SA": sa.LA,
    "LBS": local_beam.Local_Beam_Search,
}
# ======================
# GRID / ROBOT
# ======================
def generate_grid():
    grid = []
    for i in range(GRID_SIZE):
        row = []
        for j in range(GRID_SIZE):
            row.append(random.choice([0, 1]))
        grid.append(row)

    for _ in range(2):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        grid[x][y] = 2

    return grid


grid = generate_grid()
robot_i = random.randint(0, GRID_SIZE - 1)
robot_j = random.randint(0, GRID_SIZE - 1)
while grid[robot_i][robot_j] == 2:
    robot_i = random.randint(0, GRID_SIZE - 1)
    robot_j = random.randint(0, GRID_SIZE - 1)

# ======================
# HELPERS
# ======================
def draw_button(rect, text, mouse_pos, selected=False):
    if selected:
        color = (100, 180, 100)
    else:
        color = (120, 120, 120) if rect.collidepoint(mouse_pos) else (90, 90, 90)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (rect.x + 10, rect.y + 12))


def draw_text(text, x, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))


def move_robot(i, j, action):
    if action == "UP":
        return i - 1, j
    if action == "DOWN":
        return i + 1, j
    if action == "LEFT":
        return i, j - 1
    if action == "RIGHT":
        return i, j + 1
    return i, j


def append_log(message):
    global scroll_offset, auto_scroll
    log_entries.append(message)
    auto_scroll = True
    visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
    if len(log_entries) > visible_lines:
        scroll_offset = len(log_entries) - visible_lines


def clamp_scroll():
    global scroll_offset
    visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
    scroll_offset = max(0, min(scroll_offset, max(0, len(log_entries) - visible_lines)))


def get_scroll_thumb_rect():
    visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
    if len(log_entries) <= visible_lines:
        return None
    track_height = LOG_HEIGHT - 56
    thumb_height = max(40, int(track_height * visible_lines / len(log_entries)))
    max_scroll = max(1, len(log_entries) - visible_lines)
    thumb_y = LOG_Y + 22 + int((track_height - thumb_height) * scroll_offset / max_scroll)
    return pygame.Rect(LOG_X + LOG_WIDTH - 24, thumb_y, 12, thumb_height)


def draw_log_area():
    global scroll_offset
    pygame.draw.rect(screen, (45, 45, 45), (LOG_X, LOG_Y, LOG_WIDTH, LOG_HEIGHT), border_radius=14)
    pygame.draw.rect(screen, (60, 60, 60), (LOG_X + LOG_WIDTH - 28, LOG_Y + 20, 20, LOG_HEIGHT - 40), border_radius=10)
    pygame.draw.rect(screen, (120, 120, 120), scroll_up_btn, border_radius=4)
    pygame.draw.polygon(screen, (255, 255, 255), [
        (scroll_up_btn.x + 10, scroll_up_btn.y + 6),
        (scroll_up_btn.x + 4, scroll_up_btn.y + 14),
        (scroll_up_btn.x + 16, scroll_up_btn.y + 14),
    ])
    pygame.draw.rect(screen, (120, 120, 120), scroll_down_btn, border_radius=4)
    pygame.draw.polygon(screen, (255, 255, 255), [
        (scroll_down_btn.x + 4, scroll_down_btn.y + 6),
        (scroll_down_btn.x + 16, scroll_down_btn.y + 6),
        (scroll_down_btn.x + 10, scroll_down_btn.y + 14),
    ])

    visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
    if auto_scroll:
        scroll_offset = max(0, len(log_entries) - visible_lines)
    clamp_scroll()

    line_y = LOG_Y + 20
    draw_text("Log", LOG_X + 12, line_y, (220, 220, 220))
    line_y += 32
    for line in log_entries[scroll_offset:scroll_offset + visible_lines]:
        draw_text(line, LOG_X + 12, line_y, (200, 200, 200))
        line_y += LOG_LINE_HEIGHT

    thumb_rect = get_scroll_thumb_rect()
    if thumb_rect:
        pygame.draw.rect(screen, (200, 200, 200), thumb_rect, border_radius=6)

# ======================
# MAIN LOOP
# ======================
running_app = True
while running_app:
    screen.fill((20, 20, 20))
    mouse = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running_app = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            pos = e.pos
            if e.button == 1:
                # Combobox header click (under Event Log)
                header_rect = pygame.Rect(COMBO_X, COMBO_Y, COMBO_WIDTH, COMBO_HEIGHT)
                if header_rect.collidepoint(pos):
                    dropdown_open = not dropdown_open
                    continue
                # If dropdown is open, check for selection clicks (items appear below header)
                if dropdown_open:
                    total_items = len(dropdown_items)
                    visible_count = min(DROP_VISIBLE, total_items)
                    items_start_y = COMBO_Y + COMBO_HEIGHT
                    clicked_item = False
                    for i in range(visible_count):
                        item_index = dropdown_scroll + i
                        if item_index >= total_items:
                            break
                        name = dropdown_items[item_index]
                        item_rect = pygame.Rect(COMBO_X, items_start_y + i * DROP_ITEM_HEIGHT, COMBO_WIDTH, DROP_ITEM_HEIGHT)
                        if item_rect.collidepoint(pos):
                            selected_algorithm = name
                            status_text = f"Selected {selected_algorithm}"
                            append_log(f"Selected algorithm: {selected_algorithm}")
                            dropdown_open = False
                            clicked_item = True
                            break
                    if clicked_item:
                        continue
                    # Click outside dropdown closes it
                    dropdown_area = pygame.Rect(COMBO_X, COMBO_Y, COMBO_WIDTH, COMBO_HEIGHT + visible_count * DROP_ITEM_HEIGHT)
                    if not dropdown_area.collidepoint(pos):
                        dropdown_open = False
                if start_btn.collidepoint(pos):
                    algorithm_fn = algorithms.get(selected_algorithm)
                    if algorithm_fn is None:
                        path_states, actions = [], []
                    else:
                        try:
                            path_states, actions = algorithm_fn(grid, robot_i, robot_j)
                        except TypeError:
                            path_states, actions = [], []
                    step = 0
                    if path_states:
                        running = True
                        status_text = f"Running {selected_algorithm}..."
                        append_log(f"Start at ({robot_i}, {robot_j}) using {selected_algorithm}")
                        append_log(f"Found path with {len(actions)} actions")
                    else:
                        running = False
                        status_text = "No valid path found"
                        append_log(f"No valid path found using {selected_algorithm}")
                elif reset_btn.collidepoint(pos):
                    grid = generate_grid()
                    robot_i = random.randint(0, GRID_SIZE - 1)
                    robot_j = random.randint(0, GRID_SIZE - 1)
                    while grid[robot_i][robot_j] == 2:
                        robot_i = random.randint(0, GRID_SIZE - 1)
                        robot_j = random.randint(0, GRID_SIZE - 1)
                    step = 0
                    path_states = []
                    actions = []
                    running = False
                    status_text = "Ready"
                    append_log("Grid reset and robot repositioned.")
                elif slower_btn.collidepoint(pos):
                    speed_delay = min(40, speed_delay + 4)
                    append_log(f"Speed slower: delay={speed_delay}")
                elif faster_btn.collidepoint(pos):
                    speed_delay = max(4, speed_delay - 4)
                    append_log(f"Speed faster: delay={speed_delay}")
                elif scroll_up_btn.collidepoint(pos):
                    auto_scroll = False
                    scroll_offset -= 1
                    clamp_scroll()
                elif scroll_down_btn.collidepoint(pos):
                    auto_scroll = False
                    scroll_offset += 1
                    clamp_scroll()
                else:
                    thumb_rect = get_scroll_thumb_rect()
                    scroll_bar_rect = pygame.Rect(LOG_X + LOG_WIDTH - 28, LOG_Y + 20, 20, LOG_HEIGHT - 40)
                    if scroll_bar_rect.collidepoint(pos):
                        if thumb_rect and thumb_rect.collidepoint(pos):
                            scroll_dragging = True
                            scroll_drag_y = pos[1]
                            scroll_offset_start = scroll_offset
                            auto_scroll = False
                        elif thumb_rect:
                            auto_scroll = False
                            track_height = LOG_HEIGHT - 56
                            visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
                            max_scroll = max(1, len(log_entries) - visible_lines)
                            relative_y = pos[1] - (LOG_Y + 22) - thumb_rect.height // 2
                            scroll_offset = int(relative_y * max_scroll / max(1, track_height - thumb_rect.height))
                            clamp_scroll()
                    else:
                        # nothing here (algorithm list moved to combobox on right)
                        pass
            elif e.button == 4:
                auto_scroll = False
                scroll_offset -= 1
                clamp_scroll()
            elif e.button == 5:
                auto_scroll = False
                scroll_offset += 1
                clamp_scroll()
        elif e.type == pygame.MOUSEMOTION:
            if scroll_dragging:
                pos = e.pos
                thumb_rect = get_scroll_thumb_rect()
                if thumb_rect:
                    track_height = LOG_HEIGHT - 56
                    visible_lines = (LOG_HEIGHT - 40) // LOG_LINE_HEIGHT
                    max_scroll = max(1, len(log_entries) - visible_lines)
                    delta = pos[1] - scroll_drag_y
                    scroll_offset = scroll_offset_start + int(delta * max_scroll / max(1, track_height - thumb_rect.height))
                    clamp_scroll()
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                scroll_dragging = False
        elif e.type == pygame.MOUSEWHEEL:
            # If dropdown open and mouse is over the combobox area, scroll the dropdown
            if dropdown_open:
                total_items = len(dropdown_items)
                visible_count = min(DROP_VISIBLE, total_items)
                items_start_y = COMBO_Y + COMBO_HEIGHT
                dropdown_area = pygame.Rect(COMBO_X, COMBO_Y, COMBO_WIDTH + 20, COMBO_HEIGHT + visible_count * DROP_ITEM_HEIGHT)
                if dropdown_area.collidepoint(pygame.mouse.get_pos()):
                    dropdown_scroll = max(0, min(dropdown_scroll - e.y, max(0, total_items - visible_count)))
                else:
                    scroll_offset -= e.y
                    auto_scroll = False
                    clamp_scroll()
            else:
                scroll_offset -= e.y
                auto_scroll = False
                clamp_scroll()

    if running:
        speed_counter += 1
        if speed_counter >= speed_delay:
            speed_counter = 0
            if step < len(path_states) - 1:
                step += 1
                if step <= len(actions):
                    action = actions[step - 1]
                    robot_i, robot_j = move_robot(robot_i, robot_j, action)
                    append_log(f"Step {step}: {action}")
            else:
                running = False
                status_text = "Completed"
                append_log("Simulation completed.")

    pygame.draw.rect(screen, (40, 40, 40), (GRID_X - 10, GRID_Y - 10, GRID_WIDTH + 20, GRID_HEIGHT + 20), border_radius=18)
    current = path_states[step] if path_states else grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            val = current[i][j]
            cell_rect = pygame.Rect(GRID_X + j * CELL, GRID_Y + i * CELL, CELL - 8, CELL - 8)
            if val == 1 and DIRT_IMG:
                dirt_img = pygame.transform.smoothscale(DIRT_IMG, (CELL - 8, CELL - 8))
                screen.blit(dirt_img, cell_rect.topleft)
            elif val == 2 and WALL_IMG:
                wall_img = pygame.transform.smoothscale(WALL_IMG, (CELL - 8, CELL - 8))
                screen.blit(wall_img, cell_rect.topleft)
            else:
                color = (240, 240, 240) if val == 0 else (200, 200, 0)
                pygame.draw.rect(screen, color, cell_rect, border_radius=10)
            pygame.draw.rect(screen, (30, 30, 30), cell_rect, 2, border_radius=10)

    if ROBOT_IMG:
        robot_img = pygame.transform.smoothscale(ROBOT_IMG, (50, 50))
        robot_pos = (GRID_X + robot_j * CELL + CELL // 2 - 25, GRID_Y + robot_i * CELL + CELL // 2 - 25)
        screen.blit(robot_img, robot_pos)
    else:
        pygame.draw.circle(screen, (0, 200, 255), (GRID_X + robot_j * CELL + CELL // 2, GRID_Y + robot_i * CELL + CELL // 2), 22)
        pygame.draw.circle(screen, (20, 20, 20), (GRID_X + robot_j * CELL + CELL // 2, GRID_Y + robot_i * CELL + CELL // 2), 10)

    draw_log_area()
    # Draw combobox label and control under Event Log (right side)
    draw_text("Algorithm:", COMBO_X, COMBO_Y - 24)
    # Combobox header
    header_rect = pygame.Rect(COMBO_X, COMBO_Y, COMBO_WIDTH, COMBO_HEIGHT)
    header_color = (120, 120, 120)
    pygame.draw.rect(screen, header_color, header_rect, border_radius=6)
    header_label = font.render(selected_algorithm if selected_algorithm else "Chọn...", True, (255, 255, 255))
    screen.blit(header_label, (header_rect.x + 8, header_rect.y + (COMBO_HEIGHT - header_label.get_height()) // 2))
    # caret
    pygame.draw.polygon(screen, (255,255,255), [(header_rect.right - 18, header_rect.y + 12), (header_rect.right - 10, header_rect.y + 12), (header_rect.right - 14, header_rect.y + 18)])
    # Dropdown items (appear below header)
    if dropdown_open:
        total_items = len(dropdown_items)
        visible_count = min(DROP_VISIBLE, total_items)
        items_start_y = COMBO_Y + COMBO_HEIGHT
        box_h = visible_count * DROP_ITEM_HEIGHT
        pygame.draw.rect(screen, (40,40,40), (COMBO_X - 4, items_start_y - 4, COMBO_WIDTH + 28, box_h + 8), border_radius=6)
        # draw items (only visible slice)
        for i in range(visible_count):
            item_index = dropdown_scroll + i
            if item_index >= total_items:
                break
            name = dropdown_items[item_index]
            item_rect = pygame.Rect(COMBO_X, items_start_y + i * DROP_ITEM_HEIGHT, COMBO_WIDTH, DROP_ITEM_HEIGHT)
            hovered = item_rect.collidepoint(mouse)
            color = (140,140,140) if hovered else (100,100,100)
            pygame.draw.rect(screen, color, item_rect)
            label = font.render(name, True, (255,255,255))
            screen.blit(label, (item_rect.x + 8, item_rect.y + (DROP_ITEM_HEIGHT - label.get_height()) // 2))
        # draw scrollbar on the right of dropdown
        if total_items > visible_count:
            track_x = COMBO_X + COMBO_WIDTH + 8
            track_y = items_start_y
            track_h = box_h
            pygame.draw.rect(screen, (60,60,60), (track_x, track_y, 12, track_h), border_radius=6)
            thumb_h = max(20, int(track_h * visible_count / total_items))
            max_scroll = total_items - visible_count
            thumb_y = track_y + int((track_h - thumb_h) * (dropdown_scroll / max_scroll)) if max_scroll>0 else track_y
            pygame.draw.rect(screen, (180,180,180), (track_x+2, thumb_y, 8, thumb_h), border_radius=4)

    # (old duplicate dropdown removed)

    draw_button(start_btn, "START", mouse)
    draw_button(reset_btn, "RESET", mouse)
    draw_button(slower_btn, "SLOWER", mouse)
    draw_button(faster_btn, "FASTER", mouse)

    screen.blit(title_font.render("Vacuum Grid", True, (255, 255, 255)), (GRID_X, GRID_Y - 60))
    screen.blit(title_font.render("Event Log", True, (255, 255, 255)), (LOG_X, LOG_Y - 60))
    draw_text(f"Status: {status_text}", GRID_X, CONTROL_BUTTON_Y + BUTTON_HEIGHT + 10)
    display_step = step
    draw_text(f"Step: {display_step}/{len(actions)}", GRID_X, CONTROL_BUTTON_Y + BUTTON_HEIGHT + 35)
    draw_text(f"Speed delay: {speed_delay}", GRID_X + 220, CONTROL_BUTTON_Y + BUTTON_HEIGHT + 10)
    draw_text(f"Action: {actions[step-1] if actions and step > 0 else 'N/A'}", GRID_X + 220, CONTROL_BUTTON_Y + BUTTON_HEIGHT + 35)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
