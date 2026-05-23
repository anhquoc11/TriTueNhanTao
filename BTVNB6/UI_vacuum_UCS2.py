
import pygame
import time
import vacuum_UCS2 as backend

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vacuum AI")

LEFT_WIDTH = int(WIDTH * 0.7)
RIGHT_X = LEFT_WIDTH + 10
RIGHT_W = WIDTH - LEFT_WIDTH - 20

ROWS = 4
COLS = 4
CELL_SIZE = 120

font = pygame.font.SysFont("arial", 26)
small_font = pygame.font.SysFont("arial", 20)
mini_font = pygame.font.SysFont("arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
RED = (255, 80, 80)
YELLOW = (255, 220, 0)
LIGHT = (240, 240, 240)
BTN = (60, 60, 60)
CLEANED = (210, 240, 255)
DARK = (35, 35, 35)

clock = pygame.time.Clock()



def load_backend():
    global board, final_board
    global robot_i, robot_j
    global path
    global step
    global logs
    global log_scroll
    global auto_follow
    global running_sim
    global cleaned_cells
    global finished

    board = [row[:] for row in backend.a]
    final_board = [row[:] for row in backend.GOAL]

    robot_i = backend.i
    robot_j = backend.j

    # BỎ NODE START NONE
    path = backend.result[1:] if hasattr(backend, "result") else []

    step = 0
    running_sim = False
    finished = False

    logs = []
    log_scroll = 0
    auto_follow = True

    cleaned_cells = set()

    if len(path) == 0:
        logs.append("❌ NO PATH FOUND")
    else:
        board[robot_i][robot_j] = 0
        cleaned_cells.add((robot_i, robot_j))

        logs.append(f"🤖 Spawn at ({robot_i},{robot_j})")
        logs.append("🧹 Clean Start Position")


load_backend()

last_time = time.time()
delay = 0.45

start_flash = True
flash_timer = 0


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, BTN, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        txt = small_font.render(self.text, True, WHITE)

        screen.blit(
            txt,
            (
                self.rect.centerx - txt.get_width() // 2,
                self.rect.centery - txt.get_height() // 2
            )
        )

    def click(self, e):
        return (
            e.type == pygame.MOUSEBUTTONDOWN
            and self.rect.collidepoint(e.pos)
        )


btn_start = Button(40, 700, 120, 45, "START")
btn_stop = Button(180, 700, 120, 45, "STOP")
btn_next = Button(320, 700, 120, 45, "NEXT")
btn_reset = Button(460, 700, 120, 45, "RESET")



def draw_grid():
    grid_w = COLS * CELL_SIZE

    start_x = (LEFT_WIDTH - grid_w) // 2
    start_y = 100

    for i in range(ROWS):
        for j in range(COLS):

            x = start_x + j * CELL_SIZE
            y = start_y + i * CELL_SIZE

            val = board[i][j]

            color = WHITE

            if val == 1:
                color = GREEN

            elif val == 2:
                color = GRAY

            elif (i, j) in cleaned_cells:
                color = CLEANED

            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            pygame.draw.rect(
                screen,
                BLACK,
                (x, y, CELL_SIZE, CELL_SIZE),
                2
            )

            # COORDINATE
            coord = mini_font.render(f"({i},{j})", True, BLACK)
            screen.blit(coord, (x + 5, y + 5))

            # ROBOT
            if i == robot_i and j == robot_j:

                cx = x + CELL_SIZE // 2
                cy = y + CELL_SIZE // 2

                if start_flash and step == 0:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (cx, cy),
                        CELL_SIZE // 2,
                        5
                    )

                pygame.draw.circle(
                    screen,
                    BLUE,
                    (cx, cy),
                    CELL_SIZE // 3
                )

                eye_r = 4

                pygame.draw.circle(screen, WHITE, (cx - 12, cy - 8), eye_r)
                pygame.draw.circle(screen, WHITE, (cx + 12, cy - 8), eye_r)



def draw_right():
    global log_scroll
    global auto_follow

    # LOG BOX
    pygame.draw.rect(screen, LIGHT, (RIGHT_X, 10, RIGHT_W, 260))
    pygame.draw.rect(screen, BLACK, (RIGHT_X, 10, RIGHT_W, 260), 2)

    screen.blit(font.render("LOG", True, BLACK), (RIGHT_X + 10, 10))

    max_lines = 10

    max_scroll = max(0, len(logs) - max_lines)

    if auto_follow:
        log_scroll = max_scroll

    log_scroll = max(0, min(log_scroll, max_scroll))

    visible = logs[log_scroll:log_scroll + max_lines]

    y = 50

    for line in visible:

        color = BLACK

        if "❌" in line:
            color = RED

        elif "✅" in line:
            color = GREEN

        screen.blit(
            small_font.render(line, True, color),
            (RIGHT_X + 10, y)
        )

        y += 22

    # INFO PANEL
    pygame.draw.rect(screen, LIGHT, (RIGHT_X, 290, RIGHT_W, 190))
    pygame.draw.rect(screen, BLACK, (RIGHT_X, 290, RIGHT_W, 190), 2)

    screen.blit(font.render("INFO", True, BLACK), (RIGHT_X + 10, 300))

    info_y = 340

    info_list = [
        f"ALGORITHM : UCS2",
        f"STEP      : {step}/{len(path)}",
        f"POSITION  : ({robot_i},{robot_j})",
        f"CLEANED   : {len(cleaned_cells)} CELLS",
        f"COST     : {path[step-1].COST}"
    ]

    for txt in info_list:
        screen.blit(
            small_font.render(txt, True, BLACK),
            (RIGHT_X + 10, info_y)
        )

        info_y += 25

    # FINAL STATE
    screen.blit(font.render("FINAL STATE", True, BLACK), (RIGHT_X + 10, 510))

    size = 40

    for i in range(ROWS):
        for j in range(COLS):

            x = RIGHT_X + j * size
            y = 560 + i * size

            val = final_board[i][j]

            color = WHITE

            if val == 1:
                color = GREEN

            elif val == 2:
                color = GRAY

            pygame.draw.rect(screen, color, (x, y, size, size))
            pygame.draw.rect(screen, BLACK, (x, y, size, size), 1)


running = True

while running:

    clock.tick(60)

    if start_flash:

        flash_timer += clock.get_time()

        if flash_timer > 500:
            start_flash = False

    for e in pygame.event.get():

        if e.type == pygame.QUIT:
            running = False

        # START
        if btn_start.click(e):

            if len(path) > 0:
                running_sim = True
                auto_follow = True

            else:
                logs.append("❌ Cannot start")

        # STOP
        if btn_stop.click(e):
            running_sim = False
            logs.append("⏸ Simulation Paused")

        # NEXT
        if btn_next.click(e):

            if step < len(path):

                node = path[step]

                robot_i, robot_j = node.i, node.j

                board[robot_i][robot_j] = 0

                cleaned_cells.add((robot_i, robot_j))

                logs.append(f"➡ {node.ACTION}")

                step += 1

        if btn_reset.click(e):

            start_flash = True
            flash_timer = 0

            load_backend()


        if e.type == pygame.MOUSEWHEEL:
            log_scroll -= e.y
            auto_follow = False

    if running_sim and step < len(path):

        if time.time() - last_time > delay:

            node = path[step]

            robot_i, robot_j = node.i, node.j

            board[robot_i][robot_j] = 0

            cleaned_cells.add((robot_i, robot_j))

            logs.append(f"➡ {node.ACTION}")

            step += 1

            last_time = time.time()

    # FINISH
    if step >= len(path) and len(path) > 0 and not finished:

        finished = True
        running_sim = False

        logs.append("✅ CLEAN COMPLETE")

    # =========================
    # DRAW
    # =========================
    screen.fill(DARK)

    title = font.render("VACUUM AI", True, WHITE)
    screen.blit(title, (50, 20))

    draw_grid()
    draw_right()

    btn_start.draw()
    btn_stop.draw()
    btn_next.draw()
    btn_reset.draw()

    # COMPLETE TEXT
    if finished:

        txt = font.render("MISSION COMPLETE", True, YELLOW)

        screen.blit(
            txt,
            (
                LEFT_WIDTH // 2 - txt.get_width() // 2,
                620
            )
        )

    pygame.display.update()

pygame.quit()
